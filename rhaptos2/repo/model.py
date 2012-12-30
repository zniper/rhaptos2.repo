#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012
# This software is subject to
# the provisions of the GNU Lesser General
# Public License Version 2.1 (LGPL).
# See LICENCE.txt for details.
###


import datetime
import datetime
import md5, random
import os, sys
import hashlib
import statsd
import json
from functools import wraps
import urlparse
import pprint

from rhaptos2.common import conf
from rhaptos2.common import log
from rhaptos2.common.err import Rhaptos2Error
from rhaptos2.repo import get_app, dolog
from rhaptos2.repo import files, security

import flask
from flask import Flask, render_template, request, g, session, flash, \
     redirect, url_for, abort
from flaskext.openid import OpenID
import memcache
import requests
import urllib

### XXX This needs to be wrapped in makeapp function ...
app = get_app()

app.config.update(
    SECRET_KEY = app.config['openid_secretkey'],
    DEBUG      = app.debug
)
RESOURCES_DIR_PATH = os.path.join(app.config['repodir'],
                                  'resources')
METADATA_FILE_PATH = os.path.join(RESOURCES_DIR_PATH, 'resource-metadata')

# setup flask-openid
oid = OpenID(app)


#def resp_as_json():
#    '''decorator that will convert to json '''
#    @wraps(f)
#    def decorated_function(*args, **kwargs):
#        resp = flask.make_response(f)
#        resp.content_type='application/json'
#        return resp
#    return decorated_function

'''

Wanted:

onbjects to standarse the things like username lookups, username to directory, etc etc

Tests I want to see
-------------------

* logging
* message queueing
* pygit - api



API
---

:Workspace:  a group of repos
:collection: a group of files,
             including ordering of modules
             Effectively a repo
:branch: branch of a single repo

:fork: branch of a single repo, but placed under my workspace
       github - ? clone?
:pull request: how?




ToDO:

* better CORS handling - see http://flask.pocoo.org/snippets/56/
* decorator info: http://flask.pocoo.org/docs/patterns/viewdecorators/
  http://docs.python.org/library/functools.html#functools.wraps

'''



class User(object):
    """
    represents the user as looked up by an authneticated identifer

    .. todo:: this is a integration test !!! fix the nose test division stuff.

    >>> u = User('ben@mikadosoftware.com')
    >>> u.FullName
    u'Benjamin Franklin'


    """

    def __init__(self, authenticated_identifier):
        """initialise from a id we have had verified by third party

        .. todo:: this is stubbed out - it should always go to user dbase and lookup fromidentifer
        .. todo:: what should I do if user dbase is unavilable???
        .. todo:: totally unsafe laoding of user details

        """
#        try:
#        safe_auth_identifier = urllib.quote_plus(authenticated_identifier)

        payload = {'user':authenticated_identifier}

        user_server_url = app.config['globals']['bamboo_global']['userserver'].replace("/user", "/openid")

        dolog("INFO", "requesting user info - from url %s and query string %s" %
                       (user_server_url, repr(payload)))

        try:
            r = requests.get(user_server_url, params=payload)
            userdetails = r.json
        except Exception, e:
            #.. todo:: not sure what to do here ... the user dbase is down
            userdetails = None

        dolog("INFO", "Got back %s " % str(userdetails))
        if userdetails:
            self.__dict__.update(r.json)
        else:
            ### needs rethinkgin - time of deamo dday too close
            self.email = "Unknown User"
            self.fullname = "Unknown User"
            self.user_id = "Unknownuser"


    def __repr__(self):
        return pprint.pformat(self.__dict__)

    def load_JSON(self, jsondocstr):
        """ parse and store details of properly formatted JSON doc
        """
        user_dict = json.loads(jsondocstr)
        self.__dict__.update(user_dict)




class Identity(object):
    """ THis 'owns' User - its rubbish to have two clases doing the same basic thing.
        I should merge them but need longer to test (demo day)
    """

    def __init__(self, authenticated_identifier):
        """placeholder - we want to store identiy values somewhere but
           sqlite is limited to one server, so need move to network
           aware storage

        .. todo:: rename FUllNAme to fullname
        .. todo:: in fact fix whole user details
        .. todo:: combine identiy and USer into one class !

        """

        self.authenticated_identifier = authenticated_identifier
        self.user = get_user_from_identifier(authenticated_identifier)

        if self.user:
            self.email = self.user.email
            self.name = self.user.fullname
            self.userID = self.user.user_id
        else:
            self.email = None
            self.name = None
            self.userID = None

        self.user_id = self.userID

    def user_as_dict(self):
        return {"auth_identifier": self.authenticated_identifier,
                "email": self.email,
                "name": self.name}


def after_authentication(authenticated_identifier, method):
    """Called after a user has provided a validated ID (openid or peresons)

    method either openid, or persona

    """
    dolog("INFO", "in after auth - %s %s" % (authenticated_identifier, method))
    dolog("INFO", "before session - %s" % repr(session))
    userobj = get_user_from_identifier(authenticated_identifier)

    ##set session, set g, set JS
    #session update?
    if method not in ('openid', 'persona'): raise Rhaptos2Error("Incorrect method of authenticating ID")
    session['authenticated_identifier'] = authenticated_identifier
    g.user = userobj

    dolog("INFO", "ALLG:%s" % repr(g))
    dolog("INFO", "ALLG.user:%s" % repr(g.user))
    dolog("INFO", "AFTER session %s" % repr(session))

    return userobj



def get_user_from_identifier(authenticated_identifier):
    """
    """
    #supposed to be memcache lookup
    return User(authenticated_identifier)


def store_identity(identity_url, **kwds):
    """no-op but would push idneity to backend storage ie memcvache """
    pass

def retrieve_identity(identity_url, **kwds):
    """no-op but would pull idneity to backend storage ie memcvache """
    pass



def whoami():
    '''
    return the identity url stored in session cookie
    TODO: store the userid in session cookie too ?

    .. todo:: session assumes there will be a key of 'authenticated_identifier'
    .. todo:: I always go and look this up - decide if this is sensible / secure
    .. todo:: use secure cookie

    I really need to think about session cookies. Default for now.
    '''
    dolog("INFO", "Whoami called", caller=whoami)
    if 'authenticated_identifier' in session:
        user = Identity(session['authenticated_identifier'])
        g.user_id = user.userID
        return user
    else:
        callstatsd("rhaptos2.repo.notloggedin")
        g.user_id = None
        g.user = None
        return None
        #is this alwasys desrireed?


## .. todo:: why is there a view in here??
@app.route("/whoami/", methods=['GET'])
def whoamiGET():
    '''

    returns
    Either 401 if OpenID not available or JSON document of form

    {"openid_url": "https://www.google.com/accounts/o8/id?id=AItOawlWRa8JTK7NyaAvAC4KrGaZik80gsKfe2U",
     "email": "Not Implemented",
     "name": "Not Implemented"}

    I expect we shall want to shift to a User.JSON document...


    '''
    ### todo: return 401 code and let ajax client put up login.
    user =  whoami()

    if user:
        d = user.user_as_dict()
        jsond = asjson(d)
        ### make decorators !!!
        resp = flask.make_response(jsond)
        resp.content_type='application/json'
        resp = apply_cors(resp)
        return resp
    else:
        return("Not logged in", 401)


def apply_cors(resp):
    '''  '''
    resp.headers["Access-Control-Allow-Origin"]= "*"
    resp.headers["Access-Control-Allow-Credentials"]= "true"
    return resp



def add_location_header_to_response(fn):
    ''' add Location: header

        from: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
        For 201 (Created) responses, the Location is that of the new resource which was created by the request


    decorator that assumes we are getting a flask response object'''

    resp = fn()
    resp.headers["Location"]= "URL NEEDED FROM HASHID"



#@property ## need to evolve a class here I feel...
def userspace():
    ''' '''
    userspace = app.config['repodir']

    if os.path.isdir(userspace):
        return userspace
    else:
       try:
           os.makedirs(userspace)
           return userspace
       except Exception,e:
           raise Rhaptos2Error('cannot create repo \
                                or userspace %s - %s' % (
                                 userspace, e))


def callstatsd(dottedcounter):
    ''' '''
    # Try to call logging. If not connected to a network this throws
    # "socket.gaierror: [Errno 8] nodename nor servname provided, or not known"
    try:
        c = statsd.StatsClient(app.config['globals']['bamboo_global']['statsd_host'],
                           int(app.config['globals']['bamboo_global']['statsd_port']))
        c.incr(dottedcounter)
        #todo: really return c and keep elsewhere for efficieny I suspect
    except:
        pass


def asjson(pyobj):
    '''just placeholder


    >>> x = {'a':1}
    >>> asjson(x)
    '{"a": 1}'

    '''
    return json.dumps(pyobj)

def gettime():
    return datetime.datetime.today().isoformat()

def delete_module(modname):
    '''delete reqd module


    '''

    folder = userspace()
    try:
        result = files.rhaptos_file_delete(modname, folder)
    except IOError, e:
        raise e
    return ''


def fetch_module(modname):
    ''' retrieve module by name from current user store.

    '''

    folder = userspace()
    json = open(os.path.join(folder, str(modname))).read()
    return json

def mod_from_json(jsondict):
    """Given a JSON dict from a POST / PUT request
       create and return a NodeDoc class """

    n = security.NodeDoc()
    n.load_from_djson(jsondict)
    return n

def mod_from_file(uid):
    """ Given a uuid, pull the currently stored
        and return as NodeDoc object"""
    n = security.NodeDoc()
    n.load_from_file(uid)
    return n

def create_or_update_module(uuid, data):
    """Given a `uuid` and json `data`, this function will create or update the
    stored conten and metadata.
    """
    filename = uuid
    file_path = os.path.join(userspace(), filename)
    stored_data = {}
    # Grab the existing data if it exists.
    if os.path.exists(file_path):
        with open(file_path) as f:
            stored_data = json.load(f)
    # Update the data and write it back to disk.
    stored_data.update(data)
    with open(file_path, 'w') as f:
        json.dump(stored_data, f)

def create_or_update_metadata(uuid, data):
    """Given a `uuid` and json `data`, this function will create or update the
    stored metadata.
    """
    filename = "{0}.metadata".format(uuid)
    file_path = os.path.join(userspace(), filename)
    stored_data = {}
    # Grab the existing data if it exists.
    if os.path.exists(file_path):
        with open(file_path) as f:
            stored_data = json.load(f)
    # Update the data and write it back to disk.
    stored_data.update(data)
    with open(file_path, 'w') as f:
        json.dump(stored_data, f)

def get_metadata(uuid):
    """Given a `uuid`, return the metadata information in a json format."""
    filename = "{0}.metadata".format(uuid)
    file_path = os.path.join(userspace(), filename)
    try:
        with open(file_path) as f:
            data = json.load(f)
    except IOError:
        data = {}
    return json.dumps(data)

def _xxx_get_resource_metadata(hash):
    """XXX Temporary function to return the metadata for a specific resource.
    This is temporary because we are working with the file system as storage.
    """
    metadata_file = os.path.join(RESOURCES_DIR_PATH, 'metadata')
    with open(METADATA_FILE_PATH, 'r') as f:
        metadata = json.load(f)
    value = {'id': hash}
    value.update(metadata[hash])
    return value

def _xxx_set_resource_metadata(hash, mimetype, **kwargs):
    """XXX Temporary function to set the metadata for a specific resource.
    This is temporary because we are working with the file system as storage.
    """
    metadata = {}
    if os.path.exists(METADATA_FILE_PATH):
        with open(METADATA_FILE_PATH, 'r') as f:
            metadata = json.load(f)

    value = {'mimetype': mimetype}
    value.update(kwargs)
    metadata[hash] = value
    with open(METADATA_FILE_PATH, 'w') as f:
        f.write(json.dumps(metadata))

def create_or_update_resource(data, mimetype, name=None):
    """Given a `uuid` and the file like object as `data`,
    store the data. A mimetype should be provided to reliably adapt the
    data at a later time. Optionally, a human readable `name` can be given.
    with an optional `name`.
    Information about the stored upload is returned.
    """
    data = data.read()
    id = filename = hashlib.sha1(data).hexdigest()
    file_path = os.path.join(RESOURCES_DIR_PATH, filename)

    # Create the containing directory if necessary.
    if not os.path.exists(RESOURCES_DIR_PATH):
        os.mkdir(RESOURCES_DIR_PATH)

    # Store the metadata about the resource metadata
    _xxx_set_resource_metadata(id, mimetype=mimetype, name=name)

    # Store the file data.
    with open(file_path, 'wb') as f:
        f.write(data)
    return _xxx_get_resource_metadata(id)

def obtain_resource(id):
    """Given a `uuid` and a `filename`, return the contents of the
    resource as a file like object / stream.
    """
    filename = id
    file_path = os.path.join(RESOURCES_DIR_PATH, filename)
    metadata = _xxx_get_resource_metadata(id)
    return (open(file_path, 'rb'), metadata,)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
