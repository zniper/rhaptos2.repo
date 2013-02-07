#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012
# This software is subject to
# the provisions of the GNU Lesser General
# Public License Version 2.1 (LGPL).
# See LICENCE.txt for details.
###


"""
Provide a abstracted SQL Alchemy backend to allow
models to connect to postegres.

cut paste from rhaptos2.user
"""


from sqlalchemy import create_engine, MetaData, Table, ForeignKey
from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship



### Module globals.  Following Pylons lead, having global
### scoped_session will ensure threads (and thread locals in Flask)
### all have theit own sessions



db_session = scoped_session(sessionmaker(autoflush=True,
                                      autocommit=False,))
Base = declarative_base()


### As long as we subclass everything from Base, we are following
### ndeclarative pattern recommended


def connect_now(confd):
    connstr = "postgresql+psycopg2://%(pgusername)s:%(pgpassword)s@%(pghost)s/%(pgdbname)s" % confd
    engine = create_engine(connstr)
    return engine


def initdb(confd):

    global db_session
    engine = connect_now(confd)
    db_session.configure(bind=engine)
    Base.metadata.create_all(engine)
