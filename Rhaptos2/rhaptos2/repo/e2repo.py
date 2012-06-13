#!/usr/local/bin/python
#! -*- coding: utf-8 -*-


from flask import Flask, g, request, redirect, url_for
import datetime
import reflector
import datetime
import md5, random
import os, sys
import flask
import statsd
import json
from functools import wraps

from rhaptos2 import conf
from rhaptos2 import log
from rhaptos2 import exceptions

#return a dict of conf from a .ini file
confd = conf.get_config()

app = Flask(__name__)
REPO = '/tmp/repo' #conf.remote_e2repo





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



#from logging import FileHandler
#fh = FileHandler(filename=os.path.join(REPO, 'e2repo.log'))
lg = log.get_rhaptos2Logger('rhaptos2_e2repo')
app.logger.addHandler(lg)

def whoami():
    '''Not too sure how I will work this but I need a user, OpenID
  
    THis is hard coded to testuser@cnx.org'''
    return 'testuser@cnx.org'

def getfilename(modulename, REPO=REPO):

    '''find all files with this name, test.1 etc, then sort and find
    next highest numnber
  
    >>> getfilename('test', REPO='/tmp')
    'test.0'


    '''
    app.logger.info('+++++' + REPO)
    userdir = os.path.join(REPO, whoami())
    try:
        allfiles = [f for f in os.listdir(userdir) if 
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
    folder = os.path.join(REPO, username)
    json = open(os.path.join(folder, str(hashid))).read()    
    return json 

def store_module(fulltext, jsondict):
    '''recieve and write to disk the json dict holding the text edtited

    '''


    myhash = getfilename(jsondict['modulename'])

    folder = whoami()
    pathtofolder = os.path.join(REPO, folder)

    app.logger.info('******************** %s %s ' % (myhash, folder))
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

#@apply_cors
@app.route("/module/", methods=['POST'])
def modulePOST():
    app.logger.info('POST CALLED')
    callstatsd('rhaptos2.e2repo.module.POST')
    try:

        html5 = request.form['moduletxt']
        d = json.loads(html5)
        
        app.logger.info(repr(d))
                      
        myhash = store_module(html5, d)


    except Exception, e:

        app.logger.error(str(e))
        app.logger.info(repr(d))
        raise(e)

    s = asjson({'hashid':myhash})
    resp = flask.make_response(s)    
    resp.content_type='application/json'
    resp.headers["Access-Control-Allow-Origin"]= "*"

    return resp


@app.route("/workspace/", methods=['GET'])
def workspaceGET():
    ''' '''
    f = os.listdir(os.path.join(REPO, whoami()))
    json_dirlist = json.dumps(f)
    resp = flask.make_response(json_dirlist)    
    resp.content_type='application/json'
    resp.headers["Access-Control-Allow-Origin"]= "*"

    callstatsd('rhaptos2.e2repo.workspace.GET')
    return resp


@app.route("/module/<mhash>", methods=['GET'])
def moduleGET(mhash):
    app.logger.info('getcall %s' % mhash)
    callstatsd('rhaptos2.e2repo.module.GET')
    try:
        jsonstr = fetch_module(whoami(), mhash)
    except Exception, e:
        raise e

    resp = flask.make_response(jsonstr)    
    resp.headers["Access-Control-Allow-Origin"]= "*"
    return resp

@app.route("/module/", methods=['DELETE'])
def moduleDELETE():
    return 'You DELETEed @ %s' %  gettime() 

@app.route("/module/", methods=['PUT'])
def modulePUT():
    return 'You PUTed @ %s' %  gettime() 



@app.route("/version/", methods=["GET"])
#@resp_as_json()
def versionGET():
    ''' '''
    s = asjson(confd['rhaptos2_current_version'])
    resp = flask.make_response(s)    
    resp.content_type='application/json'
    resp.headers["Access-Control-Allow-Origin"]= "*"

    return resp


### Below are for test /dev only.
@app.route("/crash/", methods=["GET"])
def crash():
    ''' '''
    if app.debug == True:
        app.logger.info('crash command called.')
        raise exceptions.Rhaptos2Error('Crashing on demand')


@app.route("/burn/", methods=["GET"])
def burn():
    ''' '''
    if app.debug == True:
        app.logger.info('burn command called - dying hard with os._exit')
        #sys.exit(1)
        #Flask traps sys.exit (threads?)
        os._exit(1) #trap _this_

if __name__ == "__main__":
    import doctest
    doctest.testmod()
