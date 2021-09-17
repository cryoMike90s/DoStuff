from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    submit = SubmitField('Post')


class TaskForm(FlaskForm):
    task_name = StringField('Task Name', validators=[DataRequired()])
    content = StringField('Task', validators=[DataRequired()])
    add = SubmitField('Add')