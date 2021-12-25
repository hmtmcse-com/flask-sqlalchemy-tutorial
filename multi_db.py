from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///default-db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_BINDS"] = {
    'person': 'sqlite:///person-db.sqlite',
    'degree': 'sqlite:///degree-db.sqlite'
}
db = SQLAlchemy(app)


class Person(db.Model):
    __bind_key__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)
    income = db.Column(db.Float, default=0)


class Degree(db.Model):
    __bind_key__ = 'degree'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)


with app.app_context():
    db.create_all()


@app.route('/')
def bismillah():
    return "Flask SQLAlchemy Multi Database bind"


if __name__ == '__main__':
    app.run()
