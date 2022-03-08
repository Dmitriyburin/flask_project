from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField('Job Title', validators=[DataRequired()])
    # team_leader = IntegerField('Team Leader id', validators=[DataRequired()])
    work_size = IntegerField('Время работы', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')