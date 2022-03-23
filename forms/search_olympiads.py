from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired


class SearchOlympiadForm(FlaskForm):
    subject = SelectField('Предмет', coerce=str)
    school_class = SelectField('Школьный класс')
    submit = SubmitField('Submit')
