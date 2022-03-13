import sqlalchemy

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase

olympiads_to_subjects_table = sqlalchemy.Table('olympiads_to_classes', SqlAlchemyBase.metadata,
                                               sqlalchemy.Column('olympiad_id', sqlalchemy.Integer,
                                                                 sqlalchemy.ForeignKey('olympiads_table.id'),
                                                                 primary_key=True),
                                               sqlalchemy.Column('class_id', sqlalchemy.Integer,
                                                                 sqlalchemy.ForeignKey('school_classes_table.id'),
                                                                 primary_key=True)
                                               )


class SchoolClasses(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'school_classes_table'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    olympiads = relationship("Olympiads",
                             secondary="olympiads_to_classes",
                             back_populates="school_classes")
