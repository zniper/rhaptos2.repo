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

from rhaptos2.conf import confd
from rhaptos2 import log
from rhaptos2 import exceptions

#### see http://flask.pocoo.org/docs/patterns/packages/

app = Flask(__name__)
lg = log.get_rhaptos2Logger('rhaptos2-repo')
app.logger.addHandler(lg)

import rhaptos2.repo.views
