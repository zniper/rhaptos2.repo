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
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import uuid
import requests
import pprint
import statsd
import flask
from flask import (
    Flask, render_template,
    request, g, session, flash,
    redirect, url_for, abort,
    send_from_directory
    )

from rhaptos2.common import log, err, conf
from rhaptos2.repo import get_app, dolog, model, security, VERSION
app = get_app()


@app.before_request
def requestid():
    g.requestid = uuid.uuid4()
    g.request_id = g.requestid

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


##### route thridparty static files



@app.route("/cdn/aloha/<path:filename>")
def serve_aloha(filename):
    """ serve static files for development purposes

    We would expect that these routes would be "overwritten" by say
    the front portion of the reverse proxy we expect flask to sit
    behind.  So these will only ever be called by requests
    during development, but the URL /cdn/aloha/... would still
    exist, possibly on a CDN, certainly a good cache server.


    """
    #os.path.isfile is checked by the below function in Flask.
    dolog("INFO", repr((app.config["aloha_staging_dir"], filename)))
    return send_from_directory(app.config["aloha_staging_dir"], filename)


@app.route("/cdn/js/<path:filename>/")
def serve_other_thirdpartyjs(filename):
    """ see :def:serve_aloha """
    dolog("INFO", repr((app.config["js_staging_dir"], filename)))
    return send_from_directory(app.config["js_staging_dir"], filename)


@app.route("/cdn/css/<path:filename>/")
def serve_other_thirdpartycss(filename):
    """ see :def:serve_aloha """
    dolog("INFO", repr((app.config["css_staging_dir"], filename)))
    return send_from_directory(app.config["css_staging_dir"], filename)

##### /thirdparty static files


@app.route('/conf.js')
def confjs():
    resp = flask.make_response(render_template("conf.js", confd=app.config))
    resp.content_type='application/javascript'
    return resp

@app.route('/')
def index():
    dolog("INFO", "THis is request %s" % g.requestid)
    return render_template('index.html', confd=app.config)


# Content GET, POST (create), and PUT (change)

@app.route("/content/<uuid>", methods=['GET'])
def moduleGET(uuid):
    dolog("INFO", 'MODULE GET CALLED on %s' % uuid, caller=moduleGET, statsd=['rhaptos2.repo.module.GET',])
    try:
        jsonstr = model.fetch_module(uuid)
    except Exception, e:
        raise e

    resp = flask.make_response(jsonstr)
    resp.content_type='application/json'
    resp.headers["Access-Control-Allow-Origin"]= "*"
    return resp


@app.route("/content/", methods=['POST'])
@apply_cors
def modulePOST():
    """
    """
    dolog("INFO", 'A Module POSTed', caller=modulePOST, statsd=['rhaptos2.repo.module.POST',])

    # Autogenerate a new ID for the new content
    uid = str(uuid.uuid4())

    d = request.json
    d['id'] = uid

    #app.logger.info(repr(d))
    ### maybe we know too much about nodedocs
    nd = model.mod_from_json(d)
    nd.save()
    del(nd)

    return uid


@app.route("/content/<uuid>", methods=['PUT'])
def modulePUT(uuid):
    dolog("INFO", 'MODULE PUT CALLED', caller=modulePUT, statsd=['rhaptos2.repo.module.PUT',])

    d = request.json

    current_nd = model.mod_from_file(uuid)
    current_nd.load_from_djson(d) #this checks permis
    current_nd.save()

    # FIXME: A response is not needed if the save is successful
    s = model.asjson({'hashid':uuid})
    resp = flask.make_response(s)
    resp.content_type='application/json'
    resp.headers["Access-Control-Allow-Origin"]= "*"

    return resp



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


@app.route("/resource/", methods=['POST', 'PUT'])
@apply_cors
def post_resource():
    """Receives file resource uploads."""
    file = request.files['upload']
    # FIXME We should use magic to determine the mimetype. See also,
    #       https://github.com/Connexions/rhaptos2.repo/commit/7452bee85ecbbbec66232f3c04e4f2e40d72be1c
    mimetype = file.mimetype
    metadata = model.create_or_update_resource(file.stream, mimetype)

    url = "/resource/{0}".format(metadata['id'])
    resp = flask.make_response(url)
    resp.status_code = 200
    return resp

@app.route("/resource/<id>/", methods=['GET'])
def get_resource(id):
    """Send the resource data in the response."""
    data_stream, metadata = model.obtain_resource(id)

    resp = flask.make_response(data_stream.read())
    # XXX No mime-type headers... The following content-type
    #     is strictly temporary.
    resp.content_type = metadata['mimetype']
    resp.status_code = 200
    return resp

@app.route("/keywords/", methods=["GET"])
def keywords():
    """Returns a list of keywords for the authenticated user."""
    # XXX We really need a database search here. With the current
    #     state of the storage (file system), we would need to open
    #     every module's keywords in order to compile a comprehensive
    #     list of available keywords created by the user.
    #     We should come back to this after we have created a storage
    #     that can be queried (e.g. a SQL database).
    XXX_JUNK_KEYWORDS = ("Quantum Physics", "Information Technology",
                         "Biology", "Anthropology", "Philosophy", "Psychology",
                         "Physics", "Socialogy", "Plumbing", "Engine Repair",
                         "Programming", "Window Washing", "Cooking", "Hunting",
                         "Fishing", "Surfing",
                         )
    resp = flask.make_response(json.dumps(XXX_JUNK_KEYWORDS))
    resp.status_code = 200
    resp.content_type = 'application/json'
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
    else:
        abort(404)

@app.route("/burn/", methods=["GET"])
def burn():
    ''' '''
    if app.debug == True:
        dolog("INFO", 'burn command called - dying hard with os._exit'
                      , caller=crash, statsd=['rhaptos2.repo.crash',])
        #sys.exit(1)
        #Flask traps sys.exit (threads?)
        os._exit(1) #trap _this_
    else:
        abort(404)

@app.route("/admin/config/", methods=["GET",])
def admin_config():
    """View the config we are using

    Clearly quick and dirty fix.
    Should create a common library for rhaptos2 and web framrwoe
    """
    if app.debug == True:
        outstr = "<table>"
        for k in sorted(app.config.keys()):
            outstr += "<tr><td>%s</td> <td>%s</td></tr>" % (str(k), str(app.config[k]))

        outstr += "</table>"


        return outstr
    else:
        abort(404)

################ openid views - from flask


@app.before_request
def before_request():
    g.user = model.whoami()


@app.after_request
def after_request(response):
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

    model.after_authentication(resp.identity_url, 'openid')
    return redirect(model.oid.get_next_url())


@app.route('/logout')
def logout():
    session.pop('openid', None)
    session.pop('authenticated_identifier', None)
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
    audience="http://%s" % app.config['www_server_name']
    data = {'assertion': request.form['assertion'], 'audience': audience }
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
