#!/usr/local/bin/python
#! -*- coding: utf-8 -*-


from flask import Flask, render_template, request, g, session, flash, \
     redirect, url_for, abort


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

from rhaptos2.repo import app  #circular reference ? see http://flask.pocoo.org/docs/patterns/packages/
from rhaptos2.repo.model import * #asjson, whoami, gettime, callstatsd
#return a dict of conf from a .ini file
confd = conf.get_config()


########################### views

@app.route('/')
def index():
    return render_template('index.html')


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
    f = os.listdir(os.path.join(confd['remote_e2repo'], whoami()))
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
