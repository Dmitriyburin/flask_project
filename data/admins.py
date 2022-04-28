import sqlalchemy

from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Admins(SqlAlchemyBase):
    __tablename__ = 'admins_table'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), unique=True)

    def __repr__(self):
        return self.name
