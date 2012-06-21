========
Rhaptos2
========

This is the repository for cnx editor.
It is desinged to work primarily as a web app in conjunction with multiple other systems deployed 
using the bamboo setup files

It can be run from a single developer laptop, in a virtualenv.  

The install instructions for that are as follows::

   dependancies:

    pip install virtualenv
    pip install fabric

   Please ensure these are available system-wide or run them from your own virtualenv (Not tested)    

   All else should get put into a virtualenv so is not a dependancy really.

   Set up as below:

   mkdir -p -m 0777 /tmp/cnx
   cd /tmp/cnx

   git clone https://github.com/Connexions/bamboo.git
   git clone https://github.com/lifeisstillgood/Rhaptos2.git
   
   cd bamboo/
   bash ./newstarter.sh

   You should then see an update saying:

   export CONFIGFILE=/tmp/cnx/bamboo/conf.d/rhaptos2.ini.localhost && /tmp/mikado/venvs/testenv/bin/python /tmp/mikado/venvs/testenv/bin/rhaptos2_runrepo.py --host='0.0.0.0' --port=5000 --debug=True

   run this in one terminal

   open your webbroswer to 

   http://localhost:5000/

   you should see a simple editor.

   


to recap::

  deployment is done using fabric files, using configuration in ENV vars or in file.

  before deployment, we run a build process - basically sed-like, that sets the config 
  for the environment we are in. 






