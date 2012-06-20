========
Rhaptos2
========

This is the repository for cnx editor.
It is desinged to work primarily as a web app in conjunction with multiple other systems deployed 
using the bamboo setup files

It can be run from a single developer laptop, in a virtualenv.  

The install instructions for that are as follows::

   mkdir -p -m 0777 /tmp/cnx
   cd /tmp/cnx
   git clone https://github.com/Connexions/bamboo.git
   git clone https://github.com/lifeisstillgood/Rhaptos2.git
   

   export LOCALGITBAMBOO=/tmp/cnx/bamboo
   export LOCALGITRHAPTOS2=/tmp/cnx/Rhaptos2


   cd bamboo/
   bash ./update_venv.sh localenv

   You should then see an update saying:

   <yourpath>/bin/python -c "from rhaptos2.repo import e2repo; e2repo.app.run(debug=True, use_reloader=False)"   

   run this in one terminal

   open your webbroswer to 

   http://localhost:5000/

   you should see a simple editor.

   


to recap::

  deployment is dpoine using fabric files, usiong configuration written into global.ini

  before deployment, a staging process is run, basically sed-like, that sets the config for the environment we are in.  THis probably should move to ENV vars.







