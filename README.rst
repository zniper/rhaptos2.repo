========
Rhaptos2
========

This is the repository for cnx editor.
It is desinged to work primarily as a web app in conjunction with multiple other systems deployed 
using the bamboo setup files

It can be run from a single developer laptop, in a virtualenv.  

The install instructions for that are as follows::




   vitualenv
   bash > 4
   fabric
   Access to pypi.python.rg

   Please ensure these are available system-wide or run them from your own virtualenv (Not tested)    

   All else should get put into a virtualenv so is not a dependancy really.

   Set up as below:
   
   mkdir -p -m 0777 /tmp/cnx/workspace/
   cd /tmp/cnx/workspace/

   git clone https://github.com/Connexions/bamboo.git
   git clone https://github.com/lifeisstillgood/Rhaptos2.git
   

   cd bamboo/
   bash deploy-rhaptos2.sh localhost /tmp/cnx/workspace/bamboo/conf.d/rhaptos2.ini /tmp/cnx/workspace

   

   It should then install and run the below command 

   export CONFIGFILE=/home/pbrian/cnx/bamboo/conf.d/rhaptos2.ini.localhost && /tmp/cnx/workspace/venvs/testenv2/bin/pythopn /tmp/cnx/workspace/venvs/testenv2/bin/rhaptos2_runrepo.py --host='0.0.0.0' --port=5000 --debug=True

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






