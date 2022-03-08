from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

from data import db_session, olympiads_resource, users_resources
from data.olympiads import Olympiads
from data.users import User
from data.subjects import Subjects
from data.users_resources import UsersListResource

from forms.user import RegisterForm, LoginForm

from requests import get, post

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)

SUBJECTS = ['Математика', 'Информатика', 'Физика', 'Химия', 'Русский язык']
ADMINS = ['123@123']


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


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


@app.route("/")
def index():
    url_style = url_for('static', filename='css/style.css')
    db_sess = db_session.create_session()
    olympiads = db_sess.query(Olympiads).all()
    return render_template("index.html", olympiads=olympiads, url_style=url_style, subjects=SUBJECTS,
                           current_user=current_user, admins=ADMINS)


@app.route("/olympiad/<int:olymp_id>")
def olympiad(olymp_id):
    url_style = url_for('static', filename='css/style.css')
    db_sess = db_session.create_session()
    olympiad = [db_sess.query(Olympiads).get(olymp_id)]
    return render_template("index.html", olympiads=olympiad, url_style=url_style, subjects=SUBJECTS)


@app.route("/subjects/<subject>")
def subject(subject):
    url_style = url_for('static', filename='css/style.css')
    db_sess = db_session.create_session()
    olympiads = db_sess.query(Olympiads).all()
    if subject != 'all':
        subject_id = db_sess.query(Subjects).filter(Subjects.name == subject).first().id
        olympiads = db_sess.query(Olympiads).filter(Olympiads.subject_id == subject_id).all()
    print(olympiads)
    return render_template("index.html", olympiads=olympiads, url_style=url_style, subjects=SUBJECTS)


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
        return redirect('/')
    return render_template("register.html", url_style=url_style, form=form, authorization='Регистрация')


@app.route("/login", methods=['GET', 'POST'])
def login():
    url_style = url_for('static', filename='css/style.css')
    form = LoginForm()

    if form.validate_on_submit():

        db_sess = db_session.create_session()
        print(form.email)
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(user, form.password, user.check_password(password=form.password.data))
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
    return render_template("register.html", url_style=url_style, form=form, authorization='Вход',
                           current_user=current_user)


if __name__ == '__main__':
    main()
