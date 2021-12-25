from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/flask_sqlalchemy"
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
    return "Flask SQLAlchemy MySQL/MariaDB connection Tutorial"


if __name__ == '__main__':
    app.run()
