from app.models import Projects
from flask_login import current_user


def project_list():
    """
    Utilized by `for` loop in 'sidebar.html' that shows actual list of current project for current user,
    connected with app_context_processor in main.routes
    """
    projects_nav = Projects.query.filter_by(user_id=current_user.id)
    return projects_nav
