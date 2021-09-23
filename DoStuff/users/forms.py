from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import Length, DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from DoStuff.models import User
from flask_login import current_user


class RegisterForm(FlaskForm):
    user_name = StringField('User', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit_me = SubmitField('Register')

    def validate_user_name(self, user_name):
        """
        Function that check if current input (user_name) is already in database, if so, then user would get message
        about this fact
        """
        user = User.query.filter_by(user_name=user_name.data).first()
        if user:
            raise ValidationError('This username is already taken please choose different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered please choose different one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    log_in = SubmitField('Log In')
    remember_me = BooleanField('Remember Me')


class UpdateAccountForm(FlaskForm):
    user_name = StringField('User', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Now')

    def validate_user_name(self, user_name):
        if user_name.data != current_user.user_name:
            user = User.query.filter_by(user_name=user_name.data).first()
            if user:
                raise ValidationError("This user name is already taken, please choose different one")

    def validate_email(self, email):
        if email.data != current_user.email:
            user_email = User.query.filter_by(email=email.data).first()
            if user_email:
                raise ValidationError('That email is already taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    request = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        if user_email is None:
            raise ValidationError("That email address does not exists in our base")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    reset = SubmitField('Reset Password')

