=======
Roadmap
=======

This is a draft roadmap for project Frozone - the new editor component for cnx.org.
It will be continuously changing, as will much of the documentation here, and I apologise in
advance for half-formed thoughts slipping in.



Architecture
------------


A big focus on decoupling services and providing resilience, 'do-one-thing-well' approach.

This will throw up unusual issues. The first is already with us.  I decided to have two 

1. REST 
2. Message Queues.

PyRESTServers
~~~~~~~~~~~~~

I need a better name, but the concept is simple - a defined, stand alone, cluster-able set of 
services that work together to provide some REST based server, that will do (one) thing well.


* http transparent cache (Varnish)
* webserver (Flask in uWSGI wrapper)
* message queue to handle asynchonicity (RabbitMQ)

If I can put the architecture I would like to see in one sentence it would be::

  Dont expect a *data* response in the same cycle as your request - instead expect a link to a new URL.

If we can build our *clients* this way (building servers this way is fairly simple) we can 
expect to solve a lot of our decoupling issues.  I think we shall need two AJAX client libraries 
one in Python, one in JQuery that have this as their heart.  

Repo/server split.  I have intuitively split the backend into two - e2server and e2repo.  e2server is 
where the AJAX client talks, and e2repo is what the e2server calls down to for POST, GET of the actual modules.

But it is not a clean split - for example what is the canonical URI for a module now.  e2server/module/123 or e2repo/module/123 ?  But if we use e2server, then the repo is not easy to replace with new technology.

Needs some thought.


Development
-----------

* git, git flow, gerrit.
  I need to stop pushing direct to Master, and expect that someone will be joining me.  Stop being lazy Paul.

* documentation - need to iron out a sphinx bugs.  Plus got a hack hack for javascript docs.

* Coding standards. PEP8 


Devops
------

* CI server - Jenkins
* LXC / Jails for in house server farm.
* DO we bother with GAE? AWS will just use Jenkons,  but GAE???
* Fabfile rollouts, kill that shell script.
* Testing - have selenium, Python asserts, doctests.  How to collate those results - I expect a web logging process. 
* logging - see above.  This is important in debugging too - already we have three remote environments not logging to one central place.
* error handling - this is where testing, logging etc early on really embed the basics.  

How do we build, deploy, monitor early on.  Makes production support much much easier.
 
Build/deploy
------------

See Devops and Jenkins

