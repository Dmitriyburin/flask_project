import datetime
import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase
#
# olympiads_to_stages = sqlalchemy.Table('olympiads_to_stages', SqlAlchemyBase.metadata,
#                                              sqlalchemy.Column('olympiads_id', sqlalchemy.Integer,
#                                                                sqlalchemy.ForeignKey('olympiads_table.id'),
#                                                                primary_key=True, ),
#                                              sqlalchemy.Column('stages_id', sqlalchemy.Integer,
#                                                                sqlalchemy.ForeignKey('stages_table.id'),
#                                                                primary_key=True, ),
#                                              sqlalchemy.Column('date', sqlalchemy.Date, nullable=True,
#                                                                default=datetime.date.today())
#                                              )


class Stages(SqlAlchemyBase):
    __tablename__ = 'stages_table'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(35), nullable=True)
    olympiad_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('olympiads_table.id'))
    olympiad = relationship('Olympiads', back_populates="stages")
    date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.date.today())
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    # olympiads = relationship("Olympiads",
    #                          secondary="olympiads_to_stages",
    #                          back_populates="stages")

    def __repr__(self):
        return self.name



