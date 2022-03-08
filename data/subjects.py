import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Subjects(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'subjects'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    # team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)
    # team_lead = orm.relation('User')

    name = sqlalchemy.Column(sqlalchemy.String(35), nullable=True)
    olympiads = orm.relation("Olympiads", back_populates='subject')