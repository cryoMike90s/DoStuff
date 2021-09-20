from flask import Blueprint, render_template, redirect, url_for, request
from DoStuff.models import User, Projects, Tasks
from flask_login import current_user
from DoStuff.tasks.forms import ProjectForm, TaskForm
from DoStuff import db
from DoStuff.tasks.utilis import project_list

tasks = Blueprint('tasks', __name__)


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
    form_update = ProjectForm()
    task_form_update = TaskForm()
    project_number = Projects.query.get_or_404(project_id)
    tasks = Tasks.query.filter_by(project_parent=project_id)
    return render_template('project_and_tasks.html',
                           project_number=project_number,
                           project_list=project_list(),
                           tasks=tasks,
                           form=form,
                           form_update=form_update,
                           task_form_update=task_form_update)


@tasks.route('/home/<int:project_id>/update', methods=['POST'])
def update_project(project_id):
    form_update = ProjectForm()
    pec_project = Projects.query.get_or_404(project_id)
    pec_project.project_name = form_update.project_name.data
    db.session.commit()
    return redirect(url_for('tasks.specific_project', project_id=str(pec_project.id)))




@tasks.route('/home/<int:project_id>/delete', methods=['POST'])
def delete_project(project_id):
    spec_project = Projects.query.get_or_404(project_id)
    db.session.delete(spec_project)
    db.session.commit()
    return redirect(url_for('main.home'))


@tasks.route('/home/<int:project_id>/new_task', methods=['POST'])
def add_task(project_id):
    form = TaskForm()
    project_number = Projects.query.get_or_404(project_id)
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


@tasks.route('/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    task_form_update = TaskForm()
    task = Tasks.query.get_or_404(task_id)
    project_number = Projects.query.get_or_404(task.project_parent)
    task.task_name = task_form_update.task_name.data
    task.content = task_form_update.content.data
    db.session.commit()
    return redirect(url_for('tasks.specific_project', project_id=str(project_number.id)))




