import sqlalchemy

from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase

olympiads_to_subjects_table = sqlalchemy.Table('olympiads_to_subjects', SqlAlchemyBase.metadata,
                                               sqlalchemy.Column('olympiads', sqlalchemy.Integer,
                                                                 sqlalchemy.ForeignKey('olympiads.id')),
                                               sqlalchemy.Column('subjects', sqlalchemy.Integer,
                                                                 sqlalchemy.ForeignKey('subjects.id'))
                                               )


class Subjects(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'subjects'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(35), nullable=True)
