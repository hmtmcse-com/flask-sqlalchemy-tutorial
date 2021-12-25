from flask import Flask
from flask_sqlalchemy import SQLAlchemy, BaseQuery


class CustomQuery(BaseQuery):
    def get_or(self, ident, default=None):
        return self.get(ident) or default


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///custom-query.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app, query_class=CustomQuery)


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
    return "Flask SQLAlchemy Custom Query Class"


@app.route('/init-sample-data')
def init_sample_data():
    model_list = []
    for person_number in range(3):
        person = Person(first_name="Person " + str(person_number), email="person-" + str(person_number) + "@email.loc")
        model_list.append(person)

    db.session.add_all(model_list)
    db.session.commit()
    return "Successfully Initialized"


@app.route('/custom-query/<int:id>')
def custom_query(id):
    person = Person.query.get_or(id, "No User")
    if isinstance(person, str):
        return person
    return person.first_name


if __name__ == '__main__':
    app.run()
