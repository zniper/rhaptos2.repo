
import fabric
import fabpass
from fabric.operations import put
from fabric.api import sudo, run, local
import os


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



from frozone.conf import *



def gitpull():
    with fabric.context_managers.cd(localgitdir):
        local('git checkout feature/cleanforjenkins && git pull')

def clean_local():
    ''' '''

    for d in (localstagingdir, localhomedir, localgitrepo):
        local('mkdir -p -m 0777 %s' % d)

    local('rm -rf %s' % localgitrepo)
    local('rm -rf %s' % localstagingdir)
        

def stage_local(remote_git_repo,
                localgit,
                localstaging, 
                branch, 
                context):
    ''' Download git repo, extract a known branch to staging, 
        do search replace on staging

    expect to be called through the Makefile::

        stage_local('git://github.com/lifeisstillgood/frozone.git',
                    '/tmp/frozone/git',
                    '/tmp/frozone/stage',
                    'master',
                    'rackspace')

    I then call directly to the staging.py script provided.

    '''

    clean_local()
    local('python deploy/staging.py \
          --context=%s \
          --src=%s \
          --tgt=%s \
          --branch=%s' % (context, 
                          remote_git_repo,
                          localstaging,
                          branch )) 
    

def remote_init(): 

    for d in (remote_wwwd, remote_e2repo, remote_e2server, remote_supervisor):
        sudo('mkdir -p -m 0777 %s' % d)
        

    #need a put here
        

def filemap(topdir):
    '''walka dir, get a listing of all files, 
       then these can be used for put operations '''
    fulllist = []
    dirlist = []
    ignorelist = ['.git',]
    for root, dirs, files in os.walk(topdir):
        if root in ignorelist: continue
        dirlist.extend([root,])
        fulllist.extend([os.path.join(root, f) for f in files])
    return (dirlist, fulllist)


### a with operator that prepends the staging dir to 
#class addroot(object):#
#
#    def __init__(self, file):
#        self.file = file
#    def __enter__(self):
#        return os.path.join(localstagingdir, self.file)
#    def __exit__(self, type, value, traceback):
#        pass

def prepend(f):
    ''' '''
    return os.path.join(localstagingdir, f)

def install_cdn():
    '''Static server for tiny. THe app specific  html and js is served through www.'''

    put(prepend('conf.d/nginx.conf'), 
                '/etc/nginx/nginx.conf', use_sudo=True, mode=0755)
    put(prepend('conf.d/cdn.conf'), 
                '/etc/nginx/conf.d/', use_sudo=True, mode=0755)
    put(prepend('conf.d/www.conf'), 
                '/etc/nginx/conf.d/', use_sudo=True, mode=0755)



    sudo('mkdir -p -m 0777 /usr/share/www/nginx/cdn')
    sudo('chown -R www-data:www-data /usr/share/www/nginx/cdn')
    put(TINYMCE_STORE, '/usr/share/www/nginx/cdn', use_sudo=True, mode=0755)
    restart_nginx()



def install_www():
    '''need to be a nginx server. '''

    #0777 !!!! anyway -p stops failing if already there
    sudo('mkdir -p -m 0777 /usr/share/www/nginx/repo')

    put(prepend('www/*'), 
                remote_wwwd, use_sudo=True, mode=0755)
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

    sudo('mkdir -p -m 0777 %s' % remote_supervisor)
    put(prepend('conf.d/supervisord.conf'), 
                '/home/deployagent/supervisor')
    
    #sudo supervisord -n -c /home/deployagent/supervisor/supervisord.conf

# now start up the uwsgi servers, and restart nginx.  test by loading http://hadrian/frozone/test.html

