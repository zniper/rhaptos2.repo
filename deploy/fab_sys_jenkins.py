#!/usr/local/bin/python

'''
Fab file to install jenkins on a server.

This is part of the network level install for frozone

'''

import fabric
import fabpass
from fabric.operations import put, open_shell, prompt
from fabric.api import sudo, run, local
import os

def install_jenkins():
    ''' 


    '''
    sudo('apt-get install -y git ') 
    sudo('apt-get install -y jenkins')
