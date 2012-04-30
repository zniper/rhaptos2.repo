
import fabric
import fabpass
from fabric.operations import put
from fabric.api import sudo, run, local
import os


'''

Provides: 

  install_cdn
  install_www


I believe the only realistic way to do this is to have a set of box types 
and versions, and store those in text file on the box - so we always know 
what version/type the box we are on actually is.  


  


permissions on nginx
location of thirdparty files:

todo: have the install_client call prep, but check if it has already
prep box first


'''


#ubuntu
srcdir='/home/deployagent/frozone'


localhomedir = '/tmp/home'
localfrozonegit = os.path.join(localhomedir, 'frozone')
localstagingdir = os.path.join(localhomedir, 'staging')

wwwdir='/usr/share/www/nginx/cdn/'
flaskdir_repo='/usr/share/www/flask/e2repo/'
flaskdir_server='/usr/share/www/flask/e2server/'
homedir = '/home/deployagent'


def gitpull():
    with fabric.context_managers.cd(localgitdir):
        local('git checkout feature/cleanforjenkins && git pull')

def local_init():

    for d in (localstagingdir, localhomedir, localfrozonegit):
        local('mkdir -p -m 0777 %s' % d)

    local('rm -rf %s' % localfrozonegit)
    local('git clone git://github.com/lifeisstillgood/frozone.git %s' % localfrozonegit)
        

def local_clone_overwrite(localgitrepo=localfrozonegit, localstagingdir=localstagingdir):
    ''' '''

    local('cd %s && git checkout feature/cleanforjenkins && git pull' % localgitrepo)
    local('python %s/deploy/staging.py %s %s' % ('/home/pbrian/frozone', localgitrepo, localstagingdir)) 
    

def remote_init():

    for d in (srcdir, wwwdir, flaskdir_repo, flaskdir_server):
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
    '''Static server '''

    put(prepend('conf.d/nginx.conf'), 
                '/etc/nginx/nginx.conf', use_sudo=True, mode=0755)
    put(prepend('conf.d/cdn.conf'), 
                '/etc/nginx/conf.d/', use_sudo=True, mode=0755)

    sudo('mkdir -p -m 0777 /usr/share/www/nginx/cdn')
    sudo('chown -R www-data:www-data /usr/share/www/nginx/cdn')
    restart_nginx()

    #TODO: wget to grabr tinymce??? scp ???


def install_www():
    '''need to be a nginx server. '''

    #0777 !!!! anyway -p stops failing if already there
    sudo('mkdir -p -m 0777 /usr/share/www/nginx/repo')


    put(prepend('www/*'), 
                wwwdir, use_sudo=True, mode=0755)
    put(prepend('e2server/*.py'), 
                flaskdir_server, use_sudo=True, mode=0755)
    put(prepend('e2server/reflector.py'), 
                flaskdir_repo, use_sudo=True, mode=0755)
    put(prepend('e2repo/*.py'), 
                flaskdir_repo, use_sudo=True, mode=0755)


    restart_nginx()


def restart_nginx():

    sudo('/etc/init.d/nginx restart')



def install_supervisor():
    ''' '''

    sudo('mkdir -p -m 0777 /home/deployagent/supervisor')
    put(prepend('conf.d/supervisord.conf'), 
                '/home/deployagent/supervisor')
    
    #sudo supervisord -n -c /home/deployagent/supervisor/supervisord.conf

# now start up the uwsgi servers, and restart nginx.  test by loading http://hadrian/frozone/test.html

