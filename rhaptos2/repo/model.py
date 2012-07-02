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
from rhaptos2.repo import files

from flask import Flask, render_template, request, g, session, flash, \
     redirect, url_for, abort
from flaskext.openid import OpenID

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


app.config.update(
    DATABASE_URI = confd['openid_userdb_uri'],
    SECRET_KEY = confd['openid_secretkey'],
    DEBUG = True
)

# setup flask-openid
oid = OpenID(app)

# setup sqlalchemy
engine = create_engine(app.config['DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    email = Column(String(200))
    openid = Column(String(200))

    def __init__(self, name, email, openid):
        self.name = name
        self.email = email
        self.openid = openid




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


def apply_cors(fn):
    '''decorator to apply the correct CORS friendly header '''

    def decorator():
        resp = fn()
        resp.headers["Access-Control-Allow-Origin"]= "*"
        return resp
    return decorator


def whoami():
    '''Not too sure how I will work this but I need a user, OpenID
  
    migrate to http://flask.pocoo.org/snippets/51/

    THis is hard coded to testuser@cnx.org'''


    app.logger.info('+++++ session dict' + repr(session.__dict__) )
    app.logger.info('+++++ app config' + repr(app.config) )

    if not g.user:
        app.logger.info('+++++ No session?' + repr(g) )
        raise Rhaptos2Error('Not logged in - trap this?')
    else:
        return [g.user.email, g.user.name]

def workspace_path():
    ''' NOT SAFE IN ANY WAY'''
    email =  whoami()[0]
    return os.path.join(REPO, email)

@app.route("/whoami/", methods=['GET'])
def whoamiGET():
    ''' '''
    ### todo: return 401 code and let ajax client put up login.
    try:
        email, name =  whoami()
    except Rhaptos2Error:
        email = ''
        name = '<a href="">login</a>'

    d = {'user_email': email,
         'user_name': name}
    jsond = asjson(d)
    ### make decorators !!!
    resp = flask.make_response(jsond)    
    resp.content_type='application/json'
    resp = apply_cors(resp)

    return resp

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


# def whoami():
#     '''Not too sure how I will work this but I need a user, OpenID
  
#     THis is hard coded to testuser@cnx.org'''
#     return 'testuser@cnx.org'

#@property ## need to evolve a class here I feel...
def userspace():
    ''' '''
    user_email = whoami()[0]
    userspace = os.path.join(confd['remote_e2repo'],
                             user_email)
    if os.path.isdir(userspace):
        return userspace
    else:
       try:
           os.makedirs(userspace)
           return userspace 
       except Exception,e:
           raise Rhaptos2Error('cannot create repo or userspace %s - %s' % (userspace, e))
           
    
def getfilename(modulename):

    '''find all files with this name, test.1 etc, then sort and find
    next highest numnber
  
    >>> getfilename('test', REPO='/tmp')
    'test.0'


    '''
    app.logger.info('+++++' + confd['remote_e2repo'])

    try:
        allfiles = [f for f in os.listdir(userspace()) if 
                 os.path.splitext(os.path.basename(f))[0] == modulename]
    except OSError, IOError:
        allfiles = []
 
    if len(allfiles) == 0:
        return '%s.%s' % (modulename, 0)
    else:
        return '%s.%s' % (modulename, len(allfiles))

    
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

def store_module(fulltext, jsondict):
    '''recieve and write to disk the json dict holding the text edtited

    '''
    myhash = getfilename(jsondict['modulename'])
    pathtofolder = userspace()

    app.logger.info('******************** %s %s ' % (myhash, pathtofolder))
    newfile = os.path.join(pathtofolder, myhash)
    app.logger.info(newfile)

    try:
        open(newfile,'w').write(fulltext)    
    except:
        #it will be far more efficient to write folder on first exception than check everytime
        os.mkdir(pathtofolder)
        app.logger.error('%s path did not exist - creating' % pathtofolder) 
        open(os.path.join(pathtofolder, str(myhash)),'w').write(fulltext)    
        
       
    return myhash

