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
We wish to supply models for

* Folders
* Collections
* Modules

These will all be stored as original JSON documents, as postgres
text files, and in the same table will be stored

We shall store all the above in follwoing tables

folder:

     uuid
     date_created_utc
     date_lastmodified_utc
     content



Ownership
---------

Each container-type table will have a ownership table attached
This will hold owner / role data as below

     folder_uuid
     user_uuid
     role_type
     date_created_utc
     date_cancelled_utc

THis way we can hold ownership information reasonably well.



I am aware of the JSON type in postgres 9.3 but am not
currently willing to spend time getting it to work through sqlalchemy
 - this may be a mistake I shall see.


Intial creation of a Folder
---------------------------



"""

import json
import uuid
import pprint

from sqlalchemy import Table, ForeignKey
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime
from sqlalchemy.orm import  relationship

from rhaptos2.repo.backend import Base, db_session


class UserRole(Base):
    """The roles and users assigned for a given folder

    We have following Roles: Owner, Maintainer, XXX


    :todo: storing timezones naively here needs fixing


    """
    __tablename__ = 'userrole_folder'
    folder_uuid = Column(String, ForeignKey('cnxfolder.folderid'),
                         primary_key=True)
    user_uuid   = Column(String, primary_key=True)
    role_type   = Column(Enum('author', 'maintainer','copyright',
                               name="cnxrole_type"),
                               primary_key=True)
    date_created_utc = Column(DateTime)
    date_lastmodified_utc = Column(DateTime)




class Folder(Base):
    """

    This is also the class returned from a query ... v useful.

    """
    __tablename__ = 'cnxfolder'
    folderid = Column(String, primary_key=True)
    title = Column(String)
    contentjson = Column(Text)
    date_created_utc = Column(DateTime)
    date_lastmodified_utc = Column(DateTime)

    userroles = relationship("UserRole", backref="cnxfolder")


    #not really needed ... will use above definitoon
    def __init__(self, folderid=None, title=None, content=None):
        self.folderid = folderid
        self.title = title
        self.contentjson = content

    def row_as_dict(self):
        """Return the """
        d = {}
        for col in self.__table__.columns:
            d[col.name] = self.__dict__[col.name]
        return d



    def __repr__(self):
        return "Module:(%s)-%s" % (self.folderid, self.title)
