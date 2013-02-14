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


class UserRoleCol(Base, CNXBase):
    """The roles and users assigned for a given collection

    We have following Roles: Owner, Maintainer, XXX


    :todo: storing timezones naively here needs fixing


    """
    __tablename__ = 'userrole_col'
    collection_uuid = Column(String, ForeignKey('cnxcollection.collectionid'),
                         primary_key=True)
    user_uuid   = Column(String, primary_key=True)
    role_type   = Column(Enum('aclrw','aclro',
                               name="cnxrole_type"),
                               primary_key=True)
    date_created_utc = Column(DateTime)
    date_lastmodified_utc = Column(DateTime)

    def __repr__(self):
        return "%s-%s" % (self.role_type, self.user_uuid)



class Collection(Base, CNXBase):
    """
    Collection Class inheriting from SQLAlchemy and from a CNXBase class
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
    __tablename__ = 'cnxcollection'
    collectionid = Column(String, primary_key=True)
    title = Column(String)
    contentjson = Column(Text)
    date_created_utc = Column(DateTime)
    date_lastmodified_utc = Column(DateTime)

    userroles = relationship("UserRoleCol", backref="cnxcollection")

    def __init__(self, collectionid=None, creator_uuid=None):
        if creator_uuid:
            self.adduserrole({'user_uuid':creator_uuid, 'role_type':'aclrw'})
        else:
            raise Rhaptos2Error("Collectionsmust be created with a creator UUID ")

        if collectionid :
            self.collectionid = collectionid
        else:
            self.collectionid = str(uuid.uuid4())

    def __repr__(self):
        return "Collection:(%s)-%s" % (self.collectionid, self.title)

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

        Given a usr_uuid and a role_type, update a UserRoleCol object

        I am checking setter_user is authorised in calling function.
        Ideally check here too.
        """
        t = get_utcnow()

        ##why not pass around USerROle objects??
        user_uuid = usrdict['user_uuid']
        role_type = usrdict['role_type']

        if user_uuid not in [u.user_uuid for u in self.userroles]:
            #not got this one, add
            i = UserRoleCol()
            i.from_dict(usrdict)
            i.date_created_utc = t
            i.date_lastmodified_utc = t
            self.userroles.append(i)

        elif (user_uuid, role_type) not in [(u.user_uuid, u.role_type) for u
                                             in self.userroles]:
            #user exits but diff role tyoe = update
            i = UserRoleCol()
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
    """Ul;timately we should have multiple version handling. """
    return json.loads(jsonstr)

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


def put_user(jsond, collection_id):
    """Given a user_id, and a json_str representing the "Updated" fields
       then update those fields for that user_id """

    try:
        uobj =get_collection(collection_id)
    except Exception, e:
        dolog("INFO", str(e))
        raise Rhaptos2Error("FAiled to get user")

    #.. todo:: parser = verify_schema_version(None)
    updated_obj = populate_collection(jsond, uobj)
    db_session.add(updated_obj); db_session.commit()
    return updated_obj


def populate_collection(incomingd, collection_obj):
    """Given a dict, and an object,
       push dict into object and return it.

    .. todo:: validate and parse dict.

    """

    ### put every key in json into Collection(), manually handling
    ### userroles
    for k in incomingd:
        if k not in (u'userrole', u'userroles'):
            setattr(collection_obj, k, incomingd[k])
        else:
            ### create a list of Identifer objects from the list of
            ### identifier strings in JSON
            l = incomingd[k]
            outl =  mkobjfromlistofdict(UserRoleCol, l)
            for userrole in outl: userrole.collection_uuid = collection_obj.collectionid
            collection_obj.userroles = outl



def post_user(jsond):
    """Given a dict representing the complete set
       of fields then create a new user and those fields

    I am getting a dictionary direct form Flask request object - want
    to handle that myself with parser.

    returns User object, for later saveing to DB"""

    u = Collection()

    #parser = verify_schema_version(None)
    #incomingd = parser(json_str)
    incomingd = json_dict
    u = populate_collection(incomingd, u)
    db_session.add(u); db_session.commit()
    return u


def get_collection(collectionid):
    """
    returns a User object, when provided with user_id
    """

    ### Now lets recreate it.
    global db_session
    q = db_session.query(Collection)
    q = q.filter(Collection.collectionid == collectionid)
    rs = q.all()
    if len(rs) == 0:
        raise Rhaptos2Error("Collection ID Not found in this repo")
    ### There is a uniq constraint on the table, but anyway...
    if len(rs) > 1:
        raise Rhaptos2Error("Too many matches")

    newf = rs[0]
    return newf


def close_session():
    db_session.remove()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
