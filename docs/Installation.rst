=======================
Installing and updating
=======================


We shall be using Jenkins to do the majority of the installation,
however there is a lot to it, so here is details on how to do the
installation of the frozone eco-system (for want of a better term) and
links to the source.


Overview
========

We are using several servers, some as repositories, some as logging
servers etc.  To do this without having m,ultiple physical hosts, we
use a form of virtualisation called Linux Containers.

We also place all the hosts onto a NAT'd LAN inside a developer's
office.

This has lead to difficulty arranging servers visible for everyone,
and updated regularly.  The most likely solution is to truly develop
in the open - by hiring rackspace servers and putting the latest CI
build onto there.


Firstly we install an instance of Ubuntu on our dev server, and modify it so that
we can use Linux containers.  At this point we can use different fab files to
turn it into a variety of different servers.

.. toctree::
   :maxdepth: 1


   install-os
   fabfiles
   OS-Build

Now we want to build a DNS server

.. toctree::
   :maxdepth: 1

   dns

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


