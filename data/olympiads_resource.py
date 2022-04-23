import asyncio
import datetime
from flask import jsonify, request
from flask_restful import abort, Resource

from . import db_session
from .olympiads import Olympiads
from .olympiads_reqparse import parser
from .olympiads_to_subjects import Subjects, olympiads_to_subjects
from .olympiads_to_class import SchoolClasses
from .olympiads_to_stages import Stages
from .parser import main
from pprint import pprint


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
        olymp = Olympiads(
            title=args['title'],
            school_class=args['school_class'],
            description=args['description'],
            duration=args['duration'],
            link=args['link'],
            date=args['date']
        )

        print(session.add(olymp))
        session.commit()
        return jsonify({'success': 'OK'})


async def add_olymps_to_database(session):
    olymps = await main()

    count_success = 0
    for olymp_dict in olymps:
        print(olymp_dict)
        try:
            links = olymp_dict['links']
            olymp = Olympiads(
                title=olymp_dict['title'],
                # school_class=', '.join(olymp_dict['school_class']),
                description=olymp_dict['history'],
                link=links.get('Сайт', 'ссылка'),
            )
            for sub in olymp_dict['subject']:

                subject = session.query(Subjects).filter(Subjects.name.like(f'%{sub.lower()}%')).first()
                if subject:
                    olymp.subjects.append(subject)
            if not len(olymp.subjects):
                print('ASOKFJKJDFHPOJF')
                continue

            school_classes = [session.query(SchoolClasses).filter(SchoolClasses.number == sch_cl).first()
                              for sch_cl in range(olymp_dict['school_class'][0], olymp_dict['school_class'][-1] + 1)]
            for school_class in school_classes:
                olymp.school_classes.append(school_class)

            for stage_info in olymp_dict['stages']:
                stage = Stages(
                    name=stage_info['name'],
                    date=stage_info['date'][0]
                )
                olymp.stages.append(stage)

            session.add(olymp)
            session.commit()
            count_success += 1
            print(count_success)
        except Exception as e:
            print(e)
            session.rollback()
            continue


def add_subject_api(olympiad_id, subject_id):
    abort_if_olympiad_not_found(olympiad_id)
    session = db_session.create_session()

    olympiad = session.query(Olympiads).get(olympiad_id)
    subject = session.query(Subjects).get(subject_id)

    olympiad.subjects.append(subject)
    session.commit()
    return jsonify({'success': 'OK'})


def delete_subject_api(olympiad_id, subject_id):
    abort_if_olympiad_not_found(olympiad_id)
    session = db_session.create_session()

    olympiad = session.query(Olympiads).get(olympiad_id)
    subject = session.query(Subjects).get(subject_id)

    olympiad.subjects.remove(subject)
    session.commit()
    return jsonify({'success': 'OK'})


def add_olympiad(session):
    try:
        olymp = Olympiads(
            title='Пример загаловка олимпиады',
            # school_class=', '.join(olymp_dict['school_class']),
            description='Описание и история олимпиады',
            link='ссылка на олимпиаду',
        )
        olymp.school_classes.append(session.query(SchoolClasses).filter(SchoolClasses.number == 1).first())
        stage = Stages(
            name='Имя этапа',
            date=datetime.date(2025, 1, 1),
        )
        olymp.stages.append(stage)
        session.add(olymp)
        session.commit()
        return jsonify({'response': 200, 'success': 'OK', 'olympiad_id': olymp.id})
    except Exception as e:
        print()
        return jsonify({'response': 0, 'error': str(e)})


if __name__ == '__main__':
    add_olymps_to_database()

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
