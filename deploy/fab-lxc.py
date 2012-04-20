#!/usr/local/bin/python

'''

We create any number of lxc based containers on a VMHost.
We need to 

1. alter files on the VMHost before booting the VHost
2. login to the VHost, as root (!) and perform remainder of bootstrap

3. login as deploy user to setup as normal


Container naming

Each container is named as xxx1 xxx2 xxx3
the ID maps to an ip address and a 


networks

This is a dev env, and I have no controllable router, so 

10.0.X.X netmask 255.255.0.0  giving me a network of 10.0.0.0 (!)

* vhosts are on 10.0.1.0 (but its not a network - I dont have a router
  I can use yet!)


for each lxc

#preboot

  fab -H hpcube preboot:vhostname=cnx02,vhostid=105

#rootboot

  fab -H <lxc> useradd:username=<name>,passwd=<pass>

THen a uer fabdeploy has sudo privileges and can do normal deploy stuff



'''


import fabric
from fabric.api import local
from fabric.contrib import files
import random
import pprint
import copy
import sys
from cnxfab import *
import  time

import fabpass

CONTEXTTMPL = {
    'hostname':   'cnx',
    'ip4address': '10.0.0.104',

    'domain':     'office.mikadosoftware.com',
    'dns1':       '10.0.0.101',
    'ip4network': '10.0.0.0',
    'ip4gateway': '10.0.0.1',
    'ip4netmask': '255.255.255.0'
    }



def getniceunsafetmpfile():
    '''must have file that is safename '''
    return '/tmp/frozone.%s' % random.randint(1,1000)

def preboot(vhostname=None, vhostid=None):

    ''' alter the remote network/interfaces file on a lxc container VHost.
    we are passed the vhostname, as a string (assume it is a valid number, but allows flexibility)
    

    >>> configure_network_interface_container('cnx1', 1)
    
    write to /var/lib/lxc/{name}/rootfs/etc/network/interfaces 

    fab -H hpcube preboot:vhostname=cnx02,vhostid=105 
           ^^^^^^
           VMHost !!
    '''
    fabric.api.sudo('lxc-stop -n %s' % vhostname)
    time.sleep(5)

    #update the context 
    context = copy.deepcopy(CONTEXTTMPL)
    context['hostname'] = vhostname
    context['ip4address'] = '10.0.0.%s' % vhostid

    tgtpath = '/var/lib/lxc/%s/rootfs/etc/network/interfaces' % context['hostname']
    tmpl = '''#from frozone tmpl 
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address %(ip4address)s
    network %(ip4network)s
    netmask %(ip4netmask)s
    gateway %(ip4gateway)s

'''
    tmpfile = getniceunsafetmpfile()
    open(tmpfile,'w').write(tmpl % context)
    fabric.operations.put(tmpfile, tgtpath, use_sudo=True)



    tgtpath = '/var/lib/lxc/%s/rootfs/etc/resolv.conf' % context['hostname']
    tmpl = '''#from frozone tmpl 
domain office.mikadosoftware.com
nameserver %(dns1)s
nameserver 10.0.0.1

''' 
    tmpfile = getniceunsafetmpfile()
    open(tmpfile,'w').write(tmpl % context)
    fabric.operations.put(tmpfile, tgtpath, use_sudo=True)

    #call sudoers
    put_sudoers(vhostname, vhostid)


    fabric.api.sudo('lxc-start -d -n %s' % vhostname)
    time.sleep(10)



def put_sudoers(vhostname, vhostid):
    ''' '''
    tgtpath = '/var/lib/lxc/%s/rootfs/etc/sudoers' % vhostname
    fabric.contrib.files.append(tgtpath, 
                                '\ndeployagent ALL=NOPASSWD:ALL\n\n',
                                use_sudo=True)
    


### rootboot section - must startt up the instance. then login as root
### (only known user - easier than adjusting lxc-create)
    

def useradd(username=None, passwd=None):
    '''

   Nothing clever, create user, add to sudoers group that is std on
   Ubunutu, ch password

   Note I will use this as ::

    fab -H root@cnx02 useradd:username=test2,passwd=pass2
   
   this has no pasword for root login on the new box, so 
   we need to set that in fabric.state.env

   '''
    
    fabric.state.env['password'] = 'root' #yup, thats in the lxc-create
    fabric.state.env['user'] = 'root' #yup, thats in the lxc-create


    fabric.api.sudo('useradd  -d /home/%s -g sudo -m -s /bin/bash %s' % (
                    username, username))
    fabric.api.sudo("echo %s:%s | chpasswd" % (username, passwd))

    #sudo sh -c "echo test1:pass1 | chpasswd"




if __name__ == "__main__":
    import doctest
    doctest.testmod()
