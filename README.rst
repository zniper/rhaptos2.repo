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

Install
-------

The following will setup a development install. For instructions about
a production deployment, go to http://connexions.github.com/ .

Pre-requisites

     Python 2.7 (with header files)
     Bash >=4.0      (system dependant)
     Internet access (!)

Other things to check
::
   We need to build lxml - so we need headers for the below, as 
   pip will compile. And easy_install not use requirements!
   
   apt-get install libxml2-dev
   apt-get install libxslt1-dev



::

   curl -O http://peak.telecommunity.com/dist/ez_setup.py
   sudo python ez_setup.py
   sudo easy_install pip      
   sudo pip install virtualenv

You should now have correct environment.
We shall build firstly the developer venv

::
   
   cd ~
   mkdir -p -m 0755 src
   mkdir -p -m 0755 venvs
 
   (Of course where you put the above is a matter of personal choice)

   cd src
   git clone https://github.com/Connexions/rhaptos2.repo.git
   git clone https://github.com/Connexions/rhaptos2.common.git
   git clone https://github.com/Connexions/bamboo.scaffold.git

   $ ll
   drwxr-xr-x  7 pbrian  pbrian  14 Oct 18 18:22 bamboo.scaffold
   drwxr-xr-x  5 pbrian  pbrian  11 Oct 18 18:22 rhaptos2.common
   drwxr-xr-x  6 pbrian  pbrian  15 Oct 18 18:22 rhaptos2.repo

   
You will now need 

:file:`requirements.txt`

::

    Fabric==1.4.3
    Flask==0.9
    Flask-OpenID==1.0.1
    Jinja2==2.6
    Werkzeug==0.8.3
    bamboo.setuptools-version==0.1.0
    logilab-astng==0.24.1
    logilab-common==0.58.1
    nose==1.2.1
    pycrypto==2.6
    pylint==0.26.0
    python-memcached==1.48
    python-openid==2.2.5
    requests==0.14.1
    ssh==1.7.14
    statsd==1.0.0
    unittest-xml-reporting==1.4.1
    wsgiref==0.1.2

and now either follow the below cmds or create a bash script::

    ### You will need to have a python system installed
    ### You will need to have virtualenv in your system install too
    ### You will also need to get the requirements.txt file from 
    ### the same location as this file.  Place it at $reqmts

    reqmts=~/requirements.txt
    venv=~/venvs/dev
    mkdir -p -m 0755 ~/venvs

    virtualenv $venv 
    cd $venv
    . bin/activate


    $venv/bin/pip install -r ~/requirements.txt
    ## Install the foolish circular dependancy (SHould be with requirements but...)
    $venv/bin/pip install -y bamboo.setuptools_version


    #### Now we want to have the source code we are working on avail
    #### in the venv.

    list="rhaptos2.repo rhaptos2.common bamboo.scaffold"

    for d in $list
    do
	echo "Working on $d"

	pip uninstall -y $d || echo "$d not installed"
	cd /home/pbrian/src/$d
	$venv/bin/python setup.py develop

    done


We should now have a working virtualenv in :file:`~/venvs/dev`
Check that it is a developer specific one by ::

    $ ls ~/venvs/dev3/lib/python2.7/site-packages/ | grep link
    bamboo.scaffold.egg-link
    rhaptos2.common.egg-link
    rhaptos2.repo.egg-link

lets run the repo::

   cd ~/venvs/dev
   . bin/activate
   (dev) cd ~/src/rhaptos2.repo/rhaptos2/repo
   (dev) . ~/src/bamboo.scaffold/bamboo/scaffold/scripts/repo_config.sh 
   (dev) python run.py
   * Running on http://127.0.0.1:5000/

So what just happend?

1. We have created a venv for a developer, where the code they are likely to change (rhaptos2.repo, common)
   are effectively symlinked into the venv (not quite true - see setup.py develop)

2. then we activate this venv, cd to the main directory of the repo and 

3. push a config file into the system environment.

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

We rely on thirdparty code. Some / much is currently checked into our repo (!)
We need to have ::

  In config set: rhaptos2repo_aloha_staging_dir=/my/path
  cd /my/path
  git clone https://github.com/wysiwhat/Aloha-Editor.git
  


Issues
------

A fair number !

Firstly the config in the environment - only one developer prefers
this so we shall migrate to conf.ini files - but not before Oct 29.

Secondly there is a foolish circular dependancy on
bamboo.setuptools_version.  Extracting meaningful version numbers is
an interesting problem.

Thirdly 

Reading

I suspect we shall want to storngly consider the approaches shown here 
http://stackoverflow.com/questions/4324558/whats-the-proper-way-to-install-pip-virtualenv-and-distribute-for-python

.. http://s3.pixane.com/pip_distribute.png
