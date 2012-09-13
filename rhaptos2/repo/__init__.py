#!/usr/bin/env python
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
import logging

from rhaptos2.common import conf, log, err


def set_logger(apptype, app_configd):
    """
lg.warn("Help", extra={'statsd':['rhaptos2.repo.module', 
                                   'bamboo.foo.bar']})


    """
    lg = logging.getLogger(apptype)

    #Trapping basic missing conf
    uselogging = "%s_use_logging" % apptype
    loglevel = "%s_loglevel" % apptype

    if uselogging not in confd.keys():
        confd[uselogging] = 'Y'

    if loglevel not in confd.keys():
        confd[loglevel] = 'DEBUG'

    
    hdlr = log.StatsdHandler(app.config['rhaptos2_statsd_host'],
                    int(app.config['rhaptos2_statsd_port']))

    hdlr2 = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s  - %(message)s')
    hdlr.setFormatter(formatter)
    hdlr2.setFormatter(formatter)

    app.logger.addHandler(hdlr)
    app.logger.addHandler(hdlr2)

    app.logger.setLevel(confd[loglevel])




def get_version():
    '''Making very broad assumptions about the existence of files '''
    d = os.path.dirname(__file__)
    try:
        v = open(os.path.join(d, 'version.txt')).read().strip()
        return v
    except Exception, e:
        return '0.0.0'
    #todo: think about this 

apptype = 'rhaptos2'
confd = conf.get_config(apptype)
app = Flask(__name__)
app.config.update(confd)
app.config['BUILD_TAG'] = 'FIXBUILDTAG!'
set_logger(apptype, app.config)

import rhaptos2.repo.views
