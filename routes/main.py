from flask import Blueprint, render_template, request
from models.link import db
from models.link import Link

main = Blueprint('main',__name__)

@main.route("/")
def home():
    all = Link.query.all()
    print(all)
    return render_template('home.html', all_links = all)

@main.route("/add_your_link")
def get_add_link():
    return render_template('addLink.html')

@main.route("/add_your_link", methods= ['POST'])
def post_add_link():
    link = Link(request.form['link'], request.form['description'], 0)
    db.session.add(link)
    db.session.commit()
    return get_add_link()
