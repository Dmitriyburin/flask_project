import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

from .db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship
from .olympiads import Olympiads

users_to_olympiads = sqlalchemy.Table('users_to_olympiads', SqlAlchemyBase.metadata,
                                      sqlalchemy.Column('user_id', sqlalchemy.Integer,
                                                        sqlalchemy.ForeignKey('users.id'),
                                                        primary_key=True),
                                      sqlalchemy.Column('olympiad_id', sqlalchemy.Integer,
                                                        sqlalchemy.ForeignKey('olympiads_table.id'),
                                                        primary_key=True)
                                      )


class Users(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    is_admin = False
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(35), nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String(103), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(80), nullable=True, unique=True)
    school_class = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    olympiads = relationship("Olympiads",
                             secondary="users_to_olympiads",
                             back_populates="users")

    def __repr__(self):
        return f'<User> {self.id} {self.name} {self.school_class}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def add_favorite(self, session, olymp_id):
        fav_olymp = session.query(Olympiads).get(olymp_id)
        self.olympiads.append(fav_olymp)
        session.commit()
