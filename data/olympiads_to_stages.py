import datetime
import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase

olympiads_to_stages_table = sqlalchemy.Table('olympiads_to_stages', SqlAlchemyBase.metadata,
                                             sqlalchemy.Column('olympiads_id', sqlalchemy.Integer,
                                                               sqlalchemy.ForeignKey('olympiads_table.id'),
                                                               primary_key=True, ),
                                             sqlalchemy.Column('stages_id', sqlalchemy.Integer,
                                                               sqlalchemy.ForeignKey('stages_table.id'),
                                                               primary_key=True, )
                                             )


class Stages(SqlAlchemyBase):
    __tablename__ = 'stages_table'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(35), nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String(35), nullable=True, default=datetime.date.today())
    olympiads = relationship("Olympiads",
                             secondary="olympiads_to_stages",
                             back_populates="stages")
