from flask import Blueprint, render_template, redirect, url_for, request
from DoStuff.models import User, Projects, Tasks
from flask_login import current_user
from DoStuff.tasks.forms import ProjectForm, TaskForm
from DoStuff import db
from DoStuff.tasks.utilis import project_list

tasks = Blueprint('tasks', __name__)


@tasks.route('/home/projects')
def projects():
    projects = Projects.query.filter_by(user_id=current_user.id).all()
    return render_template('projects_and_tasks.html', projects=projects)


@tasks.route('/project/new',  methods=['GET', 'POST'])
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Projects(project_name=form.project_name.data, owner=current_user)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('new_project.html', form=form)


@tasks.route('/home/<int:project_id>')
def specific_project(project_id):
    form = TaskForm()
    project_number = Projects.query.get_or_404(project_id)
    tasks = Tasks.query.filter_by(project_parent=project_id)
    return render_template('project_and_tasks.html', project_number=project_number, project_list=project_list(), tasks=tasks, form=form)


# @tasks.route('/home/<int:project_id>/new_task', methods=['GET', 'POST'])
# def new_task(project_id):
#     form = TaskForm()
#     project_number = Projects.query.get_or_404(project_id)
#     if form.validate_on_submit():
#         task = Tasks(task_name=form.task_name.data, content=form.content.data, parent=project_number)
#         db.session.add(task)
#         db.session.commit()
#         return redirect(url_for('main.home'))
#     return render_template('new_task.html', form=form, project_number=project_number,  project_list=project_list())


@tasks.route('/home/<int:project_id>/new_task', methods=['POST'])
def add_task(project_id):
    form = TaskForm()
    project_number = Projects.query.get_or_404(project_id)
    if request.method == 'POST':
        task = Tasks(task_name=form.task_name.data, content=form.content.data, parent=project_number)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks.specific_project', project_id=str(project_number.id)))





@tasks.route('/home/<int:task_id>/delete_task', methods=['POST'])
def delete_task(task_id):
    task = Tasks.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    project_number = Projects.query.get_or_404(task.project_parent)
    return redirect(url_for('tasks.specific_project', project_id=str(project_number.id)))





