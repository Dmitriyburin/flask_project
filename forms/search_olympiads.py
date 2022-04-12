from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SearchField, DateField, SelectField
from wtforms.validators import DataRequired
import datetime


class SearchOlympiadForm(FlaskForm):
    subject = SelectField('Предмет', coerce=str)
    school_class = SelectField('Школьный класс')
    title = SearchField('Название')
    date = DateField('Дата', default=datetime.datetime.now)
    submit = SubmitField('Submit')
