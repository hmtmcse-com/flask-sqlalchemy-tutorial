from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask-sqlalchemy.sqlite"
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
    return "Flask SQLAlchemy CRUD Tutorial"


@app.route('/create')
def create():
    person = Person(first_name="First Name", last_name="Last Name", email="hmtmcse.com@gmail.com", age=22, income =500)
    db.session.add(person)
    db.session.commit()
    response = "Data successfully Inserted"
    return response


@app.route('/update')
def update():
    person = Person.query.filter_by(id=1).first()
    if person:
        person.first_name = "FName Update"
        person.last_name = "LName Update"
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
    response = ""
    persons = Person.query.all()
    for person in persons:
        response += person.first_name + " " + person.last_name + " " + person.email + "<br>"
    return response


@app.route('/create-bulk')
def create_bulk():
    person_list = []
    total_record = 20
    for index in range(total_record):
        person_list.append(
            Person(
                first_name="First Name " + str(index),
                last_name="Last Name " + str(index),
                email="email-" + str(index) + "@email.loc",
                age=1 * index,
                income=100 * index)
        )
    db.session.add_all(person_list)
    db.session.commit()
    response = str(total_record) + " Records successfully Inserted"
    return response


@app.route('/pagination')
@app.route('/pagination/<int:per_page>')
@app.route('/pagination/<int:page>/<int:per_page>')
def pagination(page: int = 1, per_page: int = 5):
    response = {
        "page": 0,
        "pages": 0,
        "per_page": 0,
        "totalItem": 0,
        "items": [],
    }
    persons = Person.query.paginate(page, per_page, error_out=False)
    if persons:
        response["page"] = persons.page
        response["pages"] = persons.pages
        response["per_page"] = persons.per_page
        response["totalItem"] = persons.total
        for person in persons.items:
            response["items"].append(person.first_name + " " + person.last_name + " " + person.email)
    return response


if __name__ == '__main__':
    app.run()
