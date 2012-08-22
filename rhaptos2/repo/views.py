#!/usr/local/bin/python
#! -*- coding: utf-8 -*-


from flask import Flask, render_template, request, g, session, flash,   redirect, url_for, abort


import datetime
import md5, random
import os, sys
import flask
import statsd
import json
from functools import wraps


from rhaptos2.common import log
from rhaptos2.common import err
from rhaptos2.common import conf

from rhaptos2.repo import app  #circular reference ? see http://flask.pocoo.org/docs/patterns/packages/

from rhaptos2.repo import model, get_version, security


########################### views


def apply_cors(fn):
    '''decorator to apply the correct CORS
       friendly header 
       I am assuming all view functions return 
       just text ..  hmmm
    '''
    @wraps(fn)
    def newfn(*args, **kwds):
        resp = flask.make_response(fn())
        resp.content_type='application/json'
        resp.headers["Access-Control-Allow-Origin"]= "*"
        resp.headers["Access-Control-Allow-Credentials"]= "true"
        return resp

    return newfn



@app.route('/static/conf.js')
def confjs():
    return render_template("conf.js", confd=app.config)

@app.route('/')
def index():
    return render_template('index.html', build_tag=app.config['BUILD_TAG'], confd=app.config)

@app.route("/module/", methods=['PUT'])
def modulePUT():
    app.logger.info('MODULE PUT CALLED')
    model.callstatsd('rhaptos2.repo.module.PUT')
    try:
       

        d = request.json
        if d['uuid'] == u'': 
            return ("PUT WITHOUT A UUID" , 400)

        app.logger.info(repr(d))
        current_nd = model.mod_from_file(d['uuid'])       
        current_nd.load_from_djson(d) #this checks permis
        uid = current_nd.uuid
        current_nd.save()  
        


    except Exception, e:

        app.logger.error(str(e))

        raise(e)

    s = model.asjson({'hashid':uid})
    resp = flask.make_response(s)    
    resp.content_type='application/json'
    resp.headers["Access-Control-Allow-Origin"]= "*"

    return resp




@app.route("/module/", methods=['POST'])
@apply_cors
def modulePOST():
    app.logger.info('POST CALLED')
    model.callstatsd('rhaptos2.repo.module.POST')
    try:
       

        d = request.json
        if d['uuid'] != u'': 
            return ("POSTED WITH A UUID" , 400)
        else:
            d['uuid'] = None

        app.logger.info(repr(d))
        ### maybe we know too much about nodedocs
        nd = model.mod_from_json(d)
        uid = nd.uuid
        nd.save()
        del(nd)

    except Exception, e:

        app.logger.error(str(e))

        raise(e)


    s = model.asjson({'hashid':uid})
    return s


@app.route("/workspace/", methods=['GET'])
def workspaceGET():
    ''' '''
    ###TODO - should whoami redirect to a login page?
    ### yes the client should only expect to handle HTTP CODES
    ### compare on userID

    identity = model.whoami()
    if not identity:
        json_dirlist = []
    else: 
        w = security.WorkSpace(identity.userID)
        json_dirlist = json.dumps(w.annotatedfiles)
 
    resp = flask.make_response(json_dirlist)    
    resp.content_type='application/json'
    resp.headers["Access-Control-Allow-Origin"]= "*"

    model.callstatsd('rhaptos2.e2repo.workspace.GET')
    return resp


@app.route("/module/<modname>", methods=['GET'])
def moduleGET(modname):
    app.logger.info('getcall %s' % modname)
    model.callstatsd('rhaptos2.e2repo.module.GET')
    try:
        jsonstr = model.fetch_module(modname)
    except Exception, e:
        raise e

    resp = flask.make_response(jsonstr)    
    resp.headers["Access-Control-Allow-Origin"]= "*"
    return resp

@app.route("/module/<modname>", methods=['DELETE'])
def moduleDELETE(modname):
    '''support deletion of a module                                                                                       
                                                                                                                        
    200 - delete file successful                                                                                             202 - queued for deletion 
    404 - no such file found                                                                                                 '''

    status_code = 200
    headers = []

    app.logger.info('getcall %s' % modname)
    model.callstatsd('rhaptos2.e2repo.module.GET')
    try:
        jsonstr = model.delete_module(modname)
    except IOError, e:
        status_code = 404
    
    resp = flask.make_response(jsonstr)
    resp.status_code = status_code
    resp.headers["Access-Control-Allow-Origin"]= "*"
    return resp





@app.route("/version/", methods=["GET"])
#@resp_as_json()
def versionGET():
    ''' '''
    s = get_version()
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


################ openid views - from flask


@app.before_request
def before_request():
    g.user = model.whoami()


@app.after_request
def after_request(response):
#    model.db_session.remove()
    return response



@app.route('/login', methods=['GET', 'POST'])
@model.oid.loginhandler
def login():
    """Does the login via OpenID.  Has to call into `model.oid.try_login`
    to start the OpenID machinery.
    """
    # if we are already logged in, go back to were we came from
    if g.user is not None:
        return redirect(model.oid.get_next_url())
    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return model.oid.try_login(openid, ask_for=['email', 'fullname',
                                                  'nickname'])
    return render_template('login.html', next=model.oid.get_next_url(),
                           error=model.oid.fetch_error(),
                           confd=app.config)


@model.oid.after_login
def create_or_login(resp):
    """This is called when login with OpenID succeeded and it's not
    necessary to figure out if this is the users's first login or not.
    This function has to redirect otherwise the user will be presented
    with a terrible URL which we certainly don't want.
    """
    session['openid'] = resp.identity_url
    model.store_identity(resp.identity_url,
                       name=resp.fullname or resp.nickname,
                       email=resp.email)
    user = model.whoami()

    if user is not None:
        flash(u'Successfully signed in')
        g.user = user
        return redirect(model.oid.get_next_url())
    return redirect(model.oid.get_next_url())


@app.route('/logout')
def logout():
    session.pop('openid', None)
    flash(u'You have been signed out')
    return redirect(model.oid.get_next_url())