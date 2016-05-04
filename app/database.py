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

def returnUserIDByEmail(mail):
    for instance in session.query(User).filter_by(email=mail):
        return instance.id

def addBasicQueryHistory(mail, query_data):
    for instance in session.query(User).filter_by(email=mail):
        users_id = instance.id
        email = instance.email

    insert_string = '1[{' + query_data + '}]'
    new_query = Query(query=insert_string, timestamp=datetime.now(), user_id=users_id)
    session.add(new_query)
    session.commit()

def addPlotHistory(mail, query_data1, query_data2):
    for instance in session.query(User).filter_by(email=mail):
        users_id = instance.id
        email = instance.email

    insert_string = '2[{' + query_data1 + '}{' + query_data2 + '}]'
    new_query = Query(query=insert_string, timestamp=datetime.now(), user_id=users_id)
    session.add(new_query)
    session.commit()

def addGridHistory(mail, file_path):
    for instance in session.query(User).filter_by(email=mail):
        users_id = instance.id
        email = instance.email

    insert_string = '3[{' + file_path + '}]'
    new_query = Query(query=insert_string, timestamp=datetime.now(), user_id=users_id)
    session.add(new_query)
    session.commit()

def addCSVHistory(mail, file_path):
    for instance in session.query(User).filter_by(email=mail):
        users_id = instance.id
        email = instance.email

    insert_string = '4[{' + file_path + '}]'
    new_query = Query(query=insert_string, timestamp=datetime.now(), user_id=users_id)
    session.add(new_query)
    session.commit()

def returnAllHistory(mail):
    users_id = returnUserIDByEmail(mail)
    matrix = []
    count = 0
    for instance in session.query(Query).filter_by(user_id=users_id):
        if instance.query[:1] == '1':
            query_type = 'Basic Statistical Query'
        elif instance.query[:1] == '2':
            query_type = 'Plot Statistical Query'
        elif instance.query[:1] == '3':
            query_type = 'Grid Statistical Query'
        elif instance.query[:1] == '4':
            query_type = 'CSV Upload Statistical Query'
        else:
            query_type = 'Unknown Statistical Query'

        time = instance.timestamp
        query_time = str(time.month) + '/' + str(time.day) + '/' + str(time.year) + ' -- ' + str(time.hour) + ':' + str(time.minute) + ':' + str(time.second)
        matrix.append([])
        matrix[count].append(query_time)
        matrix[count].append(query_type)
        matrix[count].append(str(time.month) + ':' + str(time.day) + ':' + str(time.year) + ':' + str(time.hour) + ':' + str(time.minute) + ':' + str(time.second))
        matrix[count].append(instance.query)
        count = count + 1

    return matrix
