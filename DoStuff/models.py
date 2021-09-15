from DoStuff import db, login_manager
from flask_login import UserMixin

# handle session in the background, decorator puprose to give information for extension that this is the function to get
# user by an ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# inheritance from UserMixin class save us from writing a bunch of class like IsAnonymus or Active
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    projects = db.relationship('Projects', backref='owner', lazy=True)

    def __repr__(self):
        return "User( '{}', '{}', '{}')".format(self.user_name, self.email, self.image_file)


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Projects( '{}', '{}')".format(self.title, self.date_posted)