from flask import Blueprint, render_template
from flask_login import login_required

#creation of Blueprint instance, similar to app = Flask(__main__)
main = Blueprint('main', __name__)



@main.route('/home')
@login_required
def home():
    return render_template('home.html', title="Home")