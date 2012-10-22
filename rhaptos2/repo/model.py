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
import flask
import statsd
import json
from functools import wraps
import urlparse
import pprint

from rhaptos2.common import conf
from rhaptos2.common import log
from rhaptos2.common.err import Rhaptos2Error
from rhaptos2.repo import app, dolog
from rhaptos2.repo import files, security

from flask import Flask, render_template, request, g, session, flash, \
     redirect, url_for, abort
from flaskext.openid import OpenID
import memcache
import requests
import urllib


#app = get_app()
app.config.update(
    SECRET_KEY = app.config['rhaptos2repo_openid_secretkey'],
    DEBUG = True
)

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
        """initialise from json doc

        .. todo:: this is stubbed out - it should always go to user dbase and lookup fromidentifer
        .. todo:: what should I do if user dbase is unavilable???
        .. todo:: totally unsafe laoding of user details

        """
#        try:
#        safe_auth_identifier = urllib.quote_plus(authenticated_identifier)
        payload = {'user':authenticated_identifier}

        user_server_url = app.config['bamboo_userserver']

        dolog("INFO", "requesting user info - from url %s and query string %s" %
                       (user_server_url, repr(payload)))

        r = requests.get(user_server_url, params=payload)
        userdetails = r.json
        dolog("INFO", str(userdetails))
        self.__dict__.update(r.json)
        for k in r.json['details']:
            self.__dict__[k] = r.json['details'][k]

    def __repr__(self):
        return pprint.pformat(self.__dict__)

#        except Exception, e:
#            dolog("ERROR", "Failed in User class %s" % str(e))
#            self.userID = "Err1"


    def load_JSON(self, jsondocstr):
        """ parse and store details of properly formatted JSON doc

        """
        user_dict = json.loads(jsondocstr)
        self.__dict__.update(user_dict)




class Identity(object):
    def __init__(self, authenticated_identifier):
        """placeholder - we want to store identiy values somewhere but
           sqlite is limited to one server, so need move to network
           aware storage

        .. todo:: rename FUllNAme to fullname
        .. todo:: in fact fix whole user details


        todo: combine identiy and USer into one class !
        """

        self.authenticated_identifier = authenticated_identifier
        self.user = get_user_from_identifier(authenticated_identifier)
        if self.authenticated_identifier:
            self.email = self.user.email
            self.name = self.user.FullName
            self.userID = self.user.id
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
        d = identity.user_as_dict()
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
    userspace = app.config['rhaptos2repo_repodir']

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
    c = statsd.StatsClient(app.config['rhaptos2repo_statsd_host'],
                       int(app.config['rhaptos2repo_statsd_port']))
    c.incr(dottedcounter)
    #todo: really return c and keep elsewhere for efficieny I suspect


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



if __name__ == '__main__':
    import doctest
    doctest.testmod()
