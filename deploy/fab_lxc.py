#!/usr/local/bin/python

'''

Simple usage :: 
  
    see install-os in main docs



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

  fab -H hpcube -f fab-lxc.py preboot:vhostname=cnx2,vhostip=10.0.0.2

#rootboot

  fab -f fab-lxc.py -H <lxc> useradd:username=<name>,passwd=<pass>

THen a uer fabdeploy has sudo privileges and can do normal deploy stuff



'''


import fabric
from fabric.api import local, sudo, put
from fabric.contrib import files
import random
import pprint
import copy
import sys

from frozone.deploy import fab_sys

import  time

#import fabpass

CONTEXTTMPL = {
    'hostname':   'cnx',
    'ip4address': '10.0.0.104',

    'domain':     'office.mikadosoftware.com',
    'dns1':       '10.0.0.101',
    'ip4network': '10.0.0.0',
    'ip4gateway': '10.0.0.1',
    'ip4netmask': '255.255.255.0'
    }


def build_new_container(vhostname, vhostip):
    '''create, on host, a new container, based on ubuntu template


      fab -H hpcube -f deploy/fab_lxc.py build_new_container:vhostname=cnx2,vhostip=10.0.0.12
 
    '''
    sudo('sudo lxc-create -t ubuntu -f /etc/lxc/lxc.conf -n %s' % vhostname)


def getniceunsafetmpfile():
    '''must have file that is safename '''
    return '/tmp/frozone.%s' % random.randint(1,1000)



def preboot(vhostname=None, vhostip=None):

    ''' alter the remote network/interfaces file on a lxc container VHost.
    we are passed the vhostname, as a string (assume it is a valid number, but allows flexibility)
    

    >>> configure_network_interface_container('cnx1', 1)
    
    write to /var/lib/lxc/{name}/rootfs/etc/network/interfaces 

    fab -H hpcube preboot:vhostname=cnx02,vhostip=10.0.0.12 
           ^^^^^^
           VMHost !!
    '''
    lxc_stop(vhostname)

    #update the context 
    context = copy.deepcopy(CONTEXTTMPL)
    context['hostname'] = vhostname
    context['ip4address'] = '%s' % vhostip

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


    #### fix NAT / arp bug
    sudo('''cat > /var/lib/lxc/%s/rootfs/etc/rc.local << EOF
ping -c 3 www.google.com
return 0
EOF
''' % context['hostname'])

    #call sudoers
    put_sudoers(vhostname, vhostip)
    lxc_start(vhostname)


def put_sudoers(vhostname, vhostip):
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


def lxc_stop(vhostname):
    '''stop and instance of an named lxc

    '''
    fabric.api.sudo('lxc-stop -n %s' % vhostname)
    time.sleep(10)


def lxc_start(vhostname):
    '''start an instance of an named lxc
    
    '''

    fabric.api.sudo('lxc-start -d -n %s' % vhostname)
    #give time to start
    time.sleep(10)

###################### POST BOOT

def postboot():
    '''perform all base configs needed once Virtual Server is running on network.

    - make python base
    '''
    fab_sys.sys_install_git_ubuntu()
    fab_sys.sys_install_pythonenv_ubuntu()
    sudo('reboot')

###########################

def lxc_destroy(vhostname):
    '''WIpe out a container on a host 

    '''    
    sudo('lxc-destroy -fn %s' % vhostname)

    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
