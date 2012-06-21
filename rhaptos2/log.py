#!/usr/local/bin/python
#! -*- coding: utf-8 -*-


'''
'''


import logging
from logging.handlers import SysLogHandler
from rhaptos2.conf import confd

#needs a test if syslog is actually up...

def get_rhaptos2Logger(modname):
    '''simple, pre-configured logger will be returned.
       
    if envvar: use_logging == False will return NullHandler logger.
    '''

    print "logging"
    print confd['use_logging'], type(confd['use_logging'])

    if confd['use_logging'] == 'Y':
        print 'yes logging'
        lg = logging.getLogger(modname)
        lg.setLevel(confd['loglevel'])
        ch = SysLogHandler(confd['syslog_sock'])
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        lg.addHandler(ch)
    else:
        print 'not logging'
        lg = logging.getLogger(modname)
        lg.addHandler(logging.NullHandler())        

    return lg



    
