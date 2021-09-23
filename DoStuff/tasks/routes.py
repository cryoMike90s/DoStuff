from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from DoStuff.models import Projects, Tasks
from flask_login import current_user
from DoStuff.tasks.forms import ProjectForm, TaskForm
from DoStuff import db

from flask_login import login_required

tasks = Blueprint('tasks', __name__)


@tasks.route('/project/new2', methods=['POST'])
@login_required
def new_project_2():
    new_project_form = ProjectForm()
    project = Projects(project_name=new_project_form.project_name.data, owner=current_user)
    db.session.add(project)
    db.session.commit()
    flash("Project successfully created !", 'success')

    return redirect(url_for('main.home'))


@tasks.route('/home/<int:project_id>')
@login_required
def specific_project(project_id):
    """
    Main function for view project panel, variable instances added, to make possible updating, creating or deleting
     projects and tasks
     Args:
        project_id (int): value for dynamic parameter, we expect number so that's why int, bounded with Project class
    """
    project_number = Projects.query.get_or_404(project_id)

    if project_number.owner != current_user:  # owner is backref for relationship btw. User and Projects classes
        abort(403)
    form = TaskForm()  # form for new task (add_task)
    form_update = ProjectForm()  # form for update existing project (update_project)
    task_form_update = TaskForm()
    new_project_form = ProjectForm()
    tasks = Tasks.query.filter_by(project_parent=project_id)

    return render_template('project_and_tasks.html',
                           project_number=project_number,
                           tasks=tasks,
                           form=form,
                           form_update=form_update,
                           task_form_update=task_form_update,
                           new_project_form=new_project_form)


@tasks.route('/home/<int:project_id>/update', methods=['POST'])
@login_required
def update_project(project_id):
    """
    Basic function for update name od project, project_id as argument in url_for() allows for redirect
    to updated project by number
    """
    form_update = ProjectForm()
    project_number = Projects.query.get_or_404(project_id)
    project_number.project_name = form_update.project_name.data
    db.session.commit()
    flash("Project successfully updated !", 'success')

    return redirect(url_for('tasks.specific_project', project_id=str(project_number.id)))


@tasks.route('/home/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    spec_project = Projects.query.get_or_404(project_id)
    db.session.delete(spec_project)
    db.session.commit()
    flash('Project has been deleted!', 'success')

    return redirect(url_for('main.home'))


@tasks.route('/home/<int:project_id>/new_task', methods=['POST'])
@login_required
def add_task(project_id):
    form = TaskForm()
    project_number = Projects.query.get_or_404(project_id)
    task = Tasks(task_name=form.task_name.data, content=form.content.data, parent=project_number)
    db.session.add(task)
    db.session.commit()
    flash("Task successfully added !", 'success')

    return redirect(url_for('tasks.specific_project', project_id=str(project_number.id)))


@tasks.route('/home/<int:task_id>/delete_task', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Tasks.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    project_number = Projects.query.get_or_404(task.project_parent)
    flash('Task has been deleted!', 'success')

    return redirect(url_for('tasks.specific_project', project_id=str(project_number.id)))


@tasks.route('/<int:task_id>/update', methods=['POST', 'GET'])
@login_required
def update_task(task_id):
    """
    Function connected with modal function in 'project_and_tasks.html', current content is automatically assigned
    to forms field (GET request statement), and could be modified that's why if statement
    """
    task_form_update = TaskForm()
    task = Tasks.query.get_or_404(task_id)
    project_number = Projects.query.get_or_404(task.project_parent)

    if request.method == 'POST':
        task.task_name = task_form_update.task_name.data
        task.content = task_form_update.content.data
        db.session.commit()
        flash("Task successfully updated !", 'success')

        return redirect(url_for('tasks.specific_project', project_id=str(project_number.id)))

    elif request.method == 'GET':
        task_form_update.task_name.data = task.task_name
        task_form_update.task_content.data = task.content

        return redirect(url_for('tasks.specific_project', project_id=str(project_number.id)))
