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

Structure:
We have three main view-areas.

 1. the models (Folder, Collection, Module)
 2. the helper views (workspace)
 3. binary uploads.
 4. openid and persona

Protocols
~~~~~~~~~
I try to stick to these

1. Every action (GET POST PUT DELETE) must have a useruri passed in to authorise
2. views recevie back *either* a model.<> object or a json-encodeable version of that


json-encoding
~~~~~~~~~~~~~

todo: convert to factory based app entirely
todo: remove view / as thats now JS
todo: remove apply_cors and apply internally. Or just use it?
todo: remove crash and burn


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
from err import (Rhaptos2Error,
                 Rhaptos2SecurityError,
                 Rhaptos2HTTPStatusError)

app = get_app()
backend.initdb(app.config)


@app.before_request
def requestid():
    g.requestid = uuid.uuid4()
    g.request_id = g.requestid
    g.user = auth.whoami()
    
########################### views




def mkjsonresponse(jstr):
    """
    given a jsonstring, format a response using the
    Flask formatting styles
    """
    resp = flask.make_response(jstr)
    resp.content_type = 'application/json; charset=utf-8'
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Credentials"] = "true"
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
        # it would require some flattening or a JSONEncoder but we just want
        # short form for now
        short_format_list = [{
            "id": i.id_, "title": i.title, "mediaType": i.mediaType} for i in w]
        flatten = json.dumps(short_format_list)

    auth.callstatsd('rhaptos2.e2repo.workspace.GET')
    return mkjsonresponse(flatten)


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
    return mkjsonresponse(json.dumps(XXX_JUNK_KEYWORDS))

@app.route("/version/", methods=["GET"])
#@resp_as_json()
def versionGET():
    ''' '''
    s = VERSION
    return mkjsonresponse(s)

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

MEDIA_MODELS_BY_TYPE = {
    "application/vnd.org.cnx.collection": model.Collection,
    "application/vnd.org.cnx.module": model.Module,
    "application/vnd.org.cnx.folder": model.Folder
}


def obtain_payload(werkzeug_request_obj):
    """
    .. todo::
       expand this function to encompass various checks on incoming
       payload of POST / PUT requests incl unicode,

    """
    try:
        jsond = werkzeug_request_obj.json
    except:
        jsond = None
    return jsond


### There is a hell of a lot of duplicated code here.
### I am uncertain at what point I am simply replicating the
### routing modules in Flask though.  I could capture
### all the PATH_INFO and deal with in tighter loops,
### but that seems... silly.  Yet I end up with this 
    
@app.route('/folder/', defaults={'folderuri': ''},
           methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/folder/<path:folderuri>',
           methods=['GET', 'POST', 'PUT', 'DELETE'])
def folder_router(folderuri):
    """
    """
    dolog("INFO", "In folder router, %s" % request.method)
    requesting_user_uri = g.userID
    payload = obtain_payload(request)

    if request.method == "GET":
        return folder_get(folderuri, requesting_user_uri)

    elif request.method == "POST":
        if payload is None:
            raise Rhaptos2HTTPStatusError(
                "Received a Null payload, expecting JSON ",
                code=400)
        else:
            return generic_post(model.Folder,
                                payload, requesting_user_uri)

    elif request.method == "PUT":
        if payload is None:
            raise Rhaptos2HTTPStatusError(
                "Received a Null payload, expecting JSON ",
                code=400)
        else:
            return generic_put(model.Folder, folderuri,
                               payload, requesting_user_uri)

    elif request.method == "DELETE":
        return generic_delete(folderuri, requesting_user_uri)

    else:
        return Rhaptos2HTTPStatusError("Methods:GET PUT POST DELETE.")


@app.route('/collection/', defaults={'collectionuri': ''},
           methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/collection/<path:collectionuri>',
           methods=['GET', 'POST', 'PUT', 'DELETE'])
def collection_router(collectionuri):
    """
    """
    dolog("INFO", "In collection router, %s" % request.method)
    requesting_user_uri = g.userID
    payload = obtain_payload(request)

    if request.method == "GET":
        return generic_get(collectionuri, requesting_user_uri)

    elif request.method == "POST":
        if payload is None:
            raise Rhaptos2HTTPStatusError(
                "Received a Null payload, expecting JSON",
                code=400)
        else:
            return generic_post(model.Collection,
                                payload, requesting_user_uri)

    elif request.method == "PUT":
        if payload is None:
            raise Rhaptos2HTTPStatusError(
                "Received a Null payload, expecting JSON",
                code=400)
        else:
            return generic_put(model.Collection, collectionuri,
                               payload, requesting_user_uri)

    elif request.method == "DELETE":
        return generic_delete(collectionuri, requesting_user_uri)

    else:
        return Rhaptos2HTTPStatusError("Methods:GET PUT POST DELETE.")


@app.route('/module/', defaults={'moduleuri': ''},
           methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/module/<path:moduleuri>',
           methods=['GET', 'POST', 'PUT', 'DELETE'])
def module_router(moduleuri):
    """
    """
    dolog("INFO", "In module router, %s" % request.method)
    requesting_user_uri = g.userID
    payload = obtain_payload(request)

    if request.method == "GET":
        return generic_get(moduleuri, requesting_user_uri)

    elif request.method == "POST":
        if payload is None:
            raise Rhaptos2HTTPStatusError(
                "Received a Null payload, expecting JSON",
                code=400)
        else:
            return generic_post(model.Module,
                                payload, requesting_user_uri)

    elif request.method == "PUT":
        if payload is None:
            raise Rhaptos2HTTPStatusError(
                "Received a Null payload, expecting JSON",
                code=400)
        else:
            return generic_put(model.Module, moduleuri,
                               payload, requesting_user_uri)

    elif request.method == "DELETE":
        return generic_delete(moduleuri, requesting_user_uri)

    else:
        return Rhaptos2HTTPStatusError("Methods:GET PUT POST DELETE.")


def folder_get(folderuri, requesting_user_uri):
    """
    return folder as an appropriate json based response string

    .__complex__ -> creates a version of an object that can be run through a std json.dump

    Why am I passing in the same userid in two successive objects
    
    1. I am not maintaining any state in the object, not assuming any state in thread(*)
    2. The first call returns the "hard" object (pointers only)
       Thus it (rightly) has no knowledge of the user permissions of its children.
       We will need to descend the hierarchy to 

    (*) This may get complicated with thread-locals in Flask and scoped sessions. please see notes
        on backend.py
    """
    fldr = model.obj_from_urn(folderuri, g.userID)
    fldr_complex = fldr.__complex__(g.userID)

    return mkjsonresponse(json.dumps(fldr_complex))
    


def generic_get(uri, requesting_user_uri):
    # mod = model.get_by_id(klass, uri, requesting_user_uri)
    mod = model.obj_from_urn(uri, requesting_user_uri)
    resp = mkjsonresponse(json.dumps(
                               mod.__complex__(requesting_user_uri)))
    return resp


def generic_post(klass, payload_as_dict, requesting_user_uri):
    """Post an appropriately formatted dict to klass

    .. todo::
       its very inefficient posting the folder, then asking for
       it to be recreated.

    """
    owner = requesting_user_uri
    fldr = model.post_o(klass, payload_as_dict,
                        requesting_user_uri=owner)
    return mkjsonresponse(json.dumps(fldr.__complex__(owner)))



def generic_put(klass, resource_uri, payload_as_dict,
                       requesting_user_uri):

    owner = requesting_user_uri
    fldr = model.put_o(payload_as_dict, klass, resource_uri,
                       requesting_user_uri=owner)
    return mkjsonresponse(json.dumps(fldr.__complex__(owner)))



def generic_delete(uri, requesting_user_uri):
    """ """
    owner = requesting_user_uri
    model.delete_o(uri, requesting_user_uri=owner)
    return mkjsonresponse("%s is no more" % uri)

### these can all go when we merge acl fixes    
def generic_acl(klass, uri, acllist):
    owner = g.userID
    fldr = model.get_by_id(klass, uri, owner)
    fldr.set_acls(owner, acllist)
    return mkresponse(json.dumps(fldr.__complex__(owner)))


@app.route('/collection/<path:collectionuri>/acl/',
           methods=['PUT', 'GET'])
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