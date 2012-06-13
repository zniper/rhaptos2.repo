#!/usr/local/bin/python
#! -*- coding: utf-8 -*-


'''
'''


import logging
from logging.handlers import SysLogHandler
from rhaptos2 import conf
confd = conf.get_config()

#needs a test if syslog is actually up...

def get_rhaptos2Logger(modname):
    '''simple, pre-configured logger will be returned.
    '''

    lg = logging.getLogger(modname)
    lg.setLevel(confd['loglevel'])
    ch = SysLogHandler(confd['syslog_sock'])

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %\
(message)s')
    ch.setFormatter(formatter)


    lg.addHandler(ch)
    return lg



    
