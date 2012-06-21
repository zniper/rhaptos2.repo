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

from rhaptos2 import conf
from rhaptos2 import log
from rhaptos2 import exceptions

#return a dict of conf from a .ini file
confd = conf.get_config()

app = Flask(__name__)

import rhaptos2.repo.views


if __name__ == "__main__":
    import doctest
    doctest.testmod()
