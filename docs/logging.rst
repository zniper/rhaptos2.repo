====================
Logging with Frozone
====================

When we talk about logging we essentially mean three different
things

1. metric gathering
2. auditing (passive monitoring)
3. pokeing (active monitoring)

Auditing is what we usually think of as logging.  It is usually stored
in text files, telling us what *has* happened, using *messages* sent
from the code, when a developer thinks that is a good idea (often
after an exception).

We can append a message to the log file as follows::

    lg.warn('the pdf for user %s collection %s failed on server %s\
    with err %s')

We shall use the standard *syslog* for this, but forward all collection
of logs to a central syslog server.



Metric gathering is really about graphing and seeing what is going
right / wrong over time.  

We can do this as follows::

   import statsd
   c = statsd.StatsClient(STATSD_HOST, STATSD_PORT)
   #...
   c.incr('frozone.statsd.test')




Pokeing, my term is derived from this `Steve Yegge
<https://plus.google.com/112678702228711889851/posts/eVeouesvaVX>`_
post.  There is a spectrum between testing a web-service, seeing if it
returns 4 when asked 2+2, and determinng if it is up, responding under
load, and so on.  We will develop monitoring of a web service, that will 
be indistuinguishable from QA testing of that service.





Graphite / Statsd
=================


Summary 
-------

::

   make lxc-destroy host=hpcube fabfile=deploy/fab_lxc.py vhostname=devlog vhostip=10.0.0.22
   make newcontainer host=hpcube fabfile=deploy/fab_lxc.py vhostname=devlog vhostip=10.0.0.22
   ping devlog ...
   make graphite host=devlog fabfile=deploy/fab_sys_graphite.py

.. warning::
   
   This is not fully automated install, and is unlikely to be due
   to nature of config changes=, and that it is part of
   infrastructure so automation monkey sits on sysadmin not
   devops.


It seems that the popularity of this approach came from a `blog
post
<http://codeascraft.etsy.com/2011/02/15/measure-anything-measure-everything/>`_,
which might explain a lot.

Anyway, the architecture is relatively simple.  

* Your code uses statsd library, which opens a UDP socket to the
  statsd server

* the statsd server is a node.js server, that listens for ten
  seconds, gathers each 'foo.bar' message, and averages them over
  10 seconds and passes it to the graphite server

* the graphite server, which can be seen as a single whole when
  frankly it is not, creates a new metric

Carbon is the database (rrd-alike), graphite is the
web-server-display and whisper is the listening server feeding
carbon.  I think.


advantages of the approach

1. You can create any metric on the fly. foo.bar.wibble.ct is
   meaningful.

2. its network-aware, simple and pretty bullet proof.

Example
-------

.. figure :: graphite_web.png
   :scale: 50%


Todo

* run statsd under supervisord
* some basic internal 


Install
-------

I am recommending building graphite / statsd entirely on a virtual
server.  There are a large number of dependancies and
configuration issues, and when the whole service is conceptually
'just a box over there', you may as well make it a box over there
and not worry.

So, create a lxc container as discussed elsewhere, and the set up the sys level server using :

.. automodule:: frozone.deploy.fab_sys_graphite
   :members:




biblio
------

http://www.facebook.com/note.php?note_id=32008268919
http://geek.michaelgrace.org/2011/09/how-to-install-graphite-on-ubuntu/

no change to wsgiimportscript


::

 root@cnx4:~# tcpdump -tnX port 8125
 tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
 listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
 IP 10.0.0.102.17723 > 10.0.0.14.8125: UDP, length 23
 0x0000:  4500 0033 918a 0000 4011 d4bc 0a00 0066  E..3....@......f
 0x0010:  0a00 000e 453b 1fbd 001f f6ce 6672 6f7a  ....E;......froz
 0x0020:  6f6e 652e 7374 6174 7364 2e74 6573 743a  one.statsd.test:
 0x0030:  317c 63                                  1|c



Logging - audit style
=====================

Using syslog - or rather the Ubuntu version rsyslogd.

rsyslogd still seems to have a few bugs to be ironed out in ubuntu,
but it has been well tested in the Debian world, and is simplest
solution we have for now.

The setup - we shall have *one* remote server, the logging server,
that will collate all logs sent by the other servers.  All client
servers will log to their local drives and forward on over tcp to the
remote logging server.

configuration
~~~~~~~~~~~~~

rsyslog is installed and enabled by deafualt in Ubuntu since (?).  We
will want to change the default listening port from 514 to 5514 (bug:
following a drop in privileses from startup user to syslog:syslog,
ports below 1024 seem inaccessible)

The clients obviously need to be told to log in that direction.

We also want to turn off the default beahviour of writing some errors
to the xconsole, as we have non X machines.

We also want to configure the Python scripts to use local syslog
socket ('/dev/log')



Server::

  /etc/rsyslog.conf
    
  # provides TCP syslog reception
  $ModLoad imtcp
  $InputTCPServerRun 5514

  uncomment the above two lines - we now listen for TCP connections


now::

  sudo service rsyslog restart 



src machine::

  </etc/rsyslog.conf> 
  #attempt to forward allloggingto cnx4 
  *.* @@cnx4.office.mikadosoftware.com:5514

note the double @ symbol - means send by TCP


Turn off silly xlogging - this is a known issue in Ubunutu::

  /etc/rsyslog.d/50-default.conf

    We need to comment out the below in 
    /etc/rsyslog.d/50-default.conf
    (https://bugs.launchpad.net/ubuntu/+source/rsyslog/+bug/459730)


    #daemon.*;mail.*;\
    # news.err;\
    # *.=debug;*.=info;\
    # *.=notice;*.=warn |/dev/xconsole

    thus stopping rsyslog trying to log to a X server console on a X-less box.
  
  
::

    Path to syslog config file:
    /etc/rsyslog.conf

    Syslog PID file
    /var/run/rsyslogd.pid

    Path to syslog server
    /usr/sbin/rsyslogd

    Command to start syslog
    service rsyslog start

    Command to apply changes
    service rsyslog reload

    Command to re-open log files
    service rsyslog restart


Logging in Python
=================

We are needing to look at various different module hierarchies.
I am assuming the following



::

    #!/usr/local/bin/python
    #! -*- coding: utf-8 -*-


    '''
    '''


    import logging
    from logging.handlers import SysLogHandler
    from frozone import conf

    #needs a test if syslog is actually up...

    def getFrozoneLogger(modname):
	'''simple, pre-configured logger will be returned.
	'''
	lg = logging.getLogger(modname)
	lg.setLevel(conf.LOGLEVEL)
	ch = SysLogHandler(conf.SYSLOG_SOCK)
	lg.addHandler(ch)

	return lg

	import logging
	lg = logging.getLogger(__name__)


Where do we find the grpahite database?
---------------------------------------


* /opt/graphite/storage
::

   $ sqlite3 graphite.db
   >> select * from sqlite_master;

   .help

    sqlite> .databases
    seq  name             file                                                      
    ---  ---------------  ----------------------------------------------------------
    0    main             /opt/graphite/storage/graphite.db                         

    sqlite> .tables
    account_mygraph             auth_user_groups          
    account_profile             auth_user_user_permissions
    account_variable            dashboard_dashboard       
    account_view                dashboard_dashboard_owners
    account_window              django_admin_log          
    auth_group                  django_content_type       
    auth_group_permissions      django_session            
    auth_message                events_event              
    auth_permission             tagging_tag               
    auth_user                   tagging_taggeditem 
  

    > select * from auth_user;
    1|root|||paul@mikadosoftware.com| ....
    THis is what I created at fabfile time


Getting to the data on disk
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> import whisper
    >>> whisper.info('/opt/graphite/storage/whisper/rhaptos2/carbon/verify.wsp')
    {'maxRetention': 157784400, 'xFilesFactor': 0.5, 'aggregationMethod': 'average', 'archives': [{'retention': 21600, 'secondsPerPoint': 10, 'points': 2160, 'size': 25920, 'offset': 52}, {'retention': 604800, 'secondsPerPoint': 60, 'points': 10080, 'size': 120960, 'offset': 25972}, {'retention': 157784400, 'secondsPerPoint': 600, 'points': 262974, 'size': 3155688, 'offset': 146932}]}



biblio:
~~~~~~~

http://www.aosabook.org/en/graphite.html
http://graphite.readthedocs.org/en/0.9.10/index.html
http://stackoverflow.com/questions/7099197/tracking-metrics-using-statsd-via-etsy-and-graphite-graphite-graph-doesnt-se

  
Issues to note
~~~~~~~~~~~~~~

Logger instances *hang around* - they are designed as singleton
servers, so creating them a lot really can hurt. One logger per
running module is a good balance of granualrity and manageability.

Logging usernames etc is important, and we shall developer either a
LoggerAdapter approach or just keep it in parameters passed, depending
on how the app evolves.  Watch this space.

graphite:

Do not publish updates faster than the minimum interval in
your storage-schemas.conf file.

This means that the statsd aggregator and the storage-schemas.conf
*must* be in sync else if carbon aggreagtes every minute, but statsd
pushes every 10 secs you will have statsd overwrite its own records
5/6 of the time

Note that this will not mean we can carry forward absolute metrics - we get averages 
over the minumum sampling time.  This can be a problem if our traffic is bursty.
As either statsd or carcbon will eventually average out our bursty ness.
 

To Do:

There is a lot to do here - setting timespans of logging
granualrity. using and setting up the graphite as a stort of
dashboard.
