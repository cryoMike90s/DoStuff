from DoStuff.models import User, Projects
from flask_login import current_user


def project_list():
    projects_nav = Projects.query.filter_by(user_id=current_user.id)
    return projects_nav