# /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import asyncio
import gunicorn
from celery import Celery

from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_paginate import Pagination, get_page_parameter

from flask_admin import Admin, expose, AdminIndexView, helpers
from flask_admin.contrib.sqlamodel import ModelView

from data.config import USER, PASSWORD, HOST, PORT, DATABASE
from data import db_session, olympiads_resource, users_resources
from data.olympiads import Olympiads
from data.users import Users
from data.olympiads_resource import OlympiadsResource, OlympiadsListResource
from data.olympiads_to_subjects import Subjects
from data.olympiads_to_class import SchoolClasses
from data.olympiads_to_stages import Stages
from data.olympiads_resource import add_olymps_to_database, add_subject_api, delete_subject_api
from data.users_resources import registration

from forms.user import RegisterForm, LoginForm
from forms.search_olympiads import SearchOlympiadForm

from requests import get, post


def process_http_request(environ, start_response):
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain; charset=utf-8'),
    ]
    start_response(status, response_headers)
    text = 'Here be dragons'.encode('utf-8')
    return [text]


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(
    USER, PASSWORD, HOST, DATABASE)
api = Api(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

ADMINS = ['123@123']


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect('/login')
        if current_user.email not in ADMINS:
            return redirect('/')
        return super(MyAdminIndexView, self).index()


admin = Admin(app, name='Admin', index_view=MyAdminIndexView(), template_mode='bootstrap3',
              base_template='my_master.html')
admin.add_view(ModelView(Olympiads, db.session))
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Subjects, db.session))
admin.add_view(ModelView(Stages, db.session))

SUBJECTS = {'Математика': 1,
            'Информатика': 2,
            'Физика': 1,
            'Химия': 1,
            'Русский язык': 1
            }


def main():
    # app.register_blueprint(jobs_api.blueprint)
    # app.register_blueprint(user_api.blueprint)
    api.add_resource(users_resources.UsersListResource, '/api/v2/users')
    api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:user_id>')
    api.add_resource(olympiads_resource.OlympiadsListResource, '/api/v2/olympiads')
    api.add_resource(olympiads_resource.OlympiadsResource, '/api/v2/olympiads/<int:olympiad_id>')

    app.run(debug=True)


@app.route("/favourite_olympiads", methods=['GET', 'POST'])
@app.route("/filters/<subject>/<school_class>/", methods=['GET', 'POST'])
@app.route("/filters/<subject>/<school_class>/<title>", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def index(subject=None, school_class=None, title=None):
    PER_PAGE = 10
    favourite = False
    modal = False

    url_style = url_for('static', filename='css/style.css')
    url_logo = url_for('static', filename='img/logo.jpg')

    print(db.session)
    subjects = [sub.name for sub in db.session.query(Subjects).all()]

    school_classes = db.session.query(SchoolClasses).all()

    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    olympiads = db.session.query(Olympiads).all()
    olympiads = sorted(olympiads, key=lambda olymp: olymp.stages[0].date, reverse=True)

    form = SearchOlympiadForm()
    form.subject.choices = [(sub, sub) for i, sub in enumerate(['Все предметы'] + subjects)]
    form.school_class.choices = [(cls, cls) for i, cls in enumerate(['Все классы'] + school_classes)]

    if request.method == 'POST':
        if form.validate_on_submit():
            subs = form.subject.data
            classes = form.school_class.data
            title = form.title.data if form.title.data is not None else ''
            return redirect(f'/filters/{subs}/{classes}/{title}')
        elif form.title.data:
            subs = "Все предметы"
            classes = "Все классы"
            title = form.title.data if form.title.data is not None else ''
            return redirect(f'/filters/{subs}/{classes}/{title}')

    if request.path == '/favourite_olympiads':
        if current_user.is_authenticated:
            favourite = True
            olympiads = current_user.olympiads
        else:
            print('пользователь не зарегистрирован')

    if title:
        olympiads = db.session.query(Olympiads).filter(Olympiads.title.like(f'%{title}%')).all()

    if subject and subject != 'Все предметы':
        subject = db.session.query(Subjects).filter(Subjects.name.like(f'%{subject}%')).first()
        olympiads = subject.olympiads if subject is not None else []

    if school_class and school_class != 'Все классы':
        olympiads = list(filter(lambda x:
                                int(school_class) in [int(el.number) for el in x.school_classes], olympiads))

    pagination = Pagination(page=page, total=len(olympiads))
    olympiads = olympiads[start:end]
    return render_template("index.html", olympiads=olympiads, url_style=url_style, subjects=subjects,
                           current_user=current_user, admins=ADMINS, classes=school_classes, form=form,
                           favourite=favourite, pagination=pagination, url_logo=url_logo, modal=modal,
                           datetime=datetime.datetime)


@app.route("/favourite_olympiads")
def fav_olymps():
    if current_user.is_authenticated:
        form = SearchOlympiadForm()

        if request.method == 'POST':
            if form.title.data:
                subs = "Все предметы"
                classes = "Все классы"
                title = form.title.data
                return redirect(f'/filters/{subs}/{classes}/{title}')

        url_style = url_for('static', filename='css/style.css')
        url_logo = url_for('static', filename='img/logo.jpg')

        olympiads = current_user.olympiads
        return render_template("index.html", olympiads=olympiads, url_style=url_style, subjects=SUBJECTS,
                               current_user=current_user, admins=ADMINS, favourite=True, url_logo=url_logo, form=form)


@app.route("/olympiad/<int:olymp_id>/delete-stage/<int:stage_id>", methods=['GET', 'POST'])
@app.route("/olympiad/<int:olymp_id>", methods=['GET', 'POST'])
def olympiad(olymp_id, stage_id=None):
    olympiad = db.session.query(Olympiads).get(olymp_id)
    favourites = None
    form = SearchOlympiadForm()

    if current_user.is_authenticated:
        favourites = [i.id for i in current_user.olympiads]

    if request.path == f'/olympiad/{olymp_id}/delete-stage/{stage_id}':
        stage = db.session.query(Stages).filter_by(id=stage_id).first()
        db.session.delete(stage)
        db.session.commit()
        return redirect(f'/olympiad/{olymp_id}')

    if request.method == 'POST':
        if form.title.data:
            subs = "Все предметы"
            classes = "Все классы"
            title = form.title.data
            return redirect(f'/filters/{subs}/{classes}/{title}')

        if request.form['submit_button'] == 'Добавить в избранные':
            user = db.session.query(Users).filter(Users.email == current_user.email).first()
            user.olympiads.append(olympiad)
            db.session.commit()
        if request.form['submit_button'] == 'Удалить из избранных':
            user = db.session.query(Users).filter(Users.email == current_user.email).first()
            user.olympiads.remove(olympiad)
            db.session.commit()
        if request.form['submit_button'] == 'Добавить':
            stage = Stages(
                name='Этап',
                olympiad_id=olympiad.id
            )
            db.session.add(stage)
            db.session.commit()
        # if request.form['submit_button'] == 'Удалить':

        return redirect(f'/olympiad/{olymp_id}')

    olympiad.stages.sort(key=lambda x: x.date)
    stages = list(reversed(olympiad.stages))
    url_style = url_for('static', filename='css/style.css')
    url_logo = url_for('static', filename='img/logo.jpg')
    return render_template("olympiad.html", olympiad=olympiad, url_style=url_style, admins=ADMINS, stages=stages,
                           favourites=favourites, url_logo=url_logo, datetime=datetime.datetime, form=form)


@app.route('/process_data/<int:index>/', methods=['POST'])
def doit(index):
    if index == 1:
        print('УДАЛИТЬ ОЛИМПИАДУ')
    if index == 2:
        print('УДАЛИТЬ ОЛИМПИАДУ')

    return 'ок'


# @app.route("/subjects/<subject>", methods=['GET', 'POST'])
# def subject(subject):
#     url_style = url_for('static', filename='css/style.css')
#     db.session = db.sessionion.create_session()
#     olympiads = db.session.query(Olympiads).all()
#     school_classes = db.session.query(SchoolClasses).all()
#     form = SearchOlympiadForm()
#     form.subject.choices = [(i, sub) for i, sub in enumerate(list(SUBJECTS.keys()))]
#     form.school_class.choices = [(i, cls) for i, cls in enumerate(school_classes)]
#     if subject != 'all':
#         print(subject)
#         subject = db.session.query(Subjects).filter(Subjects.name.like(f'%{subject}%')).first()
#         olympiads = subject.olympiads if subject is not None else []
#
#     print(olympiads)
#     return render_template("index.html", olympiads=olympiads, url_style=url_style, subjects=SUBJECTS, form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    url_style = url_for('static', filename='css/style.css')
    url_logo = url_for('static', filename='img/logo.jpg')

    form_login = RegisterForm()
    form = SearchOlympiadForm()

    if request.method == 'POST':
        if form.title.data:
            subs = "Все предметы"
            classes = "Все классы"
            title = form.title.data
            return redirect(f'/filters/{subs}/{classes}/{title}')

        if form_login.validate_on_submit():
            json_conf = {'email': form_login.email.data,
                         'password': form_login.password.data,
                         'name': form_login.name.data,
                         'school_class': form.school_class.data}
            response = registration(json_conf, db.session)
            user = db.session.query(Users).filter(Users.email == form_login.email.data).first()
            login_user(user)
            return redirect('/')
    return render_template("register.html", url_style=url_style, form_login=form_login, authorization='Регистрация',
                           url_logo=url_logo, form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    url_style = url_for('static', filename='css/style.css')
    url_logo = url_for('static', filename='img/logo.jpg')
    form_login = LoginForm()
    form = SearchOlympiadForm()
    if request.method == 'POST':
        if form.title.data:
            subs = "Все предметы"
            classes = "Все классы"
            title = form.title.data
            return redirect(f'/filters/{subs}/{classes}/{title}')

        if form_login.validate_on_submit():
            user = db.session.query(Users).filter(Users.email == form_login.email.data).first()
            if user and user.check_password(form_login.password.data):
                login_user(user, remember=form_login.remember_me.data)
                if user.email in ADMINS: user.is_admin = True
                return redirect("/")
    return render_template("register.html", url_style=url_style, form_login=form_login, authorization='Вход',
                           current_user=current_user, url_logo=url_logo, form=form)


def parse_olympiads():
    asyncio.run(add_olymps_to_database())


@app.route("/add_user/<int:subj_id>", methods=['GET', 'POST'])
def add_subj(subj_id):
    user = db.session.query(Users).get(1)
    print(user.olympiads)
    return ','.join(user.olympiads)


@app.route("/add_stage/<int:stage_id>", methods=['GET', 'POST'])
def add_stage(stage_id):
    olymp = db.session.query(Olympiads).get(2)
    olymp.add_stage(db.session, 1, datetime.date(year=2010, month=12, day=1))
    return 'ок'


if __name__ == '__main__':
    main()
