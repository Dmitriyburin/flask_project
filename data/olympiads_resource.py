from flask import jsonify, request
from flask_restful import abort, Resource

from . import db_session
from .olympiads import Olympiads
from .olympiads_reqparse import parser


def abort_if_olympiad_not_found(olympiad_id):
    session = db_session.create_session()
    olympiad = session.query(Olympiads).get(olympiad_id)
    if not olympiad:
        abort(404, message=f"Olympiad {olympiad_id} not found")


class OlympiadsResource(Resource):
    def get(self, olympiad_id):
        abort_if_olympiad_not_found(olympiad_id)
        session = db_session.create_session()

        olympiad = session.query(Olympiads).get(olympiad_id)
        return jsonify(
            {'olympiads': olympiad.to_dict(only=('id', 'subject'))})

    def delete(self, olympiad_id):
        abort_if_olympiad_not_found(olympiad_id)
        session = db_session.create_session()
        olympiad = session.query(Olympiads).get(olympiad_id)
        session.delete(olympiad)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, olympiad_id):
        abort_if_olympiad_not_found(olympiad_id)
        session = db_session.create_session()

        olympiad = session.query(Olympiads).get(olympiad_id)
        olympiad.id = request.json.get('id', olympiad.id)
        olympiad.title = request.json.get('title', olympiad.title)
        olympiad.school_class = request.json.get('school_class', olympiad.school_class)
        olympiad.description = request.json.get('description', olympiad.description)
        olympiad.duration = request.json.get('duration', olympiad.duration)
        olympiad.link = request.json.get('link', olympiad.link)
        olympiad.date = request.json.get('date', olympiad.date)

        session.commit()
        return jsonify({'success': 'OK'})


class OlympiadsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        olympiads = session.query(Olympiads).all()
        return jsonify(
            {'olympiads': [
                item.to_dict(only=('id', 'subject')) for item in olympiads]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        print(args)
        job = Olympiads(
            subject_id=args['subject_id'],
            title=args['title'],
            school_class=args['school_class'],
            description=args['description'],
            duration=args['duration'],
            link=args['link'],
            date=args['date']
        )



        print(session.add(job))
        session.commit()
        return jsonify({'success': 'OK'})


"""
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
"""
