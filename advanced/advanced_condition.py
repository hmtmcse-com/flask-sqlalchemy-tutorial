from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///advanced-condition.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)
    income = db.Column(db.Float, default=0)


with app.app_context():
    db.create_all()


@app.route('/')
def bismillah():
    return "Flask SQLAlchemy Advanced Condition Tutorial"


def render_table(data):
    response = "<table><tr><th>Name</th><th>Email</th><th>Age</th><th>Income</th></tr>"
    for person in data:
        response += "<tr>" + "<td>" + person.first_name + "</td>" + "<td>" + person.email + "</td>"
        response += "<td>" + str(person.age) + "</td>" + "<td>" + str(person.income) + "</td>" + "</tr>"
    response += "</table>"
    return response


def render_details(data):
    if not data:
        return ""
    response = "Name : " + data.first_name + "<br>"
    response += "Email : " + data.email + "<br>"
    response += "Age : " + str(data.age) + "<br>"
    response += "Income : " + str(data.income) + "<br>"
    return response


@app.route('/init-sample-data')
def init_sample_data():
    model_list = []
    for person_number in range(20):
        person = Person(
            first_name="Person " + str(person_number),
            email="person-" + str(person_number) + "@email.loc",
            age=13 + person_number,
            income=13 * person_number,
        )
        model_list.append(person)

    db.session.add_all(model_list)
    db.session.commit()
    return "Successfully Initialized"


@app.route('/list')
def list():
    return render_table(Person.query.all())


@app.route('/query-by-session')
def query_by_session():
    person = db.session.query(Person).first()
    return render_details(person)


@app.route('/equal')
def equal():
    person = Person.query.filter(Person.first_name == "Person 0").one()
    return render_details(person)


@app.route('/not-equal')
def mpt_equal():
    person = Person.query.filter(Person.first_name != "Person 0").all()
    return render_table(person)


@app.route('/less-than')
def less_than():
    person = Person.query.filter(Person.age < 20).all()
    return render_table(person)


@app.route('/less-than-equal')
def less_than_equal():
    person = Person.query.filter(Person.age <= 20).all()
    return render_table(person)


@app.route('/greater-than')
def greater_than():
    person = Person.query.filter(Person.age > 20).all()
    return render_table(person)


@app.route('/greater-than-equal')
def greater_than_equal():
    person = Person.query.filter(Person.age >= 20).all()
    return render_table(person)


@app.route('/like-case-sensitive')
def like_case_sensitive():
    person = Person.query.filter(Person.first_name.like("Person%")).all()
    return render_table(person)


@app.route('/like-case-insensitive')
def like_case_insensitive():
    person = Person.query.filter(Person.first_name.ilike("person%")).all()
    return render_table(person)


@app.route('/in-list')
def in_list():
    person = Person.query.filter(Person.id.in_([12, 13, 18, 1])).all()
    return render_table(person)


@app.route('/not-in-list')
def not_in_list():
    person = Person.query.filter(Person.id.not_in([12, 13, 18, 1])).all()
    return render_table(person)


@app.route('/is-null')
def is_null():
    person = Person.query.filter(Person.last_name == None).all()
    # OR
    person = Person.query.filter(Person.last_name.is_(None)).all()
    return render_table(person)


@app.route('/is-not-null')
def is_not_null():
    person = Person.query.filter(Person.last_name != None).all()
    # OR
    person = Person.query.filter(Person.last_name.is_not(None)).all()
    return render_table(person)


@app.route('/and-condition')
def and_condition():
    person_type1 = Person.query.filter(and_(Person.first_name != "Person 0", Person.first_name != "Person 1")).all()
    # OR
    person_type2 = Person.query.filter(Person.first_name != "Person 0", Person.first_name != "Person 1").all()
    # OR
    person_type3 = Person.query.filter(Person.first_name != "Person 0").filter(Person.first_name != "Person 1").all()

    response = "<h1>Type 1 </h1>"
    response += render_table(person_type1)
    response += "<br/><br/>"
    response += "<h1>Type 2 </h1>"
    response += render_table(person_type2)
    response += "<br/><br/>"
    response += "<h1>Type 3 </h1>"
    response += render_table(person_type3)
    response += "<br/><br/>"
    return response


@app.route('/or-condition')
def or_condition():
    person = Person.query.filter(or_(Person.first_name == "Person 0", Person.first_name == "Person 1")).all()
    return render_table(person)


@app.route('/order-by')
def order_by():
    person = Person.query.order_by(Person.age.asc()).all()
    # OR
    person = Person.query.order_by(Person.age.desc()).all()
    return render_table(person)


if __name__ == '__main__':
    app.run()
