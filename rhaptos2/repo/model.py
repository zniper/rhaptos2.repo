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

from rhaptos2 import conf
from rhaptos2 import log
from rhaptos2.exceptions import Rhaptos2Error

#return a dict of conf from a .ini file
confd = conf.get_config()


#REPO = '/tmp/repo' #conf.remote_e2repo

from rhaptos2.repo import app



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


def add_location_header_to_response(fn):
    ''' add Location: header 

        from: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
        For 201 (Created) responses, the Location is that of the new resource which was created by the request


    decorator that assumes we are getting a flask response object'''

    resp = fn()
    resp.headers["Location"]= "URL NEEDED FROM HASHID"


def whoami():
    '''Not too sure how I will work this but I need a user, OpenID
  
    THis is hard coded to testuser@cnx.org'''
    return 'testuser@cnx.org'

def userspace():
    ''' '''
    user_email = whoami()
    userspace = os.path.join(confd['remote_e2repo'],
                             user_email)
    if os.path.isdir(userspace):
        return userspace
    else:
       try:
           os.mkdirs(userspace)
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

def fetch_module(username, hashid):
    ''' '''
     
    folder = userspace()
    json = open(os.path.join(folder, str(hashid))).read()    
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

