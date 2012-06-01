#!/usr/local/bin/python                                                                    

'''                                                                                        
Generic routines etc
                                                                                           
                                                                                           
'''

import fabric
import fabpass
from fabric.operations import put, open_shell, prompt
from fabric.api import sudo, run, local
import os

############################# Get config 
import ConfigParser

def get_config():

    parser = ConfigParser.SafeConfigParser()
    parser.read('/usr/local/etc/frozone.ini')
    globaldict = dict(parser.items('frozone'))
    return globaldict


def prep_ubuntu_server():
    ''' 
    '''
    sudo('apt-get update')
