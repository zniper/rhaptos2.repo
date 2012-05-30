#!/usr/local/bin/python

'''
Fab file to install Graphite and Scribe and Statsd onto a server


'''

import fabric
import fabpass
from fabric.operations import put, open_shell, prompt
from fabric.api import sudo, run, local
import os


def prepare_repo():
    ''' '''
    import fab_sys
    fab_sys.sys_install_nginx_ubuntu()
    
