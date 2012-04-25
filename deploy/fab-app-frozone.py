
import fabric
import fabpass

from fabric.api import sudo, run


'''

Provides: 

  prep() - prepare a newly created lxc for being one of the
           e2client/server/repo boxes, or other required boxes
 
  install_e2client()

  install_e2server()

  install_e2repo()


I believe the only realistic way to do this is to have a set of box types 
and versions, and store those in text file on the box - so we always know 
what version/type the box we are on actually is.  


  


permissions on nginx
location of thirdparty files:

todo: have the install_client call prep, but check if it has already
prep box first


'''



srcdir='/home/deployagent/frozone'
stagingdir='/tmp/staging'
wwwdir='/usr/local/www/nginx/frozone/'
flaskdir_repo='/usr/local/www/flask/e2repo/'
flaskdir_server='/usr/local/www/flask/e2server/'


#ubuntu
srcdir='/home/deployagent/frozone'
stagingdir='/tmp/staging'
wwwdir='/usr/share/www/nginx/frozone/'
flaskdir_repo='/usr/share/www/flask/e2repo/'
flaskdir_server='/usr/share/www/flask/e2server/'



def prep():

    run('mkdir -p %s %s %s %s' % (srcdir,
                                       wwwdir,
                                       flaskdir_repo,
                                       flaskdir_server
                                       ))
    
    with fabric.context_managers.cd(srcdir):
        try:
            run('git checkout develop && git pull')
        except:
             run('git clone git://github.com/lifeisstillgood/frozone.git')
             run('git checkout develop && git pull')

def install_e2client():
    '''need to be a nginx server. '''
      
        #bleahhh
        sudo('mkdir /usr/share/www/nginx/repo')
        sudo('chmod 0777 -R /usr/share/www/nginx/repo ')

        sudo('cp e2server/nginx.conf /etc/nginx/nginx.conf')

        run('cp e2client/strawman.html \
          e2client/mikadosoftware-cnx.js \
          %s' % wwwdir)

        run('cp -r thirdparty/tinymce  %s/' % wwwdir)



        run('cp e2server/e2server.py \
            e2server/uwsgi_e2server.sh \
            e2server/reflector.py e2server/ajaxlib.py\
            e2server/__init__.py %s' % flaskdir_server)

        run('cp e2repo/e2repo.py \
            e2repo/uwsgi_e2repo.sh \
            e2server/reflector.py e2server/ajaxlib.py\
            e2repo/__init__.py %s' % flaskdir_repo)

# now start up the uwsgi servers, and restart nginx.  test by loading http://hadrian/frozone/test.html

