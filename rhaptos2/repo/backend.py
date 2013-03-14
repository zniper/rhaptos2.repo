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


"""


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import psycopg2


### Module globals.  Following Pylons lead, having global
### scoped_session will ensure threads (and thread locals in Flask)
### all have theit own sessions

db_engine = None
db_session = scoped_session(sessionmaker(autoflush=True,
                                         autocommit=False))

Base = declarative_base()


### As long as we subclass everything from Base, we are following
### declarative pattern recommended by sa docs.

def connect_now(confd):
    connstr = "postgresql+psycopg2://%(pgusername)s:%(pgpassword)s@%(pghost)s/%(pgdbname)s" % confd  # noqa
    engine = create_engine(connstr, echo=False)
    return engine


def initdb(confd):
    """This could become a conn factory.  """
    global db_session
    db_engine = connect_now(confd)
    db_session.configure(bind=db_engine)
    Base.metadata.create_all(db_engine)


def clean_dbase(config):
    """clear down the database tables - used for testing purposes
    """
    conn = psycopg2.connect("""dbname='%(pgdbname)s'\
                             user='%(pgusername)s' \
                             host='%(pghost)s' \
                             password='%(pgpassword)s'""" % config)
    c = conn.cursor()

    stmts = [
        "TRUNCATE TABLE public.cnxmodule CASCADE",
        "TRUNCATE TABLE public.userrole_module CASCADE",
        "TRUNCATE TABLE public.cnxfolder CASCADE",
        "TRUNCATE TABLE public.userrole_folder CASCADE",
        "TRUNCATE TABLE public.cnxcollection CASCADE",
        "TRUNCATE TABLE public.userrole_collection CASCADE",
    ]
    for stmt in stmts:
        c.execute(stmt)
        conn.commit()
    conn.close()
