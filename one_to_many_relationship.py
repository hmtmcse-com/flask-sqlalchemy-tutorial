from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///one-to-many.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)
    income = db.Column(db.Float, default=0)
    addresses = db.relationship('Address', backref='person', lazy=True, cascade="all, delete")


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50))
    region = db.Column(db.String(50))
    postal_code = db.Column(db.String(50))
    details = db.Column(db.Text)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def bismillah():
    return "Flask SQLAlchemy One to Many Entity Relation Tutorial"


@app.route('/init-sample-data')
def init_sample_data():
    person_list = []
    for person_number in range(3):
        person = Person(first_name="Person " + str(person_number), email="person-" + str(person_number) + "@email.loc")
        for address_number in range(2):
            address = Address(country="Country " + str(person_number) + str(address_number))
            person.addresses.append(address)
        person_list.append(person)
    db.session.add_all(person_list)
    db.session.commit()
    return "Successfully Initialized"


@app.route('/list-address')
def list_address():
    response = ""
    addresses = Address.query.all()
    for data in addresses:
        response += data.country + " " + data.person.first_name + "<br>"
    return response


@app.route('/list')
def list():
    response = "<ul>"
    persons = Person.query.all()
    for data in persons:
        response += "<li>" + data.first_name + " " + data.email
        if data.addresses:
            response += "<ul>"
            for address in data.addresses:
                response += "<li>" + address.country + "</li>"
            response += "</ul>"
        response += "</li>"
    response += "</ul>"
    return response


@app.route('/delete')
def delete():
    person = Person.query.filter_by(id=1).first()
    if person:
        db.session.delete(person)
        db.session.commit()
    return "Record has been deleted"


if __name__ == '__main__':
    app.run()
