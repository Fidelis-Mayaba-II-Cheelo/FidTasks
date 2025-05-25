from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateTimeField
from wtforms.validators import DataRequired, Length

class AddTasksForm(FlaskForm):
    goal = SelectField('Goal', choices=[] ,validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=10)])
    description = StringField('Description', validators=[DataRequired(), Length(min=10, max=200)])
    priority = SelectField('Priority', choices=['Very High', 'High', 'Medium', 'Low', 'Very Low'])
    status = SelectField('Status', choices=['Pending', 'In-Progress'])
    start_date = DateTimeField('Start Date', format='%Y-%m-%d %H:%M:%S', render_kw={'readonly': True})
    deadline = DateTimeField('Deadline', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField("Add Task")

class UpdateTasksForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=10)])
    description = StringField('Description', validators=[DataRequired(), Length(min=10, max=200)])
    priority = SelectField('Priority', choices=['Very High', 'High', 'Medium', 'Low', 'Very Low'])
    status = SelectField('Status', choices=['Pending', 'In-Progress', 'Completed'])
    deadline = DateTimeField('Deadline', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField("Update Task")