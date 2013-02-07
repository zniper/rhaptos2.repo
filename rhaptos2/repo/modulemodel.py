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

"""

keywd_link = Table(
    'keywd_link', Base.metadata,
    Column('user_id', String, ForeignKey('module.user_id')),
    Column('keyword_id', Integer, ForeignKey('keyword.keyword_id'))
    )

class Keyword(Base):
    """ """
    __tablename__ = 'keyword'
    keyword_id = Column(Integer, primary_key=True)
    keyword = Column(String, unique=True)


class Module(Base):
    """

    This is also the class returned from a query ... v useful.

    """
    __tablename__ = 'module'
    user_id = Column(String, primary_key=True)
    title = Column(String)
    content = Column(Text)
    keywords = relationship("Keyword", secondary=keywd_link)


    #not really needed ... will use above definitoon
    def __init__(self, user_id=None, title=None, content=None):
        self.user_id = user_id
        self.title = title
        self.content = content

    def row_as_dict(self):
        """Return the """
        d = {}
        for col in self.__table__.columns:
            d[col.name] = self.__dict__[col.name]
        return d



    def __repr__(self):
        return "Module:(%s)-%s" % (self.user_id, self.title)
