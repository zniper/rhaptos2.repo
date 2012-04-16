
#### hmmm, this wont work on ubuntu as directory structures wrong.
#### hmmmmmmmm

srcdir='/home/pbrian/frozone'
wwwdir='/usr/local/www/nginx/frozone/'
flaskdir_repo='/usr/local/www/flask/e2repo/'
flaskdir_server='/usr/local/www/flask/e2server/'

#git pull...
cd $srcdir

#nginx
sudo cp /usr/local/etc/nginx/nginx.conf /tmp/nginx.paranoid
sudo cp e2server/nginx.conf /usr/local/etc/nginx/
sudo cp e2client/strawman.html \
        e2client/mikadosoftware-cnx.js \
        e2client/tinydemo.html $wwwdir


sudo cp -r thirdparty/tinymce  $wwwdir/




#server(s)
sudo cp e2server/e2server.py \
        e2server/uwsgi_e2server.sh \
        e2server/reflector.py e2server/ajaxlib.py\
        e2server/__init__.py $flaskdir_server

sudo cp e2repo/e2repo.py \
        e2repo/uwsgi_e2repo.sh \
        e2server/reflector.py e2server/ajaxlib.py\
        e2repo/__init__.py $flaskdir_repo

# now start up the uwsgi servers, and restart nginx.  test by loading http://hadrian/frozone/test.html

