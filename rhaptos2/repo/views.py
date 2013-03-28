#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012-13
# This software is subject to
# the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
###


"""
views.py - View code for the repository application.

"""
import os
import json
from functools import wraps
try:
    from cStringIO import StringIO  # noqa
except ImportError:
    from StringIO import StringIO  # noqa

import uuid
import requests
import flask
from flask import (
    render_template,
    request, g, session, flash,
    redirect, abort,
    send_from_directory
)

from rhaptos2.repo import (get_app, dolog,
                           auth,
                           VERSION, model,
                           backend)
from rhaptos2.common.err import Rhaptos2Error

app = get_app()
backend.initdb(app.config)


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
        resp.content_type = 'application/json'
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Credentials"] = "true"
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
    # os.path.isfile is checked by the below function in Flask.
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
    resp.content_type = 'application/javascript'
    return resp


@app.route('/')
def index():
    dolog("INFO", "THis is request %s" % g.requestid)
    return render_template('index.html', confd=app.config)


# Content GET, POST (create), and PUT (change)
@app.route("/workspace/", methods=['GET'])
def workspaceGET():
    ''' '''
    # TODO - should whoami redirect to a login page?
    ### yes the client should only expect to handle HTTP CODES
    ### compare on userID

    identity = auth.whoami()
    if not identity:
        abort(403)
    else:
        wout = {}
        dolog("INFO", "Calling workspace with %s" % identity.userID)
        w = model.workspace_by_user(identity.userID)
        dolog("INFO", repr(w))
        ## w is a list of models (folders, cols etc).
        ## it would require some flattening or a JSONEncoder but we just want short form for now
        short_format_list = [{"id":i.id_, "title":i.title, "mediaType":i.mediaType} for i in w]
        flatten = json.dumps(short_format_list)

    resp = flask.make_response(flatten)
    resp.content_type = 'application/json'
    resp.headers["Access-Control-Allow-Origin"] = "*"

    auth.callstatsd('rhaptos2.e2repo.workspace.GET')
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
    resp.content_type = 'application/json'
    resp.headers["Access-Control-Allow-Origin"] = "*"

    return resp


### Below are for test /dev only.
@app.route("/crash/", methods=["GET"])
def crash():
    ''' '''
    if app.debug:
        dolog("INFO", 'crash command called', caller=crash, statsd=[
              'rhaptos2.repo.crash', ])
        raise Rhaptos2Error('Crashing on demand')
    else:
        abort(404)


@app.route("/burn/", methods=["GET"])
def burn():
    ''' '''
    if app.debug:
        dolog(
            "INFO", 'burn command called - dying hard with os._exit',
            caller=crash, statsd=['rhaptos2.repo.crash', ])
        # sys.exit(1)
        # Flask traps sys.exit (threads?)
        os._exit(1)  # trap _this_
    else:
        abort(404)


@app.route("/admin/config/", methods=["GET", ])
def admin_config():
    """View the config we are using

    Clearly quick and dirty fix.
    Should create a common library for rhaptos2 and web framrwoe
    """
    if app.debug:
        outstr = "<table>"
        for k in sorted(app.config.keys()):
            outstr += "<tr><td>%s</td> <td>%s</td></tr>" % (
                str(k), str(app.config[k]))

        outstr += "</table>"

        return outstr
    else:
        abort(403)

################ openid views - from flask


@app.before_request
def before_request():
    g.user = auth.whoami()


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
@auth.oid.loginhandler
def login():
    """Does the login via OpenID.  Has to call into `auth.oid.try_login`
    to start the OpenID machinery.
    """
    # if we are already logged in, go back to were we came from
    if g.user is not None:
        return redirect(auth.oid.get_next_url())
    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return auth.oid.try_login(openid, ask_for=['email', 'fullname',
                                                       'nickname'])
    return render_template('login.html', next=auth.oid.get_next_url(),
                           error=auth.oid.fetch_error(),
                           confd=app.config)


@auth.oid.after_login
def create_or_login(resp):
    """This is called when login with OpenID succeeded and it's not
    necessary to figure out if this is the users's first login or not.

    """

    auth.after_authentication(resp.identity_url, 'openid')
    return redirect(auth.oid.get_next_url())


@app.route('/logout')
def logout():
    session.pop('openid', None)
    session.pop('authenticated_identifier', None)
    flash(u'You have been signed out')
    return redirect(auth.oid.get_next_url())


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
    audience = "http://%s" % app.config['www_server_name']
    data = {'assertion': request.form['assertion'], 'audience': audience}
    resp = requests.post(
        'https://verifier.login.persona.org/verify', data=data, verify=True)

    # Did the verifier respond?
    if resp.ok:
        # Parse the response
        verification_data = json.loads(resp.content)
        dolog("INFO", "Verified persona:%s" % repr(verification_data))

        # Check if the assertion was valid
        if verification_data['status'] == 'okay':
            # Log the user in by setting a secure session cookie
#            session.update({'email': verification_data['email']})
            auth.after_authentication(verification_data['email'], 'persona')
            return resp.content

    # Oops, something failed. Abort.
    abort(500)

# folders
###################### A custom converter in Flask is a better idea
### todo: custom convertor

MEDIA_MODELS_BY_TYPE = { 
        "application/vnd.org.cnx.collection":model.Collection,
        "application/vnd.org.cnx.module":model.Module,
        "application/vnd.org.cnx.folder":model.Folder
}

### FIXME the following needs to actually support both modules and collections in a folder als

@app.route('/folder/<folderuri>', methods=['GET'])
def folder_get(folderuri):
    """  """
    dolog("INFO", "genericget::%s %s %s" % (model.Folder, folderuri, g.userID))
    try:
        out = generic_get(model.Folder, folderuri, g.userID)
        return out
    except Exception, e:
        dolog("INFO", e)
        return "whoops"
    
def rossfolder_get(folderuri):
    """    """
    foldbody=[]
    fold = model.get_by_id(model.Folder, folderuri, g.userID)
    foldjson = fold.to_dict()
    for obj in fold.body:
        try:
           mod  = model.get_by_id(model.Module, obj, g.userID)
           foldbody.append({"id":mod.id_,"title":mod.title,"mediaType":mod.mediaType})
        except:  # FIXME want to catch no such object error
           pass
    foldjson['body'] = foldbody
    foldjson['id'] = foldjson.pop('id_')
    
    resp = flask.make_response(json.dumps(foldjson))
    resp.content_type = 'application/json'
    resp.headers["Access-Control-Allow-Origin"] = "*"

    auth.callstatsd('rhaptos2.e2repo.workspace.GET')
    return resp

@app.route('/collection/<collectionuri>', methods=['GET'])
def collection_get(collectionuri):
    """  """
    return generic_get(model.Collection, collectionuri, g.userID)


@app.route('/module/<moduleuri>', methods=['GET'])
def module_get(moduleuri):
    """    """
    return generic_get(model.Module, moduleuri, g.userID)

######


def generic_get(klass, uri, requesting_user_uri):
    #mod = model.get_by_id(klass, uri, requesting_user_uri)
    mod = model.obj_from_urn(uri, requesting_user_uri)
    resp = flask.make_response(json.dumps(mod.jsonable(requesting_user_uri)))
    resp.status_code = 200
    resp.content_type = 'application/json'
    return resp


def generic_post(klass):
    """Temp fix till get regex working on routes """
    dolog("INFO", "THIS US g")
    dolog("INFO", repr(g.__dict__))
    owner = g.userID  # loggedin user
    jsond = request.json  # flask autoconverts to dict ...
    fldr = model.post_o(klass, jsond, requesting_user_uri=owner)
    resp = flask.make_response(json.dumps(fldr.jsonable(owner)))
    resp.status_code = 200
    resp.content_type = 'application/json'
    return resp


def generic_put(klass, uri):

    owner = g.userID
    incomingjsond = request.json
    fldr = model.put_o(incomingjsond, klass, uri,
                             requesting_user_uri=owner)
    resp = flask.make_response(json.dumps(fldr.jsonable(owner)))
    resp.status_code = 200
    resp.content_type = 'application/json'
    return resp


def generic_delete(klass, uri):
    """ """
    owner = g.userID
    model.delete_o(klass, uri, requesting_user_uri=owner)
    resp = flask.make_response("%s is no more" % uri)
    resp.status_code = 200
    resp.content_type = 'application/json'
    return resp


def generic_acl(klass, uri, acllist):
    owner = g.userID
    fldr = model.get_by_id(klass, uri, owner)
    fldr.set_acls(owner, acllist)
    resp = flask.make_response(json.dumps(fldr.jsonable(owner)))
    resp.status_code = 200
    resp.content_type = 'application/json'
    return resp


@app.route('/folder/', methods=['POST'])
def folder_post():
    """ """
    return generic_post(model.Folder)


@app.route('/folder/<folderid>', methods=['PUT'])
def folder_put(folderid):
    """ """
    return generic_put(model.Folder, folderid)


@app.route('/module/', methods=['POST'])
def module_post():
    """ """
    r = generic_post(model.Module)
    return r


@app.route('/module/<moduleuri>', methods=['PUT'])
def module_put(moduleuri):
    """ """
    return generic_put(model.Module, moduleuri)


@app.route('/collection/', methods=['POST'])
def collection_post():
    """ """
    return generic_post(model.Collection)


@app.route('/collection/<collectionuri>', methods=['PUT'])
def collection_put(collectionuri):
    """ """
    return generic_put(model.Collection, collectionuri)


@app.route('/collection/<path:collectionuri>/acl/', methods=['PUT', 'GET'])
def collection_acl_put(collectionuri):
    """ """
    requesting_user_uri = g.userID
    if request.method == "PUT":
        jsond = request.json
        return generic_acl(model.Collection, collectionuri, jsond)
    elif request.method == "GET":
        obj = model.get_by_id(model.Collection,
                                    collectionuri, requesting_user_uri)
        return str(obj.userroles)


@app.route('/folder/<path:uri>/acl/', methods=['PUT', 'GET'])
def acl_folder_put(uri):
    """ """
    requesting_user_uri = g.userID
    if request.method == "PUT":
        jsond = request.json
        return generic_acl(model.Folder, uri, jsond)
    elif request.method == "GET":
        obj = model.get_by_id(model.Folder,
                                    uri, requesting_user_uri)
        return str(obj.userroles)


@app.route('/module/<path:uri>/acl/', methods=['PUT', 'GET'])
def acl_module_put(uri):
    """ """
    requesting_user_uri = g.userID
    if request.method == "PUT":
        jsond = request.json
        return generic_acl(model.Module, uri, jsond)
    elif request.method == "GET":
        obj = model.get_by_id(model.Module,
                                    uri, requesting_user_uri)
        return str(obj.userroles)


@app.route('/collection/<collectionuri>', methods=['DELETE'])
def collection_del(collectionuri):
    """ """
    return generic_delete(model.Collection, collectionuri)


@app.route('/folder/<folderuri>', methods=['DELETE'])
def folder_del(folderuri):
    """ """
    return generic_delete(model.Folder, folderuri)


@app.route('/module/<moduleuri>', methods=['DELETE'])
def module_del(moduleuri):
    """ """
    return generic_delete(model.Module, moduleuri)


###############
@app.errorhandler(Rhaptos2Error)
def catchall(err):
    return "Placeholder for better error handling..." + str(err)





