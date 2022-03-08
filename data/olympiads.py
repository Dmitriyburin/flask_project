import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Olympiads(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'olympiads'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    # team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)
    # team_lead = orm.relation('User')

    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subjects.id"), nullable=True)
    subject = orm.relation('Subjects')

    title = sqlalchemy.Column(sqlalchemy.String(35), nullable=True)
    school_class = sqlalchemy.Column(sqlalchemy.String(35), nullable=True)
    description = sqlalchemy.Column(sqlalchemy.Text)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    link = sqlalchemy.Column(sqlalchemy.String(35), nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String(35), nullable=True, default=datetime.date.today())

