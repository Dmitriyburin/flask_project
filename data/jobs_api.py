import flask
from flask import request, jsonify, render_template

from . import db_session
from .jobs import Jobs
from .news import News

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_job():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {'jobs': [
            item.to_dict(only=('id', 'team_leader', 'job', 'work_size',
                               'collaborators', 'start_date', 'is_finished')) for item in jobs]})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_job(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(jobs_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {'jobs': job.to_dict(only=('id', 'team_leader', 'job', 'work_size',
                                   'collaborators', 'start_date', 'is_finished'))})


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size',
                  'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    exist_id = db_sess.query(Jobs).get(request.json['id'])

    if exist_id:
        return jsonify({'error': 'Id already exists'})

    job = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )

    db_sess.add(job)
    db_sess.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/job/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def change_jobs(jobs_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})

    db_sess = db_session.create_session()
    exist_id = db_sess.query(Jobs).get(jobs_id)
    if not exist_id:
        return jsonify({'error': 'Bad request'})

    job = db_sess.query(Jobs).get(jobs_id)
    job.id = request.json.get('id', job.id)
    job.team_leader = request.json.get('team_leader', job.team_leader)
    job.job = request.json.get('job', job.job)
    job.work_size = request.json.get('work_size', job.work_size)
    job.collaborators = request.json.get('collaborators', job.collaborators)
    job.is_finished = request.json.get('is_finished', job.is_finished)

    db_sess.add(job)
    db_sess.commit()

    return jsonify({'success': 'OK'})
