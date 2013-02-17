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
models:  I am trying to keep things simple.  This may not be a good idea.

each model is a class, based on a SQLAlchemy foundation with :class:CNXBase
as a extra inheritence.  This CNXBase gives us to and from json capabilities,
but each model has to manually override to and from json calls if


PWhat is the same about each model / class

1. They have only themselves - there are no child tables needing
   hierarchialcly handling.  If this was needed we should look at
   rhaptos2.user for the approach - pretty simple, just modiufy the
   from and to dict calls

2. They are representing *resources* - that is a entity we want to have some
   form of access control over.  So we use the generic-ish approach
   of userroles - see below.


3. THey are all ID'd by URI


Note on json - the obvious generic approach, of traversing the SQLA
model and converting to/from JSON automagically has so far failed.
There are no sensible approaches "out there", seemingly because the
obvious approaches (iter) have already been hijacked by SQLA and
the edge cases are producing weird effects.


So, this basically implies a protocol for objects / classes

1. support creater_uri= in your constructor
2. override fomr and to json SQLA where needed
3. Support ACLs
4. err ....




"""
import json
import uuid
import pprint

from sqlalchemy import (Table, ForeignKey, or_,
                        Column, Integer, String,
                        Text, Enum, DateTime)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy.types
import datetime


from cnxbase import CNXBase

#shared session from backend module, for pooling

from rhaptos2.repo.backend import Base, db_session
from rhaptos2.repo import dolog
from rhaptos2.common.err import Rhaptos2Error

################## FOLDERS #################################

class UserRole(Base, CNXBase):
    """The roles and users assigned for a given folder

    We have following Roles: Owner, Maintainer, XXX


    :todo: storing timezones naively here needs fixing


    """
    __tablename__ = 'userrole_folder'
    folder_uuid = Column(String, ForeignKey('cnxfolder.folderid'),
                         primary_key=True)
    user_uuid   = Column(String, primary_key=True)
    role_type   = Column(Enum('aclrw','aclro',
                               name="cnxrole_type"),
                               primary_key=True)
    date_created_utc = Column(DateTime)
    date_lastmodified_utc = Column(DateTime)

    def __repr__(self):
        return "%s-%s" % (self.role_type, self.user_uuid)



class Folder(Base, CNXBase):
    """
    FOlder Class inheriting from SQLAlchemy and from a CNXBase class
    to get a few generic functions.

    1. we define the table and columns
    2. set a new unique ID if not already one (differen between PUT and POST)
    3. from_dict - will receive a dictionary of keywords that map exactly
       to column fields and will populate itself.
    4. to_dict will emit a dictionary representing the object.
       If this is a "leaf" table then it is entirely using CNXBase superclass
       If this is table is PK for anothers FK then we need to manually
       code a method to get the FK linked object.
       There is no reliable generic way to do this in SQLALchemy afaik.
       Frankly thats not a problem, as its pretty cut and paste.

    5. jsonify - wrap to_dict in json.  In otherwords convert self to a JSON doc



    """
    __tablename__ = 'cnxfolder'
    folderid = Column(String, primary_key=True)
    title = Column(String)
    content = Column(ARRAY(String))
    date_created_utc = Column(DateTime)
    date_lastmodified_utc = Column(DateTime)

    userroles = relationship("UserRole",
                             backref="cnxfolder",
                             cascade="all, delete-orphan")

    def __init__(self, folderid=None, creator_uuid=None):
        """ """
        if creator_uuid:
            self.adduserrole(UserRole,
                {'user_uuid':creator_uuid, 'role_type':'aclrw'})
        else:
            raise Rhaptos2Error("Foldersmust be created with a creator UUID ")

        if folderid :
            self.folderid = folderid
        else:
            self.folderid = str(uuid.uuid4())

        self.date_created_utc = self.get_utcnow()

    def __repr__(self):
        return "Folder:(%s)-%s" % (self.folderid, self.title)


    # def to_dict(self):
    #     """Return self as a dict, suitable for jsonifying """

    #     d = {}
    #     for col in self.__table__.columns:
    #         d[col.name] = self.safe_type_out(col)#getattr(self, col.name)

    #    ### each "child" relationship, adjust the dict to be returned
    #     d['userroles'] = []
    #     for i in self.userroles:
    #         d['userroles'].append(i.to_dict())
    #     return d

def mkobjfromlistofdict(o, l):
    """ Glimmering of recursion style needed
        However too fragile...
    """
    ### really I need to know when to stop - test for list / dict in vlaues///
    outl = []
    for dict_of_fields in l:
        x = o()
        for key in dict_of_fields:
            setattr(x, key, dict_of_fields[key])
        outl.append(x)
    return outl


# def put_user(jsond, folder_id):
#     """Given a user_id, and a json_str representing the "Updated" fields
#        then update those fields for that user_id """

#     try:
#         uobj =get_folder(folder_id)
#     except Exception, e:
#         dolog("INFO", str(e))
#         raise Rhaptos2Error("FAiled to get user")

#     #.. todo:: parser = verify_schema_version(None)
#     updated_obj = populate_folder(jsond, uobj)
#     db_session.add(updated_obj); db_session.commit()
#     return updated_obj


# def populate_folder(incomingd, folder_obj):
#     """Given a dict, and an object,
#        push dict into object and return it.

#     .. todo:: validate and parse dict.

#     """

#     ### put every key in json into FOlder(), manually handling
#     ### userroles
#     for k in incomingd:
#         if k not in (u'userrole', u'userroles'):
#             setattr(folder_obj, k, incomingd[k])
#         else:
#             ### create a list of Identifer objects from the list of
#             ### identifier strings in JSON
#             l = incomingd[k]
#             outl =  mkobjfromlistofdict(UserRole, l)
#             for userrole in outl: userrole.folder_uuid = folder_obj.folderid
#             folder_obj.userroles = outl



# def post_folder(incomingd, creator_uuid):
#     """Given a dict representing the complete set
#        of fields then create a new user and those fields

#     I am getting a dictionary direct form Flask request object - want
#     to handle that myself with parser.

#     returns User object, for later saveing to DB"""

#     u = Folder(creator_uuid=creator_uuid)

#     #parser = verify_schema_version(None)
#     #incomingd = parser(json_str)
#     u.populate_self(incomingd)
#     db_session.add(u); db_session.commit()
#     return u


# def get_folder(folderid):
#     """
#     returns a User object, when provided with user_id
#     """

#     ### Now lets recreate it.
#     global db_session
#     q = db_session.query(Folder)
#     q = q.filter(Folder.folderid == folderid)
#     rs = q.all()
#     if len(rs) == 0:
#         raise Rhaptos2Error("Folder ID Not found in this repo")
#     ### There is a uniq constraint on the table, but anyway...
#     if len(rs) > 1:
#         raise Rhaptos2Error("Too many matches")

#     newf = rs[0]
#     return newf


def get_by_id(klass, ID):
    """

    part of the re-factor...
     """
    q = db_session.query(klass)
    q = q.filter(klass.folderid == ID)
    rs = q.all()
    if len(rs) == 0:
        raise Rhaptos2Error("User ID Not found in this repo")
    ### There is a uniq constraint on the table, but anyway...
    if len(rs) > 1:
        raise Rhaptos2Error("Too many matches")

    newu = rs[0]
    return newu


def post_o(klass, incomingd, creator_uuid):
    """Given a dict representing the complete set
    of fields then create a new user and those fields

    I am getting a dictionary direct form Flask request object - want
    to handle that myself with parser.

    returns User object, for later saveing to DB"""

    u = klass(creator_uuid=creator_uuid)

    #parser = verify_schema_version(None)
    #incomingd = parser(json_str)
    u.populate_self(incomingd)
    db_session.add(u); db_session.commit()
    return u

def put_o(jsond, klass, ID):
    """Given a user_id, and a json_str representing the "Updated" fields
       then update those fields for that user_id """

    try:
        uobj = get_by_id(klass, ID)
    except Exception, e:
        dolog("INFO", str(e))
        raise Rhaptos2Error("FAiled to get obj")

    #.. todo:: parser = verify_schema_version(None)
    uobj.populate_self(jsond)
    db_session.add(uobj); db_session.commit()
    return uobj

def delete_o(klass, ID):
    """ """
    fldr = get_by_id(klass, ID)
    db_session.delete(fldr)
    db_session.commit()


def close_session():
    db_session.remove()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
