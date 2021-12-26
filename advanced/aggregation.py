from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aggregation.sqlite"
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


def render_table(data):
    response = "<table><tr><th>Name</th><th>Email</th><th>Age</th><th>Income</th></tr>"
    for person in data:
        response += "<tr>" + "<td>" + person.first_name + "</td>" + "<td>" + person.email + "</td>"
        response += "<td>" + str(person.age) + "</td>" + "<td>" + str(person.income) + "</td>" + "</tr>"
    response += "</table>"
    return response


@app.route('/')
def bismillah():
    return "Flask SQLAlchemy Aggregation Function Tutorial"


@app.route('/init-sample-data')
def init_sample_data():
    model_list = []
    for person_number in range(20):
        age = 13 + person_number
        income = 13 * person_number
        email = "person-" + str(person_number) + "@email.loc"
        email2 = "person2-" + str(person_number) + "@email.loc"
        first_name = "Person " + str(person_number)
        first_name2 = "Person2 " + str(person_number)

        person = Person(first_name=first_name, email=email, age=age, income=income, )
        model_list.append(person)

        if person_number < 10:
            person = Person(first_name=first_name2, email=email2, age=age, income=income, )
            model_list.append(person)

    db.session.add_all(model_list)
    db.session.commit()
    return "Successfully Initialized"


@app.route('/list')
def list():
    return render_table(Person.query.all())


@app.route('/select-columns')
def select_columns():
    persons = Person.query.with_entities(Person.id, Person.first_name).all()
    response = ""
    for row in persons:
        response += "ID : " + str(row.id) + " Name: " + str(row.first_name) + "<br/>"
    return response


@app.route('/count-row')
def count_row():
    count_way_one = Person.query.count()
    count_way_two = Person.query.with_entities(func.count(Person.id)).first()
    response = ""
    response += "Count way 1 total row : " + str(count_way_one)
    response += "<br>"
    response += "Count way 2 total row : " + str(count_way_two[0])
    return response


@app.route('/sum-income')
def sum_income():
    result = Person.query.with_entities(func.sum(Person.income)).first()
    response = ""
    response += "Total Salary : " + str(result[0])
    return response


@app.route('/column-alias')
def column_alias():
    result = Person.query.with_entities(func.sum(Person.income).label("sum"), Person.first_name.label("name")).first()
    response = ""
    response += "Total Salary : " + str(result.sum) + "<br>"
    response += "Name : " + str(result.name)
    return response


@app.route('/average-income')
def average_income():
    result = Person.query.with_entities(func.avg(Person.income)).first()
    response = ""
    response += "Average Salary : " + str(result[0])
    return response


@app.route('/max-income')
def max_income():
    result = Person.query.with_entities(func.max(Person.income)).first()
    response = ""
    response += "Max Salary : " + str(result[0])
    return response


@app.route('/min-income')
def min_income():
    result = Person.query.with_entities(func.min(Person.income)).first()
    response = ""
    response += "Min Salary : " + str(result[0])
    return response


@app.route('/age-group-by-income')
def age_group_by_income():
    result = Person.query.with_entities(Person.age, Person.income, func.count(Person.age).label("total")).group_by(Person.income).all()
    response = ""
    for row in result:
        response += "Age : " + str(row.age) + " Income: " + str(row.income)
        response += " Total: " + str(row.total) + "<br/>"
    return response


if __name__ == '__main__':
    app.run()
