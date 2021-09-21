from flask import Blueprint, render_template
from flask_login import login_required
from DoStuff.tasks.utilis import project_list
from DoStuff.tasks.forms import ProjectForm



#creation of Blueprint instance, similar to app = Flask(__main__)
main = Blueprint('main', __name__)



@main.app_context_processor
def inject_to_all():
    return dict(project_list = project_list)


@main.route('/home')
@login_required
def home():
    new_project_form = ProjectForm()
    return render_template('home.html', title="Home", new_project_form=new_project_form)


