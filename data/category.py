import sqlalchemy

from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase

association_table = sqlalchemy.Table('association', SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('olympiads', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('olympiads.id')),
                                     sqlalchemy.Column('subjects', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('subjects.id'))
                                     )


class Subjects(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'subjects'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(35), nullable=True)
