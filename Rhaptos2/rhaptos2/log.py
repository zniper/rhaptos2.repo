#!/usr/local/bin/python
#! -*- coding: utf-8 -*-


'''
'''


import logging
from logging.handlers import SysLogHandler
from rhaptos2 import conf
import rhaptos2Err

#needs a test if syslog is actually up...

def getFrozoneLogger(modname):
    '''simple, pre-configured logger will be returned.
    '''

    lg = logging.getLogger(modname)
    lg.setLevel(conf.LOGLEVEL)
    ch = SysLogHandler(conf.SYSLOG_SOCK)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %\
(message)s')
    ch.setFormatter(formatter)


    lg.addHandler(ch)
    return lg



    
