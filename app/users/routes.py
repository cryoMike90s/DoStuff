from flask import Blueprint, render_template, redirect, flash, url_for, request
from app.users.forms import RegisterForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.users.utils import save_image
from app.users.email import send_reset_email
from app.tasks.forms import ProjectForm


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))  # if user is logged then redirect automatically to main.home route

    form = RegisterForm()

    if form.validate_on_submit():
        # hashed password as first stage of security for user passwords
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(user_name=form.user_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created for {} !".format(form.user_name.data), 'success')

        return redirect(url_for('users.login'))

    return render_template('register.html', title='Registration page', form=form)



@users.route('/login', methods=['GET', 'POST'])
def login():
    """ Basic landing page for unauthenticated users """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')  # get next url parameter and after login redirect to requested page
            flash("Login Successful", 'success')

            # if there was request for specific page that needs authorization, then that argument assigned in
            # variable `next_page` keeps that and after login automatically user is redirect to that page
            return redirect(next_page) if next_page else redirect(url_for('main.home'))

        else:
            flash("Login Unsuccessful. Please check email and password", "danger")

            return redirect(url_for('users.login'))

    return render_template('login.html', title='Log In', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """
    Function allows for current user information modification. There is feature for change of default picture that
    is assigned during registration of new user. Part of change user picture is connected with save_image()
    function located in `utils.py` where name of original picture file is processing and then saved

    new_project_form in render_template() return is intentionally located here to allow for rendering
    tasks.new_project_2 function
    """
    form = UpdateAccountForm()
    new_project_form = ProjectForm()

    if form.validate_on_submit():

        if form.picture.data:  # if statement responsible for change of default picture
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

    return render_template('account.html',
                           title="Account",
                           form=form,
                           img_file=img_file,
                           new_project_form=new_project_form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    """
    Function that render form for email input that is destination of utils.send_reset_email function responsible
    for sending email to user with token that is available for specific period of time and reset user's password
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)  # located in utils.py
        flash('An email has been sent with instruction to reset your password', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_password_request.html', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """
    Routes handling reset password token (logic is coded in models.py), if token is valid user has chance to
    change his password and that change is committed to database, but when token is not valid or expired note
    is rendering to user
    """
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))

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
