#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012-13
# This software is subject to
# the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
###


import datetime
import os
import statsd
import json
import pprint

from rhaptos2.common.err import Rhaptos2Error
from rhaptos2.repo import get_app, dolog

import flask
from flask import request, g, session
from flaskext.openid import OpenID
import requests

### THis header is where we put the authenticated ID
HTTPHEADER_STORING_USERAUTH = "REMOTE_AUTHID"
HTTPHEADER_STORING_USERURI = "REMOTE_USERURI"


app = get_app()

app.config.update(
    SECRET_KEY=app.config['openid_secretkey'],
    DEBUG=app.debug
)
RESOURCES_DIR_PATH = os.path.join(app.config['repodir'],
                                  'resources')
METADATA_FILE_PATH = os.path.join(RESOURCES_DIR_PATH,
                                  'resource-metadata')

# setup flask-openid
oid = OpenID(app)


'''

Wanted:

onbjects to standarse the things like username lookups,
username to directory, etc etc

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

        .. todo::
           this is stubbed out - it should always go to user
           dbase and lookup fromidentifer

        .. todo::
           what should I do if user dbase is unavilable???

        .. todo::
           totally unsafe laoding of user details

        """

        payload = {'user': authenticated_identifier}

        user_server_url = app.config['globals'][
            u'userserver'].replace("/user", "/openid")

        dolog("INFO", "user info - from url %s and query string %s" %
                      (user_server_url, repr(payload)))

        try:
            r = requests.get(user_server_url, params=payload)
            userdetails = r.json()
        except Exception, e:
            #.. todo:: not sure what to do here ... the user dbase is down
            dolog("INFO", e)
            userdetails = None

        dolog("INFO", "Got back %s " % str(userdetails))
        if userdetails and r.status_code == 200:
            ### todo:: better self update
            dolog("INFO", type(userdetails))
            dolog("INFO", repr(userdetails))
            self.__dict__.update(userdetails)
        else:
            ### we have a authenticated user but no name.
            ### todo:: force user to give us their details for user db
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
    """THis 'owns' User - its rubbish to have two clases doing the
        same basic thing.  I should merge them but need longer to test
        (demo day)

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
                "id": self.userID,
                "email": self.email,
                "name": self.name}


def after_authentication(authenticated_identifier, method):
    """Called after a user has provided a validated ID (openid or peresons)

    method either openid, or persona

    """
    dolog("INFO", "in after auth - %s %s" % (authenticated_identifier, method))
    dolog("INFO", "before session - %s" % repr(session))
    userobj = get_user_from_identifier(authenticated_identifier)

    # set session, set g, set JS
    # session update?
    if method not in ('openid', 'persona'):
        raise Rhaptos2Error("Incorrect method of authenticating ID")
    session['authenticated_identifier'] = authenticated_identifier
    g.user = userobj

    dolog("INFO", "ALLG:%s" % repr(g))
    dolog("INFO", "ALLG.user:%s" % repr(g.user))
    dolog("INFO", "AFTER session %s" % repr(session))

    return userobj


def get_user_from_identifier(authenticated_identifier):
    """
    """
    # supposed to be memcache lookup
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

    .. todo::
       session assumes there will be a key of 'authenticated_identifier'

    .. todo::
       I always go and look this up - decide if this is sensible / secure

    .. todo::
       use secure cookie

    I really need to think about session cookies. Default for now.


    ..  todo:: document fajkeuserID
    '''
    dolog("INFO", "Whoami called", caller=whoami)

    if HTTPHEADER_STORING_USERURI in request.headers and app.debug is True:
        fakeuserid = request.headers.get(HTTPHEADER_STORING_USERURI)
        g.user_id = fakeuserid
        return Identity(fakeuserid)

    elif (HTTPHEADER_STORING_USERAUTH in request.headers
          and app.debug is True
          and 'authenticated_identifier' not in session):
        fakeuserauth = request.headers.get(HTTPHEADER_STORING_USERAUTH)
        after_authentication(fakeuserauth, "openid")
        return Identity(fakeuserauth)

    elif 'authenticated_identifier' in session:
        user = Identity(session['authenticated_identifier'])
        g.user_id = user.userID
        return user
    else:
        callstatsd("rhaptos2.repo.notloggedin")
        g.user_id = None
        g.user = None
        return None
        # is this alwasys desrireed?


## .. todo:: why is there a view in here??
@app.route("/me/", methods=['GET'])
def whoamiGET():
    '''

    returns
    Either 401 if OpenID not available or JSON document of form

    {"openid_url": "https://www.google.com/accounts/o8/id?id=AItOawlWRa8JTK7NyaAvAC4KrGaZik80gsKfe2U",  # noqa
     "email": "Not Implemented",
     "name": "Not Implemented"}

    I expect we shall want to shift to a User.JSON document...


    '''
    ### todo: return 401 code and let ajax client put up login.
    user = whoami()

    if user:
        d = user.user_as_dict()
        jsond = asjson(d)
        ### make decorators !!!
        resp = flask.make_response(jsond)
        resp.content_type = 'application/json'
        resp = apply_cors(resp)
        return resp
    else:
        return("Not logged in", 401)


def apply_cors(resp):
    '''  '''
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Credentials"] = "true"
    return resp


def add_location_header_to_response(fn):
    '''add Location: header

        from: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
        For 201 (Created) responses, the Location is that of the new
        resource which was created by the request


    decorator that assumes we are getting a flask response object

    '''

    resp = fn()
    resp.headers["Location"] = "URL NEEDED FROM HASHID"


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
        except Exception, e:
            raise Rhaptos2Error('cannot create repo \
                                or userspace %s - %s' % (
                                userspace, e))


def callstatsd(dottedcounter):
    ''' '''
    # Try to call logging. If not connected to a network this throws
    # "socket.gaierror: [Errno 8] nodename nor servname provided, or not known"
    try:
        c = statsd.StatsClient(app.config['globals']['statsd_host'],
                               int(app.config['globals']['statsd_port']))
        c.incr(dottedcounter)
        # todo: really return c and keep elsewhere for efficieny I suspect
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()

