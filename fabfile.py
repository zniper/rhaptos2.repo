from fabric.api import local

'''

issues over run locally and remotely.  Basically only ever run remotely...
'''

srcdir='/home/pbrian/frozone'
stagingdir='/tmp/staging'
wwwdir='/usr/local/www/nginx/frozone/'
flaskdir_repo='/usr/local/www/flask/e2repo/'
flaskdir_server='/usr/local/www/flask/e2server/'


def prep():
    local('cd %s' % srcdir)
    local('git pull origin develop')

#nginx

    try:
        local('sudo cp /usr/local/etc/nginx/nginx.conf /tmp/nginx.paranoid')
    except: 
        pass
    local('sudo cp e2server/nginx.conf /usr/local/etc/nginx/nginx.conf')

    local('sudo cp e2client/strawman.html \
           e2client/mikadosoftware-cnx.js \
           e2client/tinydemo.html %s' % wwwdir)

    local('sudo cp -r thirdparty/tinymce  %s/' % wwwdir)




#server(s)
    local('sudo cp e2server/e2server.py \
        e2server/uwsgi_e2server.sh \
        e2server/reflector.py e2server/ajaxlib.py\
        e2server/__init__.py %s' % flaskdir_server)

    local('sudo cp e2repo/e2repo.py \
        e2repo/uwsgi_e2repo.sh \
        e2server/reflector.py e2server/ajaxlib.py\
        e2repo/__init__.py %s' % flaskdir_repo)

# now start up the uwsgi servers, and restart nginx.  test by loading http://hadrian/frozone/test.html

