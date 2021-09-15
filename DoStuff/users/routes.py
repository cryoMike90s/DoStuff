from flask import Blueprint, render_template, redirect, flash, url_for, request
from DoStuff.users.forms import RegisterForm, LoginForm
from DoStuff.models import User
from flask_login import login_user, current_user, logout_user, login_required
from DoStuff import db, bcrypt

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    """ Basic feature for page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(user_name=form.user_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created for {} !".format(form.user_name.data), 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register Me', form=form)


@users.route('/')
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next') #if user is trying to get in to specific page, after log in it would transport it to this page
            flash("Login Successful", 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template('login.html', title='Log In', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))
