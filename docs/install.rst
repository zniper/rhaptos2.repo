============
Installation
============

NB these are *very* much a work in progress.
The fabric files are not used yet (things still in too great state of flux)


OK - there are 3 seperate components (debateable how seperate repo and server should be)

1. client (e2client)
2. server (e2server)
3. repo (e2repo)

(e2 == editor two)

Overview
--------

I am using a JQuery based client (I am assuming we will use the JQuery 
'library' we shall build to simply take the HTML5 from whatever is on the 
client(tinymce?) and push the HTML5 to whereever we need it.  This is 
an attempt to isolate us from the GUI editor a little)

So, JQuery pushes HTML5 at a REST e2server, which will then pass-through
to e2repo and then return data back up the chain.

We have an Nginx server providing the static HTML / JQuery
We have an Nginx server running two proxies via uWSGI - that is Nginx is 
acting as a WSGI enabled server running the e2server and e2repo

There is a file :meth: poormansfabfile.sh in the root, this will deploy *to my machine*.  it is very specific but should be possible to translate across if you try


:future: I want to make a fabfile deploy for BSD, ubunut 11.10 (target) *and* GAE. The GAE is mostly for showing what I ahve done to date as frankly I am very dark as far as anyone in Texas is concerned - and thats not good all round.

Steps to install
----------------

1. Install Nginx 

::

  $ cd /usr/ports/www/nginx && make clean install
  $ apt-get install nginx

The nginx.conf file will be supplied as part of e2server

2. Install uWSGI - http://projects.unbit.it/uwsgi/

3. install Flask - easy_install flask

4. deploy frozone

::

    $ cd staging
    $ git clone git@github.com:lifeisstillgood/frozone.git
    $ cd frozone 
    $ (adjust seettings in shell script)
    $ sh poormansfabfile.sh

    $ vist both the /usr/local/www/flask/e2repo and e2server and 
      execute the uwsgi.sh scripts in there. leave them running

    $ restart nginx instance - adjust nginx.conf if needed/

    to test:
    visit http://<server>/e2server/module/
    visit http://<server>/e2repo/module/12345
    
    if you gt valid reples the nginx proxing is working.

