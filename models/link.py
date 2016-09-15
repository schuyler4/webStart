from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class Link(db.Model):
    id = db.Column('link_id', db.Integer, primary_key=True)
    link = db.Column(String)
    description = db.Column(String)
    views = db.Column(Integer)
    user = db.Column(db.String(100))

    def __init__(self, link, description, views):
        self.link = link
        self.description = description
        self.views = views


class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))

    def __init__(self, username, password, user):
        self.username = username
        self.password = password
        self.user = user

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


db.create_all()
