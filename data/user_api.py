import flask
from flask import request, jsonify, render_template

from . import db_session
from .jobs import Jobs
from .users import User

blueprint = flask.Blueprint('user_api', __name__, template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {'users': [
            item.to_dict(only=('id', 'surname', 'name', 'age',
                               'position', 'speciality', 'address', 'email', 'modified_date')) for item in users]})


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {'user': user.to_dict(only=('id', 'surname', 'name', 'age',
                                    'position', 'speciality', 'address', 'email', 'modified_date'))})


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position',
                  'speciality', 'address', 'email']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    exist_id = db_sess.query(User).get(request.json['id'])

    if exist_id:
        return jsonify({'error': 'Id already exists'})

    user = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],

    )
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['PUT'])
def users(users_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})

    db_sess = db_session.create_session()
    exist_id = db_sess.query(User).get(users_id)
    if not exist_id:
        return jsonify({'error': 'Bad request'})

    user = db_sess.query(User).get(users_id)
    user.id = request.json.get('id', user.id)
    user.surname = request.json.get('surname', user.surname)
    user.name = request.json.get('name', user.name)
    user.age = request.json.get('age', user.age)
    user.position = request.json.get('position', user.position)
    user.speciality = request.json.get('speciality', user.speciality)
    user.address = request.json.get('address', user.address)
    user.email = request.json.get('email', user.email)

    db_sess.add(user)
    db_sess.commit()

    return jsonify({'success': 'OK'})
