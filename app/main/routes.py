from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.tasks.utils import project_list
from app.tasks.forms import ProjectForm



#creation of Blueprint instance, similar to app = Flask(__main__)
main = Blueprint('main', __name__)





@main.app_context_processor
def inject_to_all():
    """
     Inject list of current user projects for loop on sidebar, 'app_context_processor' allow to write code once
    for all existing routes
    """
    return dict(project_list=project_list)


@main.route('/')
def redirect_route():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    else:
        return redirect(url_for('users.login'))


@main.route('/home')
@login_required
def home():
    """ Home landing page for authenticated user, 'new_project_form' is instance of ProjectForm() comes from creting
        new project"""
    new_project_form = ProjectForm()
    return render_template('home.html', title="Home", new_project_form=new_project_form)


