from flask import Blueprint, render_template
from app.tasks.forms import ProjectForm
from flask_login import current_user

errors = Blueprint('errors', __name__)



@errors.app_errorhandler(404)
def error_404(error):
    new_project_form = ProjectForm()
    if current_user.is_authenticated:
        return render_template('errors/404.html', new_project_form=new_project_form), 404
    else:
        return render_template('errors/404_anon.html', new_project_form=new_project_form), 404

@errors.app_errorhandler(403)
def error_403(error):
    new_project_form = ProjectForm()
    if current_user.is_authenticated:
        return render_template('errors/403.html', new_project_form=new_project_form), 403
    else:
        return render_template('errors/403_anon.html', new_project_form=new_project_form), 403

@errors.app_errorhandler(405)
def error_403(error):
    new_project_form = ProjectForm()
    if current_user.is_authenticated:
        return render_template('errors/405.html', new_project_form=new_project_form), 405
    else:
        return render_template('errors/405_anon.html', new_project_form=new_project_form), 405


@errors.app_errorhandler(500)
def error_500(error):
    new_project_form = ProjectForm()
    if current_user.is_authenticated:
        return render_template('errors/500.html', new_project_form=new_project_form), 500
    else:
        return render_template('errors/500_anon.html', new_project_form=new_project_form), 500
