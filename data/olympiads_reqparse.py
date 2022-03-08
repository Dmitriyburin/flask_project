from flask_restful import reqparse

parser = reqparse.RequestParser()
# parser.add_argument('subject_id', required=True, type=int)
parser.add_argument('title', required=True)
parser.add_argument('school_class', required=True, type=int)
parser.add_argument('description', required=True)
parser.add_argument('duration', required=True, type=int)
parser.add_argument('link', required=True)
parser.add_argument('date')

"""subject = sqlalchemy.Column(sqlalchemy.String(35), nullable=True)
    title = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    school_class = sqlalchemy.Column(sqlalchemy.String(35), nullable=True)
    description = sqlalchemy.Column(sqlalchemy.Text, default=datetime.datetime.now)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    link = sqlalchemy.Column(sqlalchemy.String(35), nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String(35), nullable=True)
"""