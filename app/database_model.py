import os
import sys
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password = Column(String(64), index=True, unique=False)
    email = Column(String(120), index=True, unique=True)
    queries = relationship('Query', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.username)


class Query(Base):
    __tablename__ = 'query'
    id = Column(Integer, primary_key=True)
    query = Column(String(140))
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return '<Query %r>' % (self.query)
