#!/usr/local/bin/python

'''
Fab file to install bind9 on a server.

This is part of the network level install for frozone

'''

import fabric
import fabpass
from fabric.operations import put, open_shell, prompt
from fabric.api import sudo, run, local
import os

def install_bind():
    ''' 


    '''
    sudo('apt-get update')
    sudo('apt-get install -y bind9 dnsutils')
    sudo('pip install dnspython')
    sudo('pip install easyzone')

def configure_bind():
    '''
    simple configuration of bind9 on ubuntu.

    This uses files located in deploy/conf.d/dns to configure a bind9 installation.
    It expects to have the zonefile names and paths altered by the staging process.

    It also is a fixed config file for names, a better solution is needed, probably auto-generating 
    zonefiles with easyzone/dnspython.


    
    '''
    
    sudo('mkdir -p -m 0655 /etc/bind/zones')
    put('../conf.d/dns/com.mikadosoftware.office.db', '/etc/bind/zones/', use_sudo=True)
    put('../conf.d/dns/named.conf.local', '/etc/bind/zones/', use_sudo=True)
    put('../conf.d/dns/named.conf.options', '/etc/bind/zones/', use_sudo=True)
    sudo('service bind9 restart')
