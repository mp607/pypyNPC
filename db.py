#!/usr/bin/python
# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()
session = None

class Songs(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    user = Column(String)
    plurkid = Column(String)
    search = Column(String)
    v1 = Column(String)
    v2 = Column(String)
    dt = Column(DateTime, default=datetime.utcnow())

    def __init__(self, user, plurkid, search, v1, v2):
        self.user = user
        self.plurkid = plurkid
        self.search = search
        self.v1 = v1
        self.v2 = v2

    def __repr__(self):
        return "<Songs(user='%s',plurkid='%s',search='%s',v1='%s',v2='%s',dt='%s')>" % \
                (self.user, self.plurkid, self.search, self.v1, self.v2, self.dt)


def insert_findSongs(user, plurkid, search, v1, v2):
    session.add(Songs(user, plurkid, search, v1, v2))
    session.commit()

def connect(echo = False):
    engine = create_engine('sqlite:///db/pypyNPC.db')
    engine.echo = echo
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind = engine)
    global session
    session = Session()

if __name__ =='__main__':
    connect(True)
    insert_findSongs(0,0,0,0,0)

    for data in session.query(Songs).filter_by(user='0').all():
        print data
        session.delete(data)
        session.commit()

    session.close()
