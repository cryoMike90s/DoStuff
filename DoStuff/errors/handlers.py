from flask import Blueprint, render_template
from DoStuff.tasks.forms import ProjectForm

errors = Blueprint('errors', __name__)


# @errors.context_processor
# def new_project_temp():
#     new_project_form = ProjectForm()
#     return dict(new_project_form=new_project_form)

@errors.app_errorhandler(404)
def error_404(error):
    new_project_form = ProjectForm()
    return render_template('errors/404.html', new_project_form=new_project_form), 404

@errors.app_errorhandler(403)
def error_403(error):
    new_project_form = ProjectForm()
    return render_template('errors/403.html', new_project_form=new_project_form), 403

@errors.app_errorhandler(405)
def error_403(error):
    new_project_form = ProjectForm()
    return render_template('errors/405.html', new_project_form=new_project_form), 405

@errors.app_errorhandler(500)
def error_500(error):
    new_project_form = ProjectForm()
    return render_template('errors/500.html', new_project_form=new_project_form), 500