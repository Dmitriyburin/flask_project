import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from sqlalchemy import create_engine
from .gitignore import user, password, host, port, database

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init():
    global __factory

    if __factory:
        return

    # This engine just used to query for list of databases
    mysql_engine = create_engine('mysql://{0}:{1}@{2}:{3}'.format(user, password, host, port))

    # Query for existing databases
    mysql_engine.execute("CREATE DATABASE IF NOT EXISTS {0} ".format(database))

    # Go ahead and use this engine
    engine = create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(user, password, host, port, database))

    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


"""
from sqlalchemy import create_engine
from gitignore import user, password, host, port, database

# This engine just used to query for list of databases
mysql_engine = create_engine('mysql://{0}:{1}@{2}:{3}'.format(user, password, host, port))

# Query for existing databases
mysql_engine.execute("CREATE DATABASE IF NOT EXISTS {0} ".format(database))

# Go ahead and use this engine
db_engine = create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(user, password, host, port, database))
"""
