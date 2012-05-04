====================
Logging with Frozone
====================

When we talk about logging we essentially mean three different
things

1. metric gathering
2. auditing (passive monitoring)
3. pokeing (active monitoring)


metric gathering for me provides 2 outcomes for the price of one.
We can see if the number of print jobs 

auditing is a process of finding out *why* the metrics changed.
Usually storing log messages, enabling us to find out more
sensibly what is going on, it is the process of sanley putting
print statements into your code.

pokeing - either treating it as a service, A further approach to
auditing is to debug - watch the stack change during a run and
analyse it more closely.  This is not part of logging as I see it.


Summary
-------

We want to log 2 things - metrics and messages.

We use statsd / graphite for the first, and syslogd or facebook's
scribe.





Graphite / Statsd
=================

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

I am recommeding building graphite / statsd entirely on a virtual
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


Server::

  /etc/rsyslog.conf
    
  # provides TCP syslog reception
  $ModLoad imtcp
  $InputTCPServerRun 514

  uncomment the above two lines - we now listen for TCP connections

now::

  reload rsyslog



src machine::

  </etc/rsyslog.conf>
  #attempt to forward allloggingto cnx4                                                     *.* @@cnx4.office.mikadosoftware.com

note the double @ symbol - means send by TCP




/etc/rsyslog.d/50-default.conf

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
