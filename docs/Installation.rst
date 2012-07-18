=======================
Installing and updating
=======================

Heroku has proven an interesting case study in large scale deployment
of many many apps.  The founders there have published an opinionated
view of how to structure deployment and applications at
`http://www.12factor.net/`_

One interesting takeaway is to ::


  Keep development, staging, and production as similar as possible

This (along with most of the other 11 ideas) I generally agree with
(frankly its all a bit common sense).  Anyway.

This means that in production if we think we are going to have a range
of webservers running our app, that we should at the very least have
two web apps running in development.  And they should be installed and
monitored the same way as they will be live.

What I am saying is that we are beyond just downloading one egg and
running the code.  We need deployment scripts just to get started.



Overview
========

There are two main deployment targets during development

1. Developer's local office

2. Rackspace Cloud servers

I  have assumed  that  each developer  will  have at  least a  virtual
machine of Ubuntu running  locally at an acceptable speed.  Personally
I  have  an  entry  level   server  running  Linux  Containers,  as  a
lightweight solution. YMMV

The idea is that at a very minimum, we shall install the repository
and web server(s) onto a clean virtual machine, and run the
'eco-system' from there.  There will be (minimal) system wide alterations to the developers real local system.




We are using several servers, some as repositories, some as logging
servers etc.  To do this without having m,ultiple physical hosts, we
use a form of virtualisation called Linux Containers.

We also place all the hosts onto a NAT'd LAN inside a developer's
office.

This has lead to difficulty arranging servers visible for everyone,
and updated regularly.  The most likely solution is to truly develop
in the open - by hiring rackspace servers and putting the latest CI
build onto there.


Firstly we install an instance of Ubuntu on our dev server, and modify
it so that we can use Linux containers.  At this point we can use
different fab files to turn it into a variety of different servers.


My Walkthrough
--------------

I am starting with a configured host server, able to run LXC.

1. Delete the existing devweb and devlog servers.
2. Delete the existing Jenkins server
3. rebuild the above three servers as base OS's
4. Apply different fabfiles to the three (devjenkins, devlog and finally
   devweb) to build the system environment.
5. Run a Jenkins job, to rebuild devweb, seeing results of nosetests

1. Check dns. I want to make sure my local DNS server is serving the right
   setup.  (THere is a DNS fabfile but I am manually handling it for now)::

     bash scripts/dns.sh
      devweb
	  10.0.0.24
      devjenkins
	  10.0.0.23
      devlog
	  10.0.0.22
      www
	  devweb.office.mikadosoftware.com. 10.0.0.24
      cdn
	  devweb.office.mikadosoftware.com. 10.0.0.24
      repo

2. kill running containers::

     make lxc_destroy host=hpcube vhostname=devlog vhostip=10.0.0.22
     make lxc_destroy host=hpcube vhostname=devweb vhostip=10.0.0.24
     (Not killing jenkins just yet.)

3. recreate ::

    see newlxc.sh
    export CONFIGFILE=/etc/rhaptos2.ini
    make newcontainer host=hpcube   fabfile=deploy/fab_lxc.py vhostname=devweb vhostip=10.0.0.24
    make newcontainer host=hpcube   fabfile=deploy/fab_lxc.py vhostname=devlog vhostip=10.0.0.22
  
Now the CONFIGFILE has become vital in almost all parts of Bamboo and Rhaptos2.  As we have a build / deploy 
process, I am not making any (?) default assumptions, but taking it all from a config file, which clearly needs
to be supplied, else I dont know if I am building for produiction or developer. 
     

4. Now each server should have Ubunut base plus bunch of Python additions
   (NB rember debian puts python packages in dist-packages, just to confuse you)
   ::


     make graphite host=devlog fabfile=deploy/fab_sys_graphite.py

     This will ask a couple of [continue] questions, say yes. 
     It will then run a grap[hite supplied dependancy check.  I allow one error/warning - txamqp to pass.  Anything else investigate.

     It then drops you into a fab run shell on remote machine.  THis sets up a
     DJango user - I take the defaults, and when complete you *need to _exit_* 
     from the remote shell so fabric can continue

     At this point Apache is restarted - any nginx conflicts will arise here.




5. test stats::


     http://devlog
     python verify_graphite.py in test dir

     ToDo: expand on this    


6. make repo::

    make repo host=devweb fabfile=deploy/fab_sys.py

    Actually the whole build/deploy the repo is a little more involced, please see ...
   
7. run Jenkins job to build repo and web servers





.. toctree::
   :maxdepth: 1


   install-os
   fabfiles
   OS-Build

Now we want to build a DNS server

.. toctree::
   :maxdepth: 1

   dns
   hosting
   lxc-routing

At this point the Virtual Lan for our developer is ready to take on anything new

.. toctree::
   :maxdepth: 1


   jenkins
   logging
   config

Now we install the application itself

.. toctree::
   :maxdepth: 1

   webservers


