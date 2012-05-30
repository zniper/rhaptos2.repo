=======
Frozone
=======


Frozone is a *complete* system - designed to be deployed on multiple hosts.
It is not just a pyhtonn package, although it contains at least one python package.

There is no overarching setup.py file - there are make files that use fabric, but they could as easily use capistrano to push the python files and nginx config files to the target hosts.

Components
==========

* e2repo - the repository server, a Python based webserver (Flask) that provides REST based save and store facilties for fragments of HTML5

* www - the web server fronting the Flask servers (nginx) and serving up html to view editor.  There is uwsgi, a load baklancer, and a editor / webview

* thirdparty - TinyMCE etc

* jenkins - the setup and config for Jenkins CI server, that is used for development purposes

* docs

* deploy - this is a set of fabric files, designed to work wiht a Makefile, and 
  they will deploy the various hosts and servers based on a configuration setup (found in
  global.ini).  

  deployment is done with fabric outside of the scope of the compoinents.  Putting fabfiles or config files that the deploy shal use inside the components is like opening the box using the crowbar found inside.  It leads to confusion.

  

TO recap:

  deployment is dpoine using fabric files, usiong configuration written into global.ini

  before deployment, a staging process is run, basically sed-like, that sets the config for the environment we are in.  THis probably should move to ENV vars.







