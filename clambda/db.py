# coding=utf-8
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from clambda.options import db_uri


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


db_engine = create_engine(db_uri)

session_maker = sessionmaker(bind=db_engine)
Session = scoped_session(session_maker)
