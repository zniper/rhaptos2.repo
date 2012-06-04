import fabric

from fabconf import SUPERVISORDIR
import fabpass
import datetime

class frozoneError(Exception):
    pass

def ubuntu_sys_install(version='1.0.0'):
    '''entry point for all fabfiles that want to post boot configure an ubuntu system
    
    only one version supported right now :-)
    '''

    sys_install_nginx_ubuntu()
    sys_install_git_ubuntu()
    sys_install_pythonenv_ubuntu()

    fabric.api.sudo('apt-get -y install emacs')
    fabric.api.sudo('apt-get -y install tree')

    sudo('''cat >> /etc/mikadodeploy.log << EOF
installed on %s
installed ubuntu_sys_install version 1.0.0
EOF
''' % datetime.datetime.today().isoformat())

    fabric.api.sudo('reboot')


def sys_install_nginx_ubuntu():
    
    fabric.api.sudo('apt-get -y install nginx')

def sys_install_git_ubuntu():
    
    fabric.api.sudo('apt-get -y install git')

def sys_install_pythonenv_ubuntu():
    '''installing most useful python bits


    http://projects.unbit.it/uwsgi/wiki/Install
    '''

    #get easy_install
    fabric.api.sudo('apt-get install -y python-setuptools')
    fabric.api.sudo('easy_install Flask')
    fabric.api.sudo('easy_install pip') 
    fabric.api.sudo('apt-get install -y build-essential python-dev libxml2-dev')
    fabric.api.sudo('pip install uwsgi')
    fabric.api.sudo('pip install supervisor')
    fabric.api.sudo('pip install Fabric')
    fabric.api.sudo('pip install statsd')







def server_install_nginx_freebsd():
    ''' '''
    raise frozoneError('not yet implemented') 
