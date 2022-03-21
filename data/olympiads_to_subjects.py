import sqlalchemy

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase

olympiads_to_subjects = sqlalchemy.Table('olympiads_to_subjects', SqlAlchemyBase.metadata,
                                               sqlalchemy.Column('olympiad_id', sqlalchemy.Integer,
                                                                 sqlalchemy.ForeignKey('olympiads_table.id'),
                                                                 primary_key=True),
                                               sqlalchemy.Column('subject_id', sqlalchemy.Integer,
                                                                 sqlalchemy.ForeignKey('subjects_table.id'),
                                                                 primary_key=True)
                                               )


class Subjects(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'subjects_table'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(35), nullable=True)
    olympiads = relationship("Olympiads",
                             secondary="olympiads_to_subjects",
                             back_populates="subjects")

    def __repr__(self):
        return self.name
