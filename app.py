import datetime

from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_admin import Admin
from flask_admin.contrib.sqlamodel import ModelView

from data import db_session, olympiads_resource, users_resources
from data.olympiads import Olympiads
from data.users import Users
from data.olympiads_resource import OlympiadsResource, OlympiadsListResource
from data.olympiads_to_subjects import Subjects
from data.olympiads_to_class import SchoolClasses
from data.olympiads_resource import add_olymps_to_database, add_subject_api, delete_subject_api

from forms.user import RegisterForm, LoginForm
from forms.search_olympiads import SearchOlympiadForm

from requests import get, post

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost/main'
api = Api(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

admin = Admin(app, name='Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Olympiads, db.session))
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Subjects, db.session))

SUBJECTS = {'Математика': 1,
            'Информатика': 2,
            'Физика': 1,
            'Химия': 1,
            'Русский язык': 1
            }
ADMINS = ['123@123']


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init()
    # app.register_blueprint(jobs_api.blueprint)
    # app.register_blueprint(user_api.blueprint)
    api.add_resource(users_resources.UsersListResource, '/api/v2/users')
    api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:user_id>')
    api.add_resource(olympiads_resource.OlympiadsListResource, '/api/v2/olympiads')
    api.add_resource(olympiads_resource.OlympiadsResource, '/api/v2/olympiads/<int:olympiad_id>')

    app.run(debug=True)


@app.route("/subjects/<subject>/<school_class>", methods=['GET', 'POST'])
@app.route("/", methods=['POST', 'GET'])
def index(subject=None, school_class=None):
    url_style = url_for('static', filename='css/style.css')

    db_sess = db_session.create_session()
    olympiads = db_sess.query(Olympiads).all()
    school_classes = db_sess.query(SchoolClasses).all()
    form = SearchOlympiadForm()
    form.subject.choices = [(sub, sub) for i, sub in enumerate(['Все предметы'] + list(SUBJECTS.keys()))]
    form.school_class.choices = [(cls, cls) for i, cls in enumerate(['Все классы'] + school_classes)]
    if form.validate_on_submit():
        subs = form.subject.data
        classes = form.school_class.data
        print(subs, classes)
        return redirect(f'/subjects/{subs}/{classes}')
    if subject and subject != 'Все предметы':
        subject = db_sess.query(Subjects).filter(Subjects.name.like(f'%{subject}%')).first()
        olympiads = subject.olympiads if subject is not None else []
    if school_class and school_class != 'Все классы':
        olympiads = list(filter(lambda x:
                                int(school_class) in [int(el.number) for el in x.school_classes], olympiads))

    return render_template("index.html", olympiads=olympiads, url_style=url_style, subjects=SUBJECTS,
                           current_user=current_user, admins=ADMINS, classes=school_classes, form=form)


@app.route("/favorite_olympiads")
def fav_olymps():
    if current_user:
        url_style = url_for('static', filename='css/style.css')
        olympiads = current_user.olympiads
        return render_template("index.html", olympiads=olympiads, url_style=url_style, subjects=SUBJECTS,
                               current_user=current_user, admins=ADMINS)


@app.route("/olympiad/<int:olymp_id>")
def olympiad(olymp_id):
    url_style = url_for('static', filename='css/style.css')
    db_sess = db_session.create_session()
    olympiad = db_sess.query(Olympiads).get(olymp_id)
    stages = olympiad.stages
    return render_template("olympiad.html", olympiad=olympiad, url_style=url_style, admins=ADMINS, stages=stages)


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
#     db_sess = db_session.create_session()
#     olympiads = db_sess.query(Olympiads).all()
#     school_classes = db_sess.query(SchoolClasses).all()
#     form = SearchOlympiadForm()
#     form.subject.choices = [(i, sub) for i, sub in enumerate(list(SUBJECTS.keys()))]
#     form.school_class.choices = [(i, cls) for i, cls in enumerate(school_classes)]
#     if subject != 'all':
#         print(subject)
#         subject = db_sess.query(Subjects).filter(Subjects.name.like(f'%{subject}%')).first()
#         olympiads = subject.olympiads if subject is not None else []
#
#     print(olympiads)
#     return render_template("index.html", olympiads=olympiads, url_style=url_style, subjects=SUBJECTS, form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    url_style = url_for('static', filename='css/style.css')
    form = RegisterForm()
    for field in form:
        print(field.label().striptags())
    if form.validate_on_submit():
        print(post('http://127.0.0.1:5000/api/v2/users',
                   json={'email': form.email.data,
                         'password': form.password.data,
                         'name': form.name.data,
                         'school_class': form.school_class.data}).json())
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.email == form.email.data).first()
        login_user(user)

        return redirect('/')
    return render_template("register.html", url_style=url_style, form=form, authorization='Регистрация')


@app.route("/login", methods=['GET', 'POST'])
def login():
    url_style = url_for('static', filename='css/style.css')
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if user.email in ADMINS: user.is_admin = True
            return redirect("/")
    return render_template("register.html", url_style=url_style, form=form, authorization='Вход',
                           current_user=current_user)


@app.route("/add_user/<int:subj_id>", methods=['GET', 'POST'])
def add_subj(subj_id):
    db_sess = db_session.create_session()
    user = db_sess.query(Users).get(1)
    print(user.olympiads)
    return ','.join(user.olympiads)


@app.route("/add_stage/<int:stage_id>", methods=['GET', 'POST'])
def add_stage(stage_id):
    db_sess = db_session.create_session()
    olymp = db_sess.query(Olympiads).get(2)
    olymp.add_stage(db_sess, 1, datetime.date(year=2010, month=12, day=1))
    return 'ок'


if __name__ == '__main__':
    main()
