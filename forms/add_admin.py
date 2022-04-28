from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class AddOlympForm(FlaskForm):
    email = StringField('Email пользователя', validators=[DataRequired()])
    submit = SubmitField('Submit')