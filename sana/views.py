from flask import render_template, request, flash, redirect, url_for, session, abort
from sana import app, login_manager
from flask_login import current_user, login_required, login_user, logout_user
from forms import PNOForm, NameForm, PasswordForm, LoginForm
from datetime import datetime, timedelta
from models import User, Request
from . import db
from random import randint
import threading

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/index')
def index():
    flash('{}'.format(request.remote_addr))
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    # first check if this ip should be banned
    r = Request.query.filter_by(request_addr = request.remote_addr).first()
    if r == None:
        r = Request(request_addr = request.remote_addr)
        db.session.add(r)
        db.session.commit()
    else:
        r.attempts += 1
        should_ban = True if r.attempts > 3 else False
        if should_ban:
            r.banned_until = datetime.now() + timedelta(hours = 1)

            # remove the  ban after 1 hour
            oneHourInSecond = 1 * 60 * 60
            threading.Timer(oneHourInSecond, remove_ban, (request.remote_addr,)).start()

        db.session.add(r)
        db.session.commit()

        if should_ban:
            abort(403)

    if current_user.is_authenticated:
        return render_template(url_for('index'))

    form = PNOForm()
    if form.validate_on_submit():
        pno = form.pno.data
        user = User.get_by_pno(pno)

        # user has registered before
        if user is not None:
            session['pno'] = pno
            return redirect(url_for('login4'))

        # no such user ever existed
        else:
            user = User(pno)
            db.session.add(user)
            db.session.commit()

            # generate random for verification code
            # not doing anything for now, reserved for future probably
            rand = randint(1000, 9999)
            flash('this is your verification code: {}'.format(rand))

            session['pno'] = pno
            session['verif_code'] = rand
            return redirect(url_for('login2'))

        return render_template('index.html')
    return render_template('login.html', form = form)

@app.route('/login2', methods = ['GET', 'POST'])
def login2():
    if 'pno' not in session.keys():
        flash('enter pno first')
        return redirect(url_for('login'))

    form = NameForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data


        session['firstname'] = firstname
        session['lastname'] = lastname
        return redirect(url_for('login3'))
    return render_template('login.html', form = form)

@app.route('/login3', methods = ['GET', 'POST'])
def login3():
    if 'pno' not in session.keys():
        flash('enter pno first')
        return redirect(url_for('login'))

    for key in ['firstname', 'lastname']:
        if key not in session.keys():
            flash('enter name first')
            return redirect(url_for('login2'))

    form = PasswordForm()
    if form.validate_on_submit():
        password = form.password.data

        pno = session['pno']
        firstname = session['firstname']
        lastname = session['lastname']

        user = User.get_by_pno(pno)
        user.firstname = firstname
        user.lastname = lastname
        user.password = password

        db.session.add(user)
        db.session.commit()

        login_user(user)

        remove_ban(request_obj = request.remote_addr)

        return redirect(url_for('index'))
    return render_template('login.html', form = form)

@app.route('/login4', methods = ['GET', 'POST'])
def login4():
    if 'pno' not in session.keys():
        flash('enter pno first')
        return redirect(url_for('login'))

    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        pno = session['pno']
        user = User.get_by_pno(pno)

        if user.check_password(password):
            flash('welcome user {}'.format(user))
            login_user(user)

            remove_ban(request = request.remote_addr)

            return redirect(url_for('index'))
        flash("wrong password")
        return redirect(url_for('login'))
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(403)
def error_handler(e):
    flash('not allowed to request more than 3 times')
    return redirect(url_for('index')), 200

def remove_ban(request_obj):
    r = Request.query.filter_by(request_addr = request_obj).first()
    if r is not None:
        r.attempts = 0
        r.banned_until = None
        db.session.add(r)
        db.session.commit()
