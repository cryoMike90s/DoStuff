from flask import Blueprint, render_template
from flask_login import login_required
from DoStuff.models import Projects
from flask_login import current_user
from DoStuff.tasks.utilis import project_list


#creation of Blueprint instance, similar to app = Flask(__main__)
main = Blueprint('main', __name__)


#ZROBIĆ GLOBALNA FUNKCJE, KTÓRA BEDZIE DOSTĘPNA DLA KAŻDEJ ROUTY



@main.route('/home')
@login_required
def home():
    projects_nav = Projects.query.filter_by(user_id=current_user.id)
    return render_template('home.html', title="Home", project_list=project_list())


