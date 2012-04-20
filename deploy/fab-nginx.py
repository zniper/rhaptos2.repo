import fabric
from fab_ostypes import UBUNTU, FREEBSD, WIN, OSX


import fabpass



'''
Tools to do basic install and customisation

logging is an issue in fabric.  solve it via redirection.?

'''

class frozoneError(Exception):
    pass

def server_install_nginx(ostype):
    ''' '''
    if ostype == UBUNTU:
        server_install_nginx_ubuntu()
    elif ostype == FREEBSD:
        server_install_nginx_freebsd()

def server_install_nginx_ubuntu():
    ''' '''

    fabric.api.sudo('apt-get -y install nginx')
    fabric.api.sudo('reboot')

def server_install_nginx_freebsd():
    ''' '''
    raise frozoneError('not yet implemented') 
