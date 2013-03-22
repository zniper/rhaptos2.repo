============
Architecture
============

.. toctree::

   design-discussion.rst
   overview.rst
   roadmap.rst


Supporting HTTP Status Codes fully

We want to support the flow as shown here 
http://i.stack.imgur.com/whhD1.png
and deploy a wrapper and test clietns to ensure it.



Some thoughts
=============

We are intending to create a architecture that will elegantly solve the use-cases presented (:doc:`usecases`)

We want to use network provided services, which will ensure those services can be scalable and robust using sensible, well understood principles (i.e. cacheing, load-balancing, sharding - all those good bits of jargon)

Where we should split the architecture into these service-components is a good question and this is draft 0.1


* Text will be stored on a file-system.  We should expose this file system as a service.  Yes, you heard, the file system is a service, over the network. 
The file system will then be scalable, probably on a simple shard basis.
This smacks a little of premature optimisation.  But it will only be accessible via the front end servers.  It is also a good way to isolate issues like getting versions of files, and getting 

This also means we could use `DRBD <http://www.drbd.org/>_`-style file system clustering to ensure we get nice replication.

Again phase II I think

* publication - fairly obviously 


Why is git and why is git not a good backend
--------------------------------------------

Why not
~~~~~~~

* A collection is the tree.

WHy
~~~

* Branching and merging is a valid use case.

Bibilography
~~~~~~~~~~~~

Please read github's architecture discussions for some interesting
background

* https://github.com/blog/530-how-we-made-github-fast
* http://www.anchor.com.au/blog/2009/09/github-designing-success/


Repository platform
-------------------

The repo sits on Ubuntu 11.10 and expects to migrate painlessly to 12.04(LTS)Ther repo is an nginx pair of load balanced 

upstream serving
http://wiki.nginx.org/HttpProxyModule

.. figure:: graphite_load_bal.png
   :scale: 50 %
   
We can see the use of nginx as a simple load balancer for two backend instances of Flask.  I create two instances using ::

 $ service rhaptos2 start PORT=7999
 $ service rhaptos2 start PORT=7998

and configure nginx as ::

 upstream repobk  {
   server devweb:7999 weight=5;
   server devweb:7998 weight=5;
 }
 



load balancing
http://library.linode.com/linux-ha/highly-available-load-balancer-ubuntu-10.04
LVS ? 

Repository Architecture
-----------------------



