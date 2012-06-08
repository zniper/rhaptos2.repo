============
Architecture
============

.. toctree::

   design-discussion.rst
   overview.rst
   roadmap.rst


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
