import datetime
import sqlalchemy
from sqlalchemy.orm import relationship

from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from .olympiads_to_subjects import Subjects


class Olympiads(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'olympiads_table'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    subjects = relationship("Subjects",
                            secondary="olympiads_to_subjects",
                            back_populates="olympiads")

    title = sqlalchemy.Column(sqlalchemy.String(120), nullable=True)
    school_classes = relationship("SchoolClasses",
                                  secondary="olympiads_to_classes",
                                  back_populates="olympiads")

    description = sqlalchemy.Column(sqlalchemy.Text)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    link = sqlalchemy.Column(sqlalchemy.String(150), nullable=True)
    # stages = relationship("Stages",
    #                       secondary="olympiads_to_stages",
    #                       back_populates="olympiads")

    stages = relationship("Stages", back_populates="olympiad")

    users = relationship("Users",
                         secondary="users_to_olympiads",
                         back_populates="olympiads")

    def add_subject(self, session, subject_id):
        subject = session.query(Subjects).get(subject_id)
        self.subjects.append(subject)
        session.commit()

    # def add_stage(self, session, stage_id, date):
    #     stage = olympiads_to_stages.insert().values(olympiads_id=self.id,
    #                                                       stages_id=stage_id,
    #                                                       date=date)
    #     session.execute(stage)
    #     session.commit()

    def __repr__(self):
        return self.title
