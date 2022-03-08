from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class OlympiadForm(FlaskForm):
    job = StringField('Job Title', validators=[DataRequired()])
    # team_leader = IntegerField('Team Leader id', validators=[DataRequired()])
    subject_id = IntegerField('Предмет', validators=[DataRequired()])
    title = StringField('Название', validators=[DataRequired()])
    school_class = StringField('Класс/Классы', validators=[DataRequired()])
    description = StringField('Продолжительность', validators=[DataRequired()])
    link = StringField('Ссылка на источник', validators=[DataRequired()])
    data = StringField('Дата проведения', validators=[DataRequired()])

    submit = SubmitField('Submit')
