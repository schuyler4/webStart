from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from models.link import Link, User, db_session
from sqlalchemy import *
from sqlalchemy.orm import *
main = Blueprint('main', __name__)


@main.route("/")
def home():
    if session['logged_in']:
        username = session['username']
        logged_in = session['logged_in']
    all_links = db_session.query(Link).all()
    print all_links
    return render_template('home.html', username=username, logged_in=logged_in, all_links=all_links)


@main.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        retype_password = request.form['retype_password']
        exists = db_session.query(db_session.query(User).filter_by(username=username).exists()).scalar()
        if exists:
            flash("that username was already used")
            return redirect(url_for("main.signup"))
        else:
            if password == retype_password:
                user = User(username, password)
                db_session.add(user)
                db_session.commit()
                flash('your account was successfully created')
                return redirect(url_for('main.home'))
    return render_template('signup.html')


@main.route("/login", methods=['GET', 'POST'])
def login():
    if session['logged_in']:
        username = session['username']
        return redirect(url_for('main.profile', username=username))
    else:
        render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = db_session.query(User).filter(User.username == username, User.password == password)
        result = query.first()
        if result:
            session['logged_in'] = True
            session['username'] = username
            flash("your logged in")
            return redirect(url_for('main.profile', username=session['username']))
        else:
            flash("your usename of password is not right")
            return redirect(url_for('main.login'))
    return render_template('login.html')


@main.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = None
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
            link_exists = db_session.query(exists().where(Link.link == link)).scalar()
            user_number = db_session.query(Link).filter(Link.owner == session['username']).count()
            print user_number
            print "panda"
            if not link_exists and user_number < 5:
                link = request.form['link']
                description = request.form['description']
                username = session['username']
                link = Link(link, description, 0, username)
                db_session.add(link)
                db_session.commit()
                redirect(url_for('main.profile', username=session['username']))
            else:
                if user_number > 5:
                    flash("you are at your maximum 5 links you need to delete one to add another")
                elif link_exists:
                    flash("someone already posted that link")
                return redirect(url_for('main.profile', username=session['username']))
        url_username = request.args.get('username')
        #print url_username
        #if url_username == session['username']:
        users_links = db_session.query(Link).all()
        print users_links
        return render_template('profile.html', links=users_links, username=session['username'])
       # else:
            #return redirect(url_for('main.home'))

@main.errorhandler(404)
def page_not_found():
    return render_template('404.html')


@main.errorhandler(500)
def server_err():
    return render_template('500.html')
