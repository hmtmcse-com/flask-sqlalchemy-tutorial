from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import aliased

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///joining.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)
    income = db.Column(db.Float, default=0)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50))
    region = db.Column(db.String(50))
    postal_code = db.Column(db.String(50))
    details = db.Column(db.Text)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)


class Degree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)


class PersonDegree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    degree_id = db.Column(db.Integer, db.ForeignKey('degree.id'), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def bismillah():
    return "Flask SQLAlchemy Joining Tutorial Tutorial"


def associate_person_degree(person_id, degrees: list):
    person = Person.query.get(person_id)
    if person:
        model_list = []
        for degree in degrees:
            model_list.append(PersonDegree(person_id=person_id, degree_id=degree))
        db.session.add_all(model_list)
        db.session.commit()


@app.route('/init-sample-data')
def init_sample_data():
    model_list = []
    for person_number in range(5):
        person = Person(first_name="Person " + str(person_number), email="person-" + str(person_number) + "@email.loc")
        db.session.add(person)
        db.session.commit()
        for address_number in range(2):
            model_list.append(Address(country="Country " + str(person_number) + str(address_number), person_id=person.id))

    for degree_number in range(8):
        degree = Degree(name="Degree " + str(degree_number), type="Certification-" + str(degree_number))
        model_list.append(degree)

    db.session.add_all(model_list)
    db.session.commit()
    associate_person_degree(1, [2, 3])
    associate_person_degree(3, [5, 6])
    associate_person_degree(2, [1, 7])
    return "Successfully Initialized"


@app.route('/get-join-result')
def join_result():
    response = ""

    # Way 1
    way_1 = db.session.query(Person, Address, Degree, PersonDegree).filter(
        Person.id == Address.person_id,
        Person.id == PersonDegree.person_id,
        Degree.id == PersonDegree.degree_id
    ).all()

    response += "<h1>Way 1</h1>"
    for data in way_1:
        response += "Person Name: " + data[0].first_name + " Address Country : " + data[1].country
        response += " Degree name : " + data[2].name + "<br>"

    # Way 2 use alias
    p, a, d = aliased(Person, name="p"), aliased(Address, name="a"), aliased(Degree, name="d")
    way_2 = db.session.query(p, a, d, PersonDegree).filter(
        p.id == a.person_id,
        p.id == PersonDegree.person_id,
        d.id == PersonDegree.degree_id
    ).all()

    response += "<h1>Way 2</h1>"
    for data in way_2:
        response += "Person Name: " + data.p.first_name + " Address Country : " + data.a.country
        response += " Degree name : " + data.d.name + "<br>"

    way_3 = Person.query \
        .join(Address, Person.id == Address.person_id) \
        .join(PersonDegree, Person.id == PersonDegree.person_id) \
        .join(Degree, Degree.id == PersonDegree.degree_id)\
        .add_columns(Person.first_name, Address.country.label("acountry"), Degree.name)\
        .all()

    response += "<h1>Way 3</h1>"
    for data in way_3:
        response += "Person Name: " + data[0].first_name + " Address Country : " + data.acountry
        response += " Degree name : " + data[3] + "<br>"

    return response


if __name__ == '__main__':
    app.run()
