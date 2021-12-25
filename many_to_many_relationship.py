from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///many-to-many.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

person_degree = db.Table(
    'person_degree',
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True),
    db.Column('degree_id', db.Integer, db.ForeignKey('degree.id'), primary_key=True)
)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)
    income = db.Column(db.Float, default=0)
    degrees = db.relationship('Degree', secondary=person_degree, lazy='subquery', backref=db.backref('degrees', lazy=True))


class Degree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)


with app.app_context():
    db.create_all()


@app.route('/')
def bismillah():
    return "Flask SQLAlchemy Many to Many Entity Relation Tutorial"


@app.route('/init-sample-data')
def init_sample_data():
    person_and_degree_list = []
    for person_number in range(3):
        person = Person(first_name="Person " + str(person_number), email="person-" + str(person_number) + "@email.loc")
        person_and_degree_list.append(person)

    for degree_number in range(5):
        degree = Degree(name="Degree " + str(degree_number), type="Certification-" + str(degree_number))
        person_and_degree_list.append(degree)

    db.session.add_all(person_and_degree_list)
    db.session.commit()
    return "Successfully Initialized"


@app.route('/create')
def create():
    # Get 1 person and associate degree 1 and 2
    person = Person.query.get(1)
    if person:
        degrees = Degree.query.filter(Degree.id.in_([1, 2])).all()
        person.degrees = []  # Remove previous entry
        for degree in degrees:
            person.degrees.append(degree)
        db.session.add(person)
        db.session.commit()
    response = "Data successfully Inserted"
    return response


@app.route('/update')
def update():
    # Get 1 person and associate degree 3 and 4
    person = Person.query.get(1)
    if person:
        degrees = Degree.query.filter(Degree.id.in_([3, 4])).all()
        person.degrees = []  # Remove previous entry
        for degree in degrees:
            person.degrees.append(degree)
        db.session.add(person)
        db.session.commit()
    return "Data has been updated."


@app.route('/delete')
def delete():
    person = Person.query.filter_by(id=1).first()
    if person:
        db.session.delete(person)
        db.session.commit()
    return "Record has been deleted"


@app.route('/list')
def list():
    response = "<ul>"
    persons = Person.query.all()
    for data in persons:
        response += "<li>" + data.first_name + " " + data.email
        if data.degrees:
            response += "<ul>"
            for degree in data.degrees:
                response += "<li>" + degree.name + " " + degree.type + "</li>"
            response += "</ul>"
        response += "</li>"
    response += "</ul>"
    return response


if __name__ == '__main__':
    app.run()
