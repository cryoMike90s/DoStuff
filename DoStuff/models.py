from flask import current_app
from DoStuff import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login knows nothing about db, it needs app help in loading a user. That is the reason the app will
    configure a user_loader func, that can be called to load a user by giving the ID. The load user is registered
    with the decorator.
    """
    return User.query.get(int(user_id))


# inheritance from UserMixin class save us from writing a bunch of class like IsAnonymus or Active
class User(db.Model, UserMixin):
    """
    SQLAlchemy database class for User, that inherits from db.Model base class of Flask-SQLAlchemy
    Args:
        db.Model: Base class of Flask SQLAlchemy
        UserMixin: Flask-Login works with the app's user model and expect certain prop. `is_authenticated`, `is_active`,
                    `is_anonymous`, `get_id()`. Instead of implement all of them separately there is class UserMixin
                    class which provides generic implementation of them

    """
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    projects = db.relationship('Projects', backref='owner', cascade='all,delete', lazy=True)

    def __repr__(self):
        """
        Method which tells Python how to print objects of class
        """
        return "User( '{}', '{}', '{}')".format(self.user_name, self.email, self.image_file)

    def get_secret_token(self, expiration_time=1800):
        """Creates a secret token which would be send on user email"""
        s = Serializer(current_app.config['SECRET_KEY'], expiration_time)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_secret_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id =s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasks = db.relationship('Tasks', backref='parent', cascade='all,delete', lazy=True)

    def __repr__(self):
        return "Projects( '{}')".format(self.title)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    project_parent = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    def __repr__(self):
        return "Tasks( '{}, {}')".format(self.task_name, self.content)