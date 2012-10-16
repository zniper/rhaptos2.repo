# -*- coding: utf-8 -*-
"""__init__.py (rhaptos.repo) - Rhaptos application package

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
import statsd
import json
import logging
import uuid
import flask  # XXX Why is this imported twice (see 2 lines down)?
from functools import wraps
from flask import (
    Flask, render_template,
    request, g, session, flash,
    redirect, url_for, abort,
    )
from rhaptos2.common import conf, log, err

import pkg_resources  # part of setuptools
__version__ = pkg_resources.require("rhaptos2.repo")[0].version

APPTYPE = 'rhaptos2repo'

# Globally reference application variable.
_app = None

def get_app():
    """Get the application object"""
    global _app
    return _app

def set_app(app):
    """Set the global application object"""
    global _app
    _app = app

def dolog(lvl, msg, caller=None, statsd=None):
    """wrapper function purely for adding context to log stmts

    I am trying to keep this simple, no parsing of the stack etc.

    caller is the function passed when the dolog func is called.  We jsut grab its name
    extras is likely to hold a list of strings that are the buckets


    >>> dolog("ERROR", "whoops", os.path.isdir, ['a.b.c',])

    """
    lvls = {
    "CRITICAL" : 50,
    "ERROR"    : 40,
    "WARNING"  : 30,
    "INFO"     : 20,
    "DEBUG"    : 10,
    "NOTSET"   : 0
    }
    try:
        goodlvl = lvls[lvl]
    except:
        goodlvl = 20 ###!!!

    #create an extras dict, that holds curreent user, request and action notes
    if caller:
        calledby = "rhaptos2.loggedin." + str(caller.__name__)
    else:
        calledby = "rhaptos2.loggedin.unknown"

    if statsd:
        statsd.append(calledby)
    else:
        statsd = [calledby,]

    try:
        request_id = g.request_id
    except:
        request_id = "no_request_id"

    try:
        user_id = g.user_id
    except:
        user_id = "no_user_id"

    extra = {'statsd': statsd,
             'user_id': user_id,
             'request_id': request_id}

    app = get_app()
    app.logger.log(goodlvl, msg, extra=extra)

def set_logger(apptype, app_configd):
    """
    useage:
        lg.warn("Help", extra={'statsd':['rhaptos2.repo.module',
                                         'bamboo.foo.bar']})

    """
    lg = logging.getLogger(apptype)
    confd = conf.get_config(apptype)

    ### Trapping basic missing conf
    uselogging = "%s_use_logging" % apptype
    loglevel = "%s_loglevel" % apptype

    if uselogging not in confd.keys():
        confd[uselogging] = 'Y'

    if loglevel not in confd.keys():
        confd[loglevel] = 'DEBUG'
    ###

    ## define handlers
    hdlr2 = log.StatsdHandler(app_configd['rhaptos2repo_statsd_host'],
                    int(app_configd['rhaptos2repo_statsd_port']))

    hdlr = logging.StreamHandler()

    ## formatters
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s  - %(request_id)s - %(user_id)s - %(message)s')

    hdlr.setFormatter(formatter)
    #hdlr2 just sends statsd calls so does not need formatter ...

    app = get_app()
    app.logger.addHandler(hdlr)
    app.logger.addHandler(hdlr2)

    app.logger.setLevel(confd[loglevel])

def get_version():
    """Making very broad assumptions about the existence of files"""
    d = os.path.dirname(__file__)
    try:
        v = open(os.path.join(d, 'version.txt')).read().strip()
        return v
    except Exception, e:
        return '0.0.0'
    #todo: think about this
