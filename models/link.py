from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, Column, Integer, DateTime, func, String

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'

class Link(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    link = db.Column(String)
    description = db.Column(String)
    views = db.Column(Integer)

    def __init__(self, link, description, views):
        self.link = link
        self.description = description
        self.views = views

db.create_all()
