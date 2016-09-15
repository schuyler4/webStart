from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from models.link import db
from models.link import Link
from models.link import User
main = Blueprint('main', __name__)


@main.route("/")
def home():
    logged_in = None
    username = None
    if session['logged_in']:
        username = session['username']
        logged_in = True
    return render_template('home.html', username=username, logged_in=logged_in)


@main.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        exists = db.session.query(db.session.query(User).filter_by(username=username).exists()).scalar()
        if exists:
            flash("that username was already used")
            return redirect(url_for("main.signup"))
        else:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
            flash('your account was successfully created')
            return redirect(url_for('main.home'))
    return render_template('signup.html')


@main.route("/login", methods=['GET', 'POST'])
def login():
    if session['logged_in']:
        return redirect(url_for('main.profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = User.query.filter(User.username == username, User.password == password)
        result = query.first()
        if result:
            session['logged_in'] = True
            session['username'] = username
            flash("your logged in")
            return redirect(url_for('main.profile'))
        else:
            flash("your usename of password is not right")
            return redirect(url_for('main.login'))
    return render_template('login.html')


@main.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('main.home'))


def logged_in():
    if session['logged_in']:
        return True
    else:
        return False


@main.route("/profile/<username>", methods=['GET', 'POST'])
def profile(username):
    if not logged_in():
        redirect(url_for('main.login'))
    else:
        if request.method == 'POST':
            link = request.form['link']
            description = request.form['description']
            exits = db.session.query(db.session.query(Link).filter_by(link=link).exists()).scalar()
            if not exits:
                username = session['username']
                link = Link(link, description, username, 0)
                db.session.add(link)
                db.session.commit()
                redirect(url_for('main.profile', username = session['username']))
            else:
                flash("someone already posted that link")
                return redirect(url_for('main.profile', username = session['username']))
        users_links = Link.query.filter(Link.user == session['username'])
        return render_template('profile.html', users_links = users_links, username=session['username'])