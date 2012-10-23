# -*- coding: utf-8 -*-
"""views.py - View code for the repository application.

Author: Paul Brian
(C) 2012 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
import os
import sys
import datetime
import md5
import random
import json
from functools import wraps
import uuid
import requests
import pprint
import statsd
import flask
from flask import (
    Flask, render_template,
    request, g, session, flash,
    redirect, url_for, abort,
    )

from rhaptos2.common import log, err, conf
from rhaptos2.repo import app, dolog, model, security, VERSION



#@app.before_request
#def requestid():
#    g.requestid = uuid.uuid4()
#    g.request_id = g.requestid

########################### views


def apply_cors(fn):
    '''decorator to apply the correct CORS friendly header

       I am assuming all view functions return
       just text ..  hmmm
    '''
    @wraps(fn)
    def newfn(*args, **kwds):
        resp = flask.make_response(fn(*args, **kwds))
        resp.content_type='application/json'
        resp.headers["Access-Control-Allow-Origin"]= "*"
        resp.headers["Access-Control-Allow-Credentials"]= "true"
        return resp

    return newfn

@app.route('/conf.js')
def confjs():
    resp = flask.make_response(render_template("conf.js", confd=app.config))
    resp.content_type='application/javascript'
    return resp

@app.route('/')
def index():
    dolog("INFO", "THis is request %s" % g.requestid)
    return render_template('index.html', confd=app.config)

@app.route("/module/", methods=['PUT'])
def modulePUT():
    dolog("INFO", 'MODULE PUT CALLED', caller=modulePUT, statsd=['rhaptos2.repo.module.PUT',])
    try:


        d = request.json
        if d['uuid'] == u'':
            return ("PUT WITHOUT A UUID" , 400)

        current_nd = model.mod_from_file(d['uuid'])
        current_nd.load_from_djson(d) #this checks permis
        uid = current_nd.uuid
        current_nd.save()

    except Exception, e:
        raise(e)

    s = model.asjson({'hashid':uid})
    resp = flask.make_response(s)
    resp.content_type='application/json'
    resp.headers["Access-Control-Allow-Origin"]= "*"

    return resp




@app.route("/module/", methods=['POST'])
@apply_cors
def modulePOST():
    """
    """
    dolog("INFO", 'A Module POSTed', caller=modulePOST, statsd=['rhaptos2.repo.module.POST',])

    d = request.json
    if d['uuid'] != u'':
        return ("POSTED WITH A UUID" , 400)
    else:
        d['uuid'] = None

    #app.logger.info(repr(d))
    ### maybe we know too much about nodedocs
    nd = model.mod_from_json(d)
    uid = nd.uuid
    nd.save()
    del(nd)

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
        json_dirlist = json.dumps([])
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
    dolog("INFO", 'MODULE GET CALLED on %s' % modname, caller=moduleGET, statsd=['rhaptos2.repo.module.GET',])
    try:
        jsonstr = model.fetch_module(modname)
    except Exception, e:
        raise e

    resp = flask.make_response(jsonstr)
    resp.content_type='application/json'
    resp.headers["Access-Control-Allow-Origin"]= "*"
    return resp

@app.route("/module/<modname>", methods=['DELETE'])
def moduleDELETE(modname):
    '''support deletion of a module

    200 - delete file successful                                                                                             202 - queued for deletion
    404 - no such file found                                                                                                 '''

    status_code = 200
    headers = []

    dolog("INFO", 'DELETE CALLED on %s' % modname, caller=moduleDELETE, statsd=['rhaptos2.repo.module.DELETE',])
    try:
        jsonstr = model.delete_module(modname)
    except IOError, e:
        status_code = 404

    resp = flask.make_response(jsonstr)
    resp.status_code = status_code
    resp.headers["Access-Control-Allow-Origin"]= "*"
    return resp

@app.route("/module/<modname>/metadata", methods=['POST', 'PUT'])
@apply_cors
def post_metadata(modname):
    """Receive posted data that will creator or update the metadata storage
    for a module.
    """
    # XXX 'modname' is used for consistancy, but it's not ideal, since
    #     the value isn't actually a module name.
    uuid = modname
    data = request.json
    model.create_or_update_metadata(uuid, data)

    resp = flask.make_response()
    resp.status_code = 200
    return resp


@app.route("/version/", methods=["GET"])
#@resp_as_json()
def versionGET():
    ''' '''
    s = VERSION
    resp = flask.make_response(s)
    resp.content_type='application/json'
    resp.headers["Access-Control-Allow-Origin"]= "*"

    return resp


### Below are for test /dev only.
@app.route("/crash/", methods=["GET"])
def crash():
    ''' '''
    if app.debug == True:
        dolog("INFO", 'crash command called', caller=crash, statsd=['rhaptos2.repo.crash',])
        raise exceptions.Rhaptos2Error('Crashing on demand')


@app.route("/burn/", methods=["GET"])
def burn():
    ''' '''
    if app.debug == True:
        dolog("INFO", 'burn command called - dying hard with os._exit'
                      , caller=crash, statsd=['rhaptos2.repo.crash',])
        #sys.exit(1)
        #Flask traps sys.exit (threads?)
        os._exit(1) #trap _this_


################ Admin-y stuff
@app.route("/admin/config/", methods=["GET",])
def admin_config():
    """View the config we are using

    Clearly quick and dirty fix.
    Should create a common library for rhaptos2 and web framrwoe
    """
    outstr = "<table>"
    for k in sorted(app.config.keys()):
        outstr += "<tr><td>%s</td> <td>%s</td></tr>" % (str(k), str(app.config[k]))
    outstr += "</table>"


    return outstr

################ openid views - from flask


@app.before_request
def before_request():
    g.user = model.whoami()


@app.after_request
def after_request(response):
#    model.db_session.remove()
    return response

# XXX A temporary fix for the openid images.
@app.route('/images/openid-providers-en.png')
def temp_openid_image_url():
    """Provides a (temporary) fix for the openid images used
    on the login page.
    """
    # Gets around http://openid-selector.googlecode.com quickly
    resp = flask.redirect('/static/img/openid-providers-en.png')
    return resp

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

    """

#    session['openid'] = resp.identity_url
#    model.store_identity(resp.identity_url,
#                       name=resp.fullname or resp.nickname,
#                       email=resp.email)

    model.after_authentication(resp.identity_url, 'openid')
#    user = model.whoami()#returns Identity object

#    if user is not None:
#        flash(u'Successfully signed in')
#        g.user = user


    return redirect(model.oid.get_next_url())


@app.route('/logout')
def logout():
    session.pop('openid', None)
    flash(u'You have been signed out')
    return redirect(model.oid.get_next_url())


##############
@app.route('/persona/logout/', methods=['POST'])
def logoutpersona():
    dolog("INFO", "logoutpersona")
    return "Yes"

@app.route('/persona/login/', methods=['POST'])
def loginpersona():
    """Taken mostly from mozilla quickstart """
    dolog("INFO", "loginpersona")
    # The request has to have an assertion for us to verify
    if 'assertion' not in request.form:
        abort(400)

    # Send the assertion to Mozilla's verifier service.
    data = {'assertion': request.form['assertion'], 'audience': 'http://www.frozone.mikadosoftware.com:80'}
    resp = requests.post('https://verifier.login.persona.org/verify', data=data, verify=True)

    # Did the verifier respond?
    if resp.ok:
        # Parse the response
        verification_data = json.loads(resp.content)
        dolog("INFO", "Verified persona:%s" % repr(verification_data))


        # Check if the assertion was valid
        if verification_data['status'] == 'okay':
            # Log the user in by setting a secure session cookie
#            session.update({'email': verification_data['email']})
            model.after_authentication(verification_data['email'], 'persona')
            return resp.content

    # Oops, something failed. Abort.
    abort(500)
