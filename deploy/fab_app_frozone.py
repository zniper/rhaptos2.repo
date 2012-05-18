
import fabric
import fabpass
from fabric.operations import put
from fabric.api import sudo, run, local
import os

from frozone.conf import *

'''

Provides: 

  install_cdn
  install_www


This expects to be called through a fab call that is itself called
through Make, giving a horror of argument passing.

::
   
  make host=cnx1 fabfile=deploy/fab_app_frozone.py context=office clean-local
  -> generates ...
  fab -H cnx1 -f fab_app_frozone.py clean_local:context=office
  -> which calls
  fab_app_frozone.clean_local(context,...)





I believe the only realistic way to do this is to have a set of box types 
and versions, and store those in text file on the box - so we always know 
what version/type the box we are on actually is.  


  


permissions on nginx
location of thirdparty files:

todo: have the install_client call prep, but check if it has already
prep box first


'''






######### Tools


def prepend(f):
    '''given a file that should be under frozone/ give back that as a local path to make put operations easier '''
    return os.path.join(localstagingdir, 
                        os.path.join('frozone', f)
                        )


def clean_local():
    ''' '''

    for d in (localstagingdir, localgitrepo):
        local('mkdir -p -m 0777 %s' % d)

    local('rm -rf %s' % localgitrepo)
    local('rm -rf %s' % localstagingdir)
        
    

def remote_init(): 

    for d in (remote_wwwd, remote_e2repo, remote_e2server, remote_supervisor_home):
        sudo('mkdir -p -m 0777 %s' % d)
        

        
def install_cdn():
    '''Static server for tiny. THe app specific  html and js is served through www.'''

    put(prepend('conf.d/nginx/nginx.conf'), 
                '/etc/nginx/nginx.conf', use_sudo=True, mode=0755)
    put(prepend('conf.d/nginx/cdn.conf'), 
                '/etc/nginx/conf.d/', use_sudo=True, mode=0755)
    put(prepend('conf.d/nginx/www.conf'), 
                '/etc/nginx/conf.d/', use_sudo=True, mode=0755)



    sudo('mkdir -p -m 0777 /usr/share/www/nginx/cdn')
    sudo('chown -R www-data:www-data /usr/share/www/nginx/cdn')
    put(TINYMCE_STORE, '/usr/share/www/nginx/cdn', use_sudo=True, mode=0755)
    restart_nginx()



def install_www():
    '''need to be a nginx server. '''

    #0777 !!!! anyway -p stops failing if already there
    sudo('mkdir -p -m 0777 /usr/share/www/nginx/repo')
#    sudo('mkdir -p -m 0777 %s' % remote_sitepackage)


    put(os.path.join(localstagingdir, 'frozone'),
                remote_sitepackage, use_sudo=True, mode=0755)

    put(prepend('www/*'), 
                remote_wwwd, use_sudo=True, mode=0755)
    ######## why not run from site-packages?
    
    put(prepend('e2server/*.py'), 
                remote_e2server, use_sudo=True, mode=0755)
    put(prepend('e2server/reflector.py'), 
                remote_e2repo, use_sudo=True, mode=0755)
    put(prepend('e2repo/*.py'), 
                remote_e2repo, use_sudo=True, mode=0755)


    restart_nginx()


def restart_nginx():

    sudo('/etc/init.d/nginx restart')



def install_supervisor():
    ''' '''

    sudo('mkdir -p -m 0777 %s' % remote_supervisor_home)
    put(prepend('conf.d/nginx/supervisord.conf'), 
                 remote_supervisor_home)
    
    sudo('supervisord -c %s' % os.path.join(remote_supervisor_home, 'supervisord.conf'))

# now start up the uwsgi servers, and restart nginx.  test by loading http://hadrian/frozone/test.html

