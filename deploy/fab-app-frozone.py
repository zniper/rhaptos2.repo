
import fabric
import fabpass

from fabric.api import sudo



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

    sudo('mkdir -p %s' % srcdir)
    sudo('cd %s' % srcdir)
    try:
        sudo('git pull origin develop')
    except:
        sudo('git clone git@github.com:lifeisstillgood/frozone.git')
        sudo('git checkout develop')


    #mkdir -p /usr/share/flask/www/e2repo
    #mkdir -p /usr/share/flask/www/e2repo

    sudo('cp %s/e2server/nginx.conf /etc/nginx/nginx.conf' % stagingdir)

    sudo('cp e2client/strawman.html \
           e2client/mikadosoftware-cnx.js \
           e2client/tinydemo.html %s' % wwwdir)

    sudo('sudo cp -r thirdparty/tinymce  %s/' % wwwdir)




#server(s)
    sudo('sudo cp e2server/e2server.py \
        e2server/uwsgi_e2server.sh \
        e2server/reflector.py e2server/ajaxlib.py\
        e2server/__init__.py %s' % flaskdir_server)

    sudo('sudo cp e2repo/e2repo.py \
        e2repo/uwsgi_e2repo.sh \
        e2server/reflector.py e2server/ajaxlib.py\
        e2repo/__init__.py %s' % flaskdir_repo)

# now start up the uwsgi servers, and restart nginx.  test by loading http://hadrian/frozone/test.html

