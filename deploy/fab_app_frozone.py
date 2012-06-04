


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


import fabric
import fabpass
from fabric.operations import put
from fabric.api import sudo, run, local
import os

import fab_lib
confd = fab_lib.get_config()




######### Tools


def remote_init(): 

    ''' (clean down) then create target dir on remote host.

    TBD - Clean Down
    '''

    for d in (confd['remote_wwwd'], 
              confd['remote_e2repo'], 
              confd['remote_e2server'],
              confd['remote_supervisor_home']):
        sudo('mkdir -p -m 0777 %s' % d)
        

        
def install_cdn(localstagingdir):

    '''Static server for tiny. THe app specific html and js is served
    through www.'''

    put(os.path.join(localstagingdir, 'conf.d/nginx/nginx.conf'),
                '/etc/nginx/nginx.conf', use_sudo=True, mode=0755)

    put(os.path.join(localstagingdir, 'conf.d/nginx/cdn.conf'), 
                '/etc/nginx/conf.d/', use_sudo=True, mode=0755)

    put(os.path.join(localstagingdir, 'conf.d/nginx/www.conf'), 
                '/etc/nginx/conf.d/', use_sudo=True, mode=0755)


    sudo('mkdir -p -m 0777 /usr/share/www/nginx/cdn')
    sudo('chown -R www-data:www-data /usr/share/www/nginx/cdn')
    put(confd['tinymce_store'], '/usr/share/www/nginx/cdn', use_sudo=True, mode=0755)
    restart_nginx()

def getrhaptos2pkg(localstagingdir):
    ''' '''
    return os.path.join(localstagingdir, 
            'Rhaptos2/dist/Rhaptos2-0.0.1.tar.gz')

def install_rhaptos2(localstagingdir, configfile):
    ''' build setup pkg, push to the remote, install it.
   
    '''
    local('cd %s/Rhaptos2 && python setup.py sdist' % localstagingdir)
    put(getrhaptos2pkg(localstagingdir),
        '/tmp', 
        use_sudo=True, mode=0755)
    sudo('pip install "/tmp/Rhaptos2-0.0.1.tar.gz"')
    #install site wide config file
    sudo('mkdir -p -m 0777 /usr/local/etc/rhaptos2')
    put(os.path.join(localstagingdir, configfile), 
        '/usr/local/etc/rhaptos2/frozone.ini',
        use_sudo=True, mode=0755)
         

def install_www(localstagingdir):
    '''need to be a nginx server. '''

    #0777 !!!! anyway -p stops failing if already there
    sudo('mkdir -p -m 0777 /usr/share/www/nginx/repo')


    #todo : install a pacakge !!
    put(os.path.join(localstagingdir, 'Rhaptos2/rhaptos2/repo'),
                confd['remote_sitepackage'], use_sudo=True, mode=0755)

    put('www/*', 
         confd['remote_wwwd'], use_sudo=True, mode=0755)
    ######## why not run from site-packages?
    
    put(os.path.join(localstagingdir, 'Rhaptos2/rhaptos2/repo/*.py'), 
                confd['remote_e2repo'], use_sudo=True, mode=0755)

    restart_nginx()


def restart_nginx():

    sudo('/etc/init.d/nginx restart')



def install_supervisor(localstagingdir):
    ''' '''

    sudo('mkdir -p -m 0777 %s' % confd['remote_supervisor_home'])
    put(os.path.join(localstagingdir, 'conf.d/nginx/supervisord.conf'), 
                 confd['remote_supervisor_home'])
    try:
        sudo('supervisord -c %s' % os.path.join(confd['remote_supervisor_home'], 
                                                'supervisord.conf'))
    except:
        print 'could not start supervisor as its already up '

# now start up the uwsgi servers, and restart nginx.  test by loading http://hadrian/frozone/test.html

