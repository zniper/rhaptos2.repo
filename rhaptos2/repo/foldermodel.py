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


"""
import json
import uuid
import pprint

from sqlalchemy import (Table, ForeignKey, or_,
                        Column, Integer, String,
                        Text, Enum, DateTime)
from sqlalchemy.orm import relationship
import sqlalchemy.types
import datetime


from cnxbase import CNXBase

#shared session from backend module, for pooling

from rhaptos2.repo.backend import Base, db_session
from rhaptos2.common.err import Rhaptos2Error


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
    contentjson = Column(Text)
    date_created_utc = Column(DateTime)
    date_lastmodified_utc = Column(DateTime)

    userroles = relationship("UserRole",
                             backref="cnxfolder",
                             cascade="all, delete-orphan")


    def __init__(self, folderid=None, creator_uuid=None):
        if creator_uuid:
            self.adduserrole({'user_uuid':creator_uuid, 'role_type':'aclrw'})
        else:
            raise Rhaptos2Error("Foldersmust be created with a creator UUID ")

        if folderid :
            self.folderid = folderid
        else:
            self.folderid = str(uuid.uuid4())
        self.content = self.contentjson

    def __repr__(self):
        return "Folder:(%s)-%s" % (self.folderid, self.title)

    def safe_type_out(self, col):
        """return the value of a coulmn field safely for json
           This is essentially a JSONEncoder sublclass inside object - ...
        """

        if isinstance(type(col.type), sqlalchemy.types.DateTime):
            outstr = getattr(self, col.name).isoformat()
        else:
            outstr = getattr(self, col.name)
        return outstr


    def set_acls(self, setter_user_uuid, acllist):
        """set the user acls on this object.

        SOme, not all objects that inherit form CNXBase (!)
        will have a relatred user_roles table.
        This will map the object ID to a acl type and a user


        [{'date_lastmodified_utc': None,
          'date_created_utc': None,
          'user_uuid': u'Testuser1',
          'role_type': 'author'},
         {'date_lastmodified_utc': None,
          'date_created_utc': None,
          'user_uuid': u'testuser2',
          'role_type': 'author'}]



        """
        ##is this authorised? - sep function?
        if (setter_user_uuid, "aclrw") not in [(u.user_uuid, u.role_type)
                                               for u in self.userroles]:
            raise Rhaptos2Error("http:401")
        else:
            for usrdict in acllist:
                #I am losing modified info...
                self.adduserrole(usrdict)

    def adduserrole(self, usrdict):
        """ keeping a common funciton in one place

        Given a usr_uuid and a role_type, update a UserRole object

        I am checking setter_user is authorised in calling function.
        Ideally check here too.
        """
        t = get_utcnow()

        ##why not pass around USerROle objects??
        user_uuid = usrdict['user_uuid']
        role_type = usrdict['role_type']

        if user_uuid not in [u.user_uuid for u in self.userroles]:
            #not got this one, add
            i = UserRole()
            i.from_dict(usrdict)
            i.date_created_utc = t
            i.date_lastmodified_utc = t
            self.userroles.append(i)

        elif (user_uuid, role_type) not in [(u.user_uuid, u.role_type) for u
                                             in self.userroles]:
            #user exits but diff role tyoe = update
            i = UserRole()
            i.from_dict(usrdict)
            i.date_lastmodified_utc = t
            self.userroles.append(i)
        else:
            #user is there, user and role type is there, rhis is duplicate
            pass


    def from_dict(self, d):
        """

        We only support pushing JSON in - one object at a time There
        is no obvious way to do it automatically over a hierarchy, so
        manually look for the "realtions" and add them.  (backrefs
        seriously complicate the obvious attack vector here)

        There are no "child" data in the json - that is nothign
        in json that maps to another table.

        """
        for k in d:
            setattr(self, k, d[k])


    def to_dict(self):
        """Return self as a dict, suitable for jsonifying """

        d = {}
        for col in self.__table__.columns:
            d[col.name] = self.safe_type_out(col)#getattr(self, col.name)

       ### each "child" relationship, adjust the dict to be returned
        d['userroles'] = []
        for i in self.userroles:
            d['userroles'].append(i.to_dict())
        return d

    def jsonify(self):
        """Helper function that returns simple json repr """
        return self.contentjson


def get_utcnow():
    """Eventually we shall handle TZones here too"""
    return datetime.datetime.utcnow()

def parse_json(jsonstr):
    """Given a json-formatted string representing a folder, return a dict

       There is a lot todo here.
       We should have version handling (see online discussions)
       We should check that the json is actually valid for a folder
       """
    try:
        jsond = json.loads(jsonstr)
    except:
        raise Rhaptos2Error("Error converting json to dict")
    return jsond

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


def put_user(jsond, folder_id):
    """Given a user_id, and a json_str representing the "Updated" fields
       then update those fields for that user_id """

    try:
        uobj =get_folder(folder_id)
    except Exception, e:
        dolog("INFO", str(e))
        raise Rhaptos2Error("FAiled to get user")

    #.. todo:: parser = verify_schema_version(None)
    updated_obj = populate_folder(jsond, uobj)
    db_session.add(updated_obj); db_session.commit()
    return updated_obj


def populate_folder(incomingd, folder_obj):
    """Given a dict, and an object,
       push dict into object and return it.

    .. todo:: validate and parse dict.

    """

    ### put every key in json into FOlder(), manually handling
    ### userroles
    for k in incomingd:
        if k not in (u'userrole', u'userroles'):
            setattr(folder_obj, k, incomingd[k])
        else:
            ### create a list of Identifer objects from the list of
            ### identifier strings in JSON
            l = incomingd[k]
            outl =  mkobjfromlistofdict(UserRole, l)
            for userrole in outl: userrole.folder_uuid = folder_obj.folderid
            folder_obj.userroles = outl



def post_folder(incomingd, creator_uuid):
    """Given a dict representing the complete set
       of fields then create a new user and those fields

    I am getting a dictionary direct form Flask request object - want
    to handle that myself with parser.

    returns User object, for later saveing to DB"""

    u = Folder(creator_uuid=creator_uuid)

    #parser = verify_schema_version(None)
    #incomingd = parser(json_str)
    populate_folder(incomingd, u)  #be careful None returned. XXX
    db_session.add(u); db_session.commit()
    return u


def get_folder(folderid):
    """
    returns a User object, when provided with user_id
    """

    ### Now lets recreate it.
    global db_session
    q = db_session.query(Folder)
    q = q.filter(Folder.folderid == folderid)
    rs = q.all()
    if len(rs) == 0:
        raise Rhaptos2Error("Folder ID Not found in this repo")
    ### There is a uniq constraint on the table, but anyway...
    if len(rs) > 1:
        raise Rhaptos2Error("Too many matches")

    newf = rs[0]
    return newf


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

def put_o(jsond, klass, ID):
    """Given a user_id, and a json_str representing the "Updated" fields
       then update those fields for that user_id """

    try:
        uobj = get_by_id(klass, ID)
    except Exception, e:
        dolog("INFO", str(e))
        raise Rhaptos2Error("FAiled to get user")

    #.. todo:: parser = verify_schema_version(None)
    updated_obj = populate_folder(jsond, uobj)
    db_session.add(uobj); db_session.commit()
    return uobj

def delete_o(klass, ID):
    """ """
    fldr = get_by_id(klass, ID)
    db_session.delete(fldr)
    db_session.commit()

# def get_user_by_identifier(unquoted_id):
#     """ """

#     ### Now lets recreate it.

#     q = db_session.query(Identifier)
#     q = q.filter(Identifier.identifierstring == unquoted_id)
#     rs = q.all()

#     if len(rs) == 0:
#         raise Rhaptos2Error("Identifer ID Not found in this repo")
#     if len(rs) > 1:
#         raise Rhaptos2Error("Too many matches")

#     #.. todo:: stop using indexes on rows - transform to fieldnames
#     user_id = rs[0].user_id
#     newu = get_user(user_id)
#     return newu


# def get_user_by_name(namefrag):
#     """
#     Perform a case insensitive search on fullname

#     I would like to offer at least two other searches,
#     specifying the fields to search, and a frag search across
#     many fields.
#     """

#     q = db_session.query(User)
#     q = q.filter(or_(
#                      User.fullname.ilike("%%%s%%" % namefrag),
#                      User.email.ilike("%%%s%%" % namefrag),
#                      ))
#     rs = q.all()
#     out_l = []
#     for row in rs:
#         out_l.append(row)
#     return out_l

# def get_all_users():
#     """ FOr search functionality"""

#     q = db_session.query(User)
#     rs = q.all()
#     out_l = []
#     c = 0
#     for row in rs:
#         out_l.append(row)
#         c += 1
#         if c >= 25: break
#     # ..todo:: the worst limiting case ever...
#     return out_l



# def delete_user(security_token, user_id):
#     """ """
#     raise Rhaptos2Error("delete user not supported")


def close_session():
    db_session.remove()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
