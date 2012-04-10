#!/usr/local/bin/python

'''
collating all the installs into one place

1. editor.server
1.a  nginx (flatfiles serving tinymce)
1.b. uwsgi/nginx
1.c. uwsgi-management
1.d. flask (running under supervisord)

Other tasks for the server:

1.d. Flask
     This will need to support REST based API that supplies 
     POST module
     PUT Module??
     delete and get will be pass through to the repo???
    
1.d.i Ancillary actions - such as transform from html5 to cnxml
      

#install and configure nginx
- Manual job so far...

#install and configure uswgi and flask  
easy_install uwsgi
easy_install flask

Then follow the instructions in uwsgi folder, to have working flask and wsgi 


'''
from fabric.api import *

def install_nginx():
    pass

def install_flask():
    pass

def install_uwsgi():
    pass

def config_nginx():
    pass

def config_uwsgi():
    pass

def start_nginx():
    pass


