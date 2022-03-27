from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SearchField, BooleanField, SelectField
from wtforms.validators import DataRequired


class SearchOlympiadForm(FlaskForm):
    subject = SelectField('Предмет', coerce=str)
    school_class = SelectField('Школьный класс')
    title = SearchField('Название')
    submit = SubmitField('Submit')
