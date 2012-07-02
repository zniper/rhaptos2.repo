=============
rhaptos2.repo
=============

This is the repository for cnx editor.  It is desinged to work
primarily as a web app in conjunction with multiple other systems
deployed using the bamboo setup files

It can be run from a single developer laptop, in a virtualenv.  
There are some disclaimers however, YMMV.

If you are interested in contributing to the project we are open for
business, please visit
http://frozone.readthedocs.org/en/latest/index.html for details on how to setup full development versions.


The install instructions for that are as follows::


   Pre-requisites

   1. You will need to have the Python Header files installed in the 
   correct location.  This can either be achieved by compiling from source
   or if on debia/ubuntu running 
  
    $ apt-get install python-dev

   2. You will also need at a system level

     fabric          (pip install fabric)
     virtualenv      (pip install virtualenv)
     bash >=4.0      (system dependant)
     Internet access (!)

   All else should get put into a virtualenv that will be
   automatically created so is not a dependancy really.

   Set up as below:
   
   #location of the working tree (code)
   mkdir ~/cnxcode
   #location of everything else 
   mkdir -p -m 0777 /tmp/cnx/workspace/   
   #Just to explain this, the source code is stored in one location,
   # then cp'd to workspace where it will be setup with config,
   # built, compiled and deployed.

   cd ~/cnxcode

   git clone https://github.com/Connexions/bamboo.git
   git clone https://github.com/Connexions/rhaptos2.repo.git
   then:
       git checkout 0.0.3 in both directories
    

   cd ~/cnxcode/bamboo/
   bash deploy-local.sh localhost ~/cnxcode/bamboo/conf.d/rhaptos2.ini ~/cnxcode/

   

   It should then install and run on port 5000 automatically, in the foreground of the terminal.

   open your webbroswer to 

   http://localhost:5000/

   you should see a simple editor.
   Please signin using google openid account (no others tested yet)


Disclaimers::

   The compilation and setup of the repo on a local laptop is not guaranteed.
   We trap pysqlite compilation failures and rebuild statically, but there is no guarantee we can build locally on your system.  THis has only been tested on ubunutu 12.04.




to recap::

  deployment is done using fabric files, using configuration in ENV vars or in file.

  before deployment, we run a build process - basically sed-like, that sets the config 
  for the environment we are in. 






