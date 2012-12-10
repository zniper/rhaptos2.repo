.. Paul Brian, Michael Mulich, (C) 2012 Rice University

   This software is subject to the provisions of the GNU Lesser General
   Public License Version 2.1 (LGPL).  See LICENSE.txt for details.

=============
rhaptos2.repo
=============

This is the repository for Connexions editor.  It is designed to work
primarily as a web application in conjunction with multiple other systems
deployed using the bamboo setup files.

See the `Connexions development documentation
<http://connexions.github.com/>`_ for more information.


Quick developer install 
-----------------------

This will install repo, with simple defaults, ready for developer use
Basically curl the startup script (quickdownload.sh).  Run that with 
an argument of an *empty* dir you want to use for the source and repos.
THen this will download the repo, and dependancies, setup the virtualenv
and tell you what commands to then run.

::

   $ cd ~
   $ curl -O https://raw.github.com/Connexions/rhaptos2.repo/master/quickdownload.sh
   $ bash quickdownload.sh /tmp/testrepo1 # <- replace with any empty dir you like
 
You will now be given a set of commands to run::

    You need to change the following parts of the ini file:
    rhaptos2repo_aloha_staging_dir=/tmp/testrepo1/src/aloha
    then you can 
    cd /tmp/testrepo1/venvs/vrepo; source bin/activate
    cd /tmp/testrepo1/src/rhaptos2.repo/rhaptos2/repo;
    python run.py --debug config=../../local.ini
    At this point you should see a runing instance


Known Issues
------------

1. With a localhost install you cannot sign in with OpenID.  This will
   need to be fixed with a workaround. TBD

Install
-------

The following will setup a development install. For instructions about
a production deployment, go to http://connexions.github.com/ .

Pre-requisites::

     Python 2.7 (with header files)
     Bash >=4.0      (system dependant)
     Internet access (!)

Python setup::

   We will need the system version of Python to
   have pip and virtualenv installed.

   curl -O http://peak.telecommunity.com/dist/ez_setup.py
   sudo python ez_setup.py
   sudo easy_install pip      
   sudo pip install virtualenv
   
Other things to check

::

   We need to build lxml - so we need headers for the below, as 
   pip will compile. And easy_install not use requirements!
   
   apt-get install libxml2-dev
   apt-get install libxslt1-dev


You should now have correct system environment, and we shall 
build our own virtual environments to work on.

1. Download source code

::
   
   cd ~
   mkdir -p -m 0755 src
   mkdir -p -m 0755 venvs
 
   (Of course where you put the above is a matter of personal choice)

   cd src
   git clone https://github.com/Connexions/rhaptos2.repo.git
   git clone https://github.com/Connexions/rhaptos2.common.git

   $ ll
   drwxr-xr-x  5 pbrian  pbrian  11 Oct 18 18:22 rhaptos2.common
   drwxr-xr-x  6 pbrian  pbrian  15 Oct 18 18:22 rhaptos2.repo

There is a "helper" script in rhaptos2.repo -> "buildvenv.sh"

It is explicitly designed to install a virtualenv and can be run as follows::

   $ bash buildenv.sh ~/venvs/myvenv ~/src/rhaptos2.common ~/src/rhaptos2.repo

This will create a virtualenv in ~/venvs/myenv and look for requirements.txt files in the folders pointed to by all subsequent arguments.  These requirements.txt will be installed in the venv.

FInally :command:`setup.py develop` will be run in the pkgdir argument locations (src/rhaptos2.common etc)

2. ALter local.ini

 (TBC)


lets run the repo::

   cd ~/venvs/dev
   . bin/activate
   (dev) python run.py --debug --config=../../local.ini --port=8000
   * Running on http://127.0.0.1:8000/

So what just happend?

1. We have created a venv for a developer, where the code they are
   likely to change (rhaptos2.repo, common) are effectively symlinked
   into the venv (not quite true - see setup.py develop)

2. then we activate this venv

4. run a script that instantiates the repo correctly.  Host and port are configurable.


Deployment
----------

This is designed to be deployed into environments as follows::

   cd ~/src  
   git clone https://github.com/Connexions/bamboo.recipies.git

   cd ~/venvs/dev
   . bin/activate
   (dev) cd ~/src/bamboo.scaffold/bamboo/scaffold/scripts/
   (dev) . ./repo_config.sh && python controller.py --recipie rhaptos2repo stage build test deploy

The above will stage (move files, apply patches), build, create a
venv, run unit tests, and deploy into the web servers set in config,
using sshkeys set in config etc.

Third Party code
----------------

We rely on third party code.  
Eventually we shall pull all dependancies out into a stageing process.
For now pretty much all dependnacies (ie bootstrap.css) is in the static folder of Flask.  However, we are developing in parallel with Aloha, 
so we track the cnx-master branch of that - to do so clone Aloha into
a directory and point Flask at it (Flask will serve that cloned dir from 
localhost) ::

  In local.ini set: rhaptos2repo_aloha_staging_dir=/my/path
  cd /my/path
  git clone https://github.com/wysiwhat/Aloha-Editor.git
  git checkout cnx-master




