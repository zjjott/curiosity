# coding=utf-8

import random
from datetime import date
import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column,
                        Boolean, BigInteger,
                        Integer,
                        String,
                        Text)
from sqlalchemy.ext.declarative import declared_attr

from clambda.db import session_scope, Session, db_engine

logger = logging.getLogger("sqlalchemy")
BASEOBJ = declarative_base()


class ModelBase(BASEOBJ):
    """Base class for Nova and Glance Models"""
    __abstract__ = True
    __table_args__ = {'mysql_engine': 'InnoDB',
                      'mysql_charset': 'utf8'}
    __table_initialized__ = False

    @declared_attr
    def __tablename__(cls):
        """可以在类定义里面设定__tablename__=xxx或者从这里默认构造出一个表名"""
        class_name = cls.__name__.lower()
        return class_name

    @classmethod
    def session(cls):
        return session_scope()

    @classmethod
    def query(cls, *args, **kwargs):
        """ Query """
        session = Session()
        if len(args) == 0:
            q = session.query(cls)
        else:
            q = session.query(*args)
        return q

    def save_object(self, session=None, commit=True):
        """Save a new object"""
        if session is None:
            session = Session()
        session.add(self)
        if commit:
            try:
                session.commit()
            except:
                session.rollback()
                # clean_db_session()
                raise


class LambdaFunction(ModelBase):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    memory_limit = Column(
        Integer,
        default=1000,
        nullable=False,
        doc="task execute memory limit(K)")
    time_limit = Column(Integer, default=30, nullable=False,
                        doc="task execute time limit(s)")
    code = Column(Text)


def main():
    pass


if __name__ == '__main__':
    # ModelBase.metadata.create_all(db_engine)
    LambdaFunction(user_id=1,
                   memory_limit=1000,
                   time_limit=1000,
                   code="""def execute():
    print("hello world")
"""
                   ).save_object()
