from flask import jsonify
from flask_restful import abort, Resource

from . import db_session
from .jobs import Jobs
from .jobs_reqparse import parser


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"User {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()

        job = session.query(Jobs).get(job_id)
        return jsonify(
            {'jobs': job.to_dict(only=('id', 'team_leader', 'job', 'work_size',
                                       'collaborators', 'start_date', 'is_finished'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify(
            {'jobs': [
                item.to_dict(only=('id', 'team_leader', 'job', 'work_size',
                                   'collaborators', 'start_date', 'is_finished')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )

        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})
