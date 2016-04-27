import os
import sys
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), index=True, unique=True)
    password = Column(String(64), index=True, unique=False)
    queries = relationship('Query', backref='author', lazy='dynamic')


class Query(Base):
    __tablename__ = 'query'
    id = Column(Integer, primary_key=True)
    query = Column(String(140))
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))

engine = create_engine('sqlite:///vizitData.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def login(mail, pass_wd):
    person = session.query(User).filter(User.email == mail).one_or_none()
    if person == None:
        return False
    else:
        if person.password == pass_wd:
            return True
        else:
            return False

def addUser(mail, pass_wd):
    email = session.query(User).filter(User.email == mail).one_or_none()
    if email == None:
        new_user = User(email=mail, password=pass_wd)
        session.add(new_user)
        session.commit()
        return True
    else:
        return False
        

#Test the methods out
addUser("test", "password", "test@mail.com")
