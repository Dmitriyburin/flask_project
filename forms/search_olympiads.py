from flask_wtf import FlaskForm
from wtforms import widgets, SubmitField, SearchField, DateField, SelectField, BooleanField
from wtforms.validators import DataRequired
import datetime


class SearchOlympiadForm(FlaskForm):
    subject = SelectField('Предмет', coerce=str)
    school_class = SelectField('Школьный класс')
    title = SearchField('Название')
    date = DateField('Дата', default=datetime.datetime.now)
    date_option = BooleanField('Использовать дату')
    submit = SubmitField('Submit')

