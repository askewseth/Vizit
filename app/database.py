from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from database_model import User, Base, Query

engine = create_engine('sqlite:///vizit_database.db')

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

def addUser(user, pass_wd, mail):
    new_user = User(username=user, password=pass_wd, email=mail)
    session.add(new_user)
    session.commit()

#Test the methods out
addUser("test", "password", "test@mail.com")
