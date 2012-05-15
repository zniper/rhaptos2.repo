import fabric
from fabconf import SUPERVISORDIR
import fabpass



class frozoneError(Exception):
    pass

def ubuntu_sys_install():
    ''' '''

    sys_install_nginx_ubuntu()
    sys_install_git_ubuntu()
    sys_install_pythonenv_ubuntu()

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

    #setup supervisor
    fabric.api.run('mkdir %s' % SUPERVISORDIR)
    


def sys_install_nginx_ubuntu():
    
    fabric.api.sudo('apt-get -y install nginx')



def server_install_nginx_freebsd():
    ''' '''
    raise frozoneError('not yet implemented') 
