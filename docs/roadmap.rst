=======
Roadmap
=======

Roadmap for project frozone - new editor for Cnx.org

* architecture
* devops 
* build/deploy
* development
* server farm
* testing

For week three I propose a focus on infrastructure.

Architecture
------------


A big focus on decoupling services and providing resilience, 'do-one-thing-well' approach.
This will throw up unusual issues. The first is already with us.  I decided to have two 
1. REST 
2. Message Queues.

I am epxecting there will be pyRESTServers - a complete, scalable up and down chunk consisting of

* http transparent cache (Varnish)
* webserver (Flask in uWSGI wrapper)
* message queue to handle asynchonicity (RabbitMQ)
* dont expect a data response in the same request / response cycle, expect a redirect to a GET.





python-rest-library

* The repo/server split has thrown up an important issue.  We need to (find/build) a robust 
  library for 

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

