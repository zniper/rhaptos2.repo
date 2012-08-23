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

from rhaptos2.common import conf
from rhaptos2.common import log
from rhaptos2.common import err


def set_logger(apptype, app_configd):
    lg = log.get_logger(apptype, app_configd)
    app.logger.addHandler(lg)


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
set_logger(apptype, app.config)

import rhaptos2.repo.views
