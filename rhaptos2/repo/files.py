#!/usr/local/bin/python

''' 
Simple file management module.
We are basing this repo primarily on file storage (at least for now - we intend to prototype and try out new forms of workspoace / collections.)

Anyway, file storage is often tricky so clever robust file deletion / creation will be done thorugh here.  I suspect it will also deal with remote file storage too.
'''

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
#from rhaptos2.common import conf
#confd = conf.get_config('rhaptos2')
from rhaptos2.repo import app 


def return1():
    print "[logline] this is a log line"
    return 2#testing soimewthing silly

def rhaptos_file_delete(modname, userspace):
    '''
    '''
    f = os.path.join(userspace, modname)
    os.remove(f)
         