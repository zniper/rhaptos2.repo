#!/usr/local/bin/python                                                                    

'''                                                                                        
Generic routines etc
                                                                                           
                                                                                           
'''

import fabric
import fabpass
from fabric.operations import put, open_shell, prompt
from fabric.api import sudo, run, local
import os

from frozone import conf


def prep_ubuntu_server():
    ''' 
    '''
    sudo('apt-get update')
