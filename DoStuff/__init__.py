from flask import Flask
from flask_sqlalchemy import *
from typing import Callable
from config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail


class MySQLAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Integer: Callable
    DateTime: Callable
    Text: Callable
    relationship: Callable
    ForeignKey: Callable


db = MySQLAlchemy()
migrate = Migrate()
mail = Mail()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = u"You need to Log In first."
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class) #Configuration from specific file

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)



    #importing blueprints from specific directories
    from DoStuff.main.routes import main
    from DoStuff.tasks.routes import tasks
    from DoStuff.users.routes import users

    #register of those Blueprints
    app.register_blueprint(main)
    app.register_blueprint(tasks)
    app.register_blueprint(users)

    with app.app_context():
        db.create_all()



    return app