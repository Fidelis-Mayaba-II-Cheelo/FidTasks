from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateTimeField
from wtforms.validators import DataRequired, Length

class CreateGoalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=10)])
    description = StringField('Description', validators=[DataRequired(), Length(min=10, max=200)])
    category = SelectField('Category', choices=['Work', 'Personal', 'Errands'])
    priority = SelectField('Priority', choices=['Very High', 'High', 'Medium', 'Low', 'Very Low'])
    status = SelectField('Status', choices=['Pending', 'In-Progress'])
    deadline = DateTimeField('Deadline', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField("Create Goal")


class UpdateGoalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=10)])
    description = StringField('Description', validators=[DataRequired(), Length(min=10, max=200)])
    category = SelectField('Category', choices=['Work', 'Personal', 'Errands'])
    priority = SelectField('Priority', choices=['Very High', 'High', 'Medium', 'Low', 'Very Low'])
    status = SelectField('Status', choices=['Pending', 'In-Progress', 'Completed'])
    deadline = DateTimeField('Deadline', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField("Update Goal")

