=================================
Build and configure a host server
=================================




I am expecting to parameterise these configs, based on FreeBSD /
Ubuntu, versions thereof, and whether things are virtualised.  I am
leaving that extra complexity alone for now, and focusing on ubunut
containers.

The configuration and server setup (network on VHost, installing 3rd
party packages) is to be controlled thorugh fabric for now.


basic notes
===========

The basic way to run a fabric deployment is on the command line call::

   $ fab -H www.example.com www2.example.com put_website

This will look for a file fabfile.py, and will execute the function
:func:put_website() in that file twice, once connected to www and once
at www2.  (We assume the users have correct ssh authorized_keys etc)

However, the fabfile.py can get very large quickly.


a :file:fabfile.py defines all the deployment capabilities of a given project.  
if in the file we import :file:cnxfab.py as follows::

    from fabfile-cnx import foo, bar 

then foo and bar will be available as *tasks* to fab as well. I tend to split the files into 
deployments of specific 3rd party servers, so ::

    import fab-oracle
    import fab-nginx 


and the different fabfiles can do more specific customisation, so fabfile-cnx.py may do clefver things with nginx
installs, and just call fab-nginx.install_nginx(), then do a unusual config.

    

using fabric::

   $ fab -f myfabfile.py -H deploy@cubea deploy@cubeb put_networkinterfaceconfig


using parameters

   $ fab -h hpcube task:foo=bar



Moniotring Virtual Hosts
------------------------

::

  fab -H hpcube,cubea -- dpkg -l
  fab -H hpcube,cubea -- uname -a
  fab ... other things like get resolv.conf and network/interfaces
  firewall setups ...



