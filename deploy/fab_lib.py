#!/usr/local/bin/python                                                                    

'''                                                                                        
Generic routines etc
                                                                                           
This is a copy of rhaptos2/conf.py - keep in synch till push off to seperate packjage                                                                                           
'''

import fabric
import fabpass
from fabric.operations import put, open_shell, prompt
from fabric.api import sudo, run, local
import os

############################# Get config 
import ConfigParser

class Rhaptos2ConfigError(Exception):
    '''Put this in common area'''
    pass


def get_config():

    parser = ConfigParser.SafeConfigParser()
    parser.read('/usr/local/etc/rhaptos2/frozone.ini')
    globaldict = dict(parser.items('frozone'))

    ### get from the environment anything labelled rhaptos2_ as well
    ### test here???
    expected_keys = ['rhaptos2_current_version',  # such as '0.0.2'
                    ] 
    thisdict = {}
    for k in os.environ:
        if k.find('rhaptos2_') == 0:
            thisdict[k] = os.environ[k]
    for k in expected_keys:
        if k not in thisdict.keys():
             raise Rhaptos2ConfigError('%s not found in os.environ.  It is required.' % k)

    thisdict['rhaptos2_pkg_name'] = 'Rhaptos2-%s.tar.gz' % thisdict['rhaptos2_current_version']

    globaldict.update(thisdict)    

    return globaldict


def prep_ubuntu_server():
    ''' 
    '''
    sudo('apt-get update')
