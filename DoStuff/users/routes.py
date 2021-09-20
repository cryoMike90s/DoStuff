from flask import Blueprint, render_template, redirect, flash, url_for, request
from DoStuff.users.forms import RegisterForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from DoStuff.models import User
from flask_login import login_user, current_user, logout_user, login_required
from DoStuff import db, bcrypt
from DoStuff.users.utilis import save_image
from DoStuff.users.email import send_reset_email


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


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_image(form.picture.data)
            current_user.img_file = picture_file
        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Changes saved", "success")
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email

    img_file = url_for('static', filename='images/' + current_user.img_file)

    return render_template('account.html', title="Account", form=form, img_file=img_file)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_password_request.html', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.home')) # nikoniecznie jest to potrzebne na razie
    user = User.verify_secret_token(token)
    if user is None:
        flash('That is invalid or expired token', 'warning')
        return redirect(url_for('users.reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form=form)


