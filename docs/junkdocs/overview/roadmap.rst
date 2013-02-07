=======
Roadmap
=======

This is a draft roadmap for project Frozone - the new editor component
for cnx.org.  It will be continuously changing, as will much of the
documentation here, and I apologise in advance for half-formed
thoughts slipping in.


Talking about the Roadmap
-------------------------




cnx.org is big.  Not massive, but big in that it covers a lot of
ground, and complexity, and has already existing standards for SLAs,
community use and plenty of expectations.  This is not necessarily a
problem, but it is an important constraint.

It is probably fair to call cnx an ecosystem - that is the type and
range of interactions are not trivial or easily predictable.  for
example, anything to do with pdf generation.  Sometimes we look at
these hard to predict interactions and blame ourselves - we should
have been clever enough to spot it, prescient enough to write a test.
Sometimes that is true, sometimes it is not, and telling the
difference can save us from both emotional hand wringing and
unnecessary or futile work trying to tame the beast. (Fred Brooks'
essential and accidental complexity apply here).

But why refer to ecosystems - because that is what modern day software
systems have become.  Platforms, perhaps, but interacting, and doing
so in complex and shifting patterns.

And eco-systems have some interesting qualities

1. They evolve, rather than grow from master plans, and roadmaps

2. They use selection (artificial or natural).  So things need to be
   able to die.  And to be measured in some fashion, if we are the
   ones to cause thier death.

3. organisms, like cells, have well, an inside and an outside and a
   well defined difference.  And so we should think of creating
   services, like organims, with defined inside and outsides.

4. Yes I am talking service orientated architecture, but think more
   like organisms.

5. in between organsims is - well the transmission environment -
   sounds, smells, sight.
   


* SOA and devops - comments by Steve Yegge on Amazon's experiences
  https://plus.google.com/112678702228711889851/posts/eVeouesvaVX


Summary
~~~~~~~

I am expecting us to produce a Service Orientated Architecture - components talking to compoentns
through defined interfaces, and acting in robust and defensive manners.  


Architecture
------------


A big focus on decoupling services and providing resilience,
'do-one-thing-well' approach.

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

Python REST client
~~~~~~~~~~~~~~~~~~

This is still a massive requirement.  As you can see in frozone, a python POST client is trivial.
But we need a relaible client, that can handle network outages, retry, avoid breaking non-idempotency,
can deal with a wide range of errors and tests.  Can be part of a test / monitoring suite.



Repo/server split.  I have intuitively split the backend into two - e2server and e2repo.  e2server is 
where the AJAX client talks, and e2repo is what the e2server calls down to for POST, GET of the actual modules.
Nah I am being a bit dense.  There is nothing that the e2server -> e2repo cannot do that is not better done by exposing
e2repo directly, and having a shared message queue.  My usecases were something like ::

  * translate urls ala bit.ly from meaningful to canonical
  * server front ends the repo, so we can shift storage as and when.  Well REST webserver on e2repo does that quite well enough
  * server might want to perform other functions - like translate html5 > cnxml and then push cnxml to legacy repo.
    It can by listening on e2repo message queue.



Development
-----------

* git, git flow, gerrit.
  I need to stop pushing direct to Master, and expect that someone will be joining me.  Stop being lazy Paul.

* documentation - need to iron out a sphinx bugs.  Plus got a hack hack for javascript docs.

* Coding standards. PEP8 

e2client design
~~~~~~~~~~~~~~~

Want to see good examples of lazy loading the client, and how we can most effectively work with a real desinger (you know , they own the CSS, and can change certain parts of HTML, etc)  Dont be too prescriptive here but be aware.



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

