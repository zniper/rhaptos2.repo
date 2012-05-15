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



.. toctree::
   :maxdepth: 1


   install-os
   fabfiles
   jenkins
   logging
   config
   webservers
   OS-Build

