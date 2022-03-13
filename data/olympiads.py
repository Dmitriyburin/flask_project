import datetime
import sqlalchemy
from sqlalchemy.orm import relationship

from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Olympiads(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'olympiads_table'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subjects.id"), nullable=True)
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
    # date = sqlalchemy.Column(sqlalchemy.String(35), nullable=True, default=datetime.date.today())

    stages = relationship("Stages",
                          secondary="olympiads_to_stages",
                          back_populates="olympiads")
