#!/usr/local/bin/python
#! -*- coding: utf-8 -*-


from flask import Flask, render_template, request, g, session, flash, \
     redirect, url_for, abort


import datetime
import datetime
import md5, random
import os, sys
import flask
import statsd
import json
from functools import wraps

from rhaptos2.common import conf
from rhaptos2.common import log
from rhaptos2.common.err import Rhaptos2Error

#return a dict of conf from a .ini file
confd = conf.get_config('rhaptos2')


from rhaptos2.repo import app
from rhaptos2.repo import files, security

from flask import Flask, render_template, request, g, session, flash, \
     redirect, url_for, abort
from flaskext.openid import OpenID

#from sqlalchemy import create_engine, Column, Integer, String
#from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy.ext.declarative import declarative_base


app.config.update(
    DATABASE_URI = confd['openid_userdb_uri'],
    SECRET_KEY = confd['openid_secretkey'],
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
import memcache


class User(object):
    """
    Is the user from memcache

    Not sure there is a clear diff between Identity and User
    """

    def __init__(self, jsondoc):
        """initialise from json doc """
        self.userID = "org.cnx.user.f9647df6-cc6e-4885-9b53-254aa55a3383"
  
class Identity(object):
    def __init__(self, openid_url):
        """placeholder - we want to store identiy values somewhere
           but sqlite is limited to one server, so need move to network aware storage
        """
        self.openid_url = openid_url
        self.user = get_user_from_openid(openid_url)
        if self.openid_url:
            self.email = 'your email' 
            self.name = 'your name'
            self.userID = self.user.userID
        else:
            self.email = None
            self.name = None
            self.userID = None

def get_user_from_openid(openid_url):
    """
    """
    #supposed to be memcache lookup
    return User('')


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

    '''
    callstatsd("rhaptos2.repo.whoami")    
    app.logger.info('+++++ session dict' + repr(session.__dict__) )
    app.logger.info('+++++ app config' + repr(app.config) )

    if 'openid' in session:
        user = Identity(session['openid'])
        return user
    else:
        callstatsd("rhaptos2.repo.notloggedin")    
        return None
        #is this alwasys desrireed?


@app.route("/whoami/", methods=['GET'])
def whoamiGET():
    ''' '''
    ### todo: return 401 code and let ajax client put up login.
    identity =  whoami()
    
        
    if identity:
        d = identity.__dict__
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
    userspace =confd['remote_e2repo']

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
           
    
# def getfilename(modulename):

#     '''find all files with this name, test.1 etc, then sort and find
#     next highest numnber
  
#     >>> getfilename('test', REPO='/tmp')
#     'test.0'


#     '''
#     app.logger.info('+++++' + confd['remote_e2repo'])

#     try:
#         allfiles = [f for f in os.listdir(userspace()) if 
#                  os.path.splitext(os.path.basename(f))[0] == modulename]
#     except OSError, IOError:
#         allfiles = []
 
#     if len(allfiles) == 0:
#         return '%s.%s' % (modulename, 0)
#     else:
#         return '%s.%s' % (modulename, len(allfiles))

    
def callstatsd(dottedcounter):
    ''' '''
    c = statsd.StatsClient(confd['statsd_host'], int(confd['statsd_port']))
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



