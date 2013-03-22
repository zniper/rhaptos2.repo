============
Story So Far
============


Use this page to discover recent changes
========================================

5 June
------

OK, we have pushed a few of the tickets onwards and now have

* *Test REST client* - very much alpha, but provides a working set of
  tests run by nose, that complete after each Jenkins build.  See
  rhaptos2/client

* *Rename Frozone* Oh yes, I have renamed (almost) all of the code to
  be under rhaptos2.  This was driven by Ed's sensible desire to get
  things under publically acceptable namespaces.  The rhaptos2 name is
  not finalised, but I chose it to see hwo much effort the renaming
  would be overall.  Whilst sed did help, it turns out the answer is
  'more than I expected' But the next rename (if rhaptos2 is not
  right) will be speedier.

* *local Developer install* We can build and run from a virtualenv a
  repository on the local machine.  Along with my virtualenv howto (
  http://frozone.readthedocs.org/en/latest/) it is possible just to
  run a local repo (that passes the rest-client tests !) and not have
  to install jenkins or loggers etc.  I will try not to break it :-)

* *API* The REST client tests will encompass the API as shown in
  http://frozone.readthedocs.org/en/latest/requirements.html.  THis
  will test those supported and not yet supported. Please note the
  future API does depend a fair bit on getting the use cases right
  (see below)

* *CI, debugging* For devs using the 'wider' setup of multiple hosts,
  there are improved setup instructions and notes on using CHarles as
  a web debugging proxy - vital when looking at weird JSON bugs.

* *Use Cases* - I am looking to understand the process users will og
  through in editing / merging / publishing in the new architecture,
  so we can more closely match technology to use cases.  Please do
  comment.  (http://frozone.readthedocs.org/en/latest/usecases.html)



23 May
------

We have a working, installed by Jenkins, reporting to Graphite, 
'editor' and file-only repository.

It can be found at `http://www.frozone.mikadosoftware.com/strawman.html <http://www.frozone.mikadosoftware.com/strawman.html>`_

How to use:

1. enter in a module name, using no spaces and alphabetic charaters only
2. enter in some text
3. save
4. the unpublished version will now appear as part of the 'workspace'
   in list format.  You can click on one of these to reload the editor with a   previous version.  
5. change the module name to edit a different module

Every module has a name and a version number.  The name must be unique.

Limitations
-----------

Quite a few.

Firstly username - this is fixed. 
How do we want the hierarchy to descend from username.  
If we have any hiearchy that is not replicable in standard foilder/file 
approach, then the file only repo should be abandoned quickly.

Added to this, indexing / collections will require a real data strcuture,
which begs the question what will we use?  MongoDB seems best but I would like to carefully review the use cases.

Also username is fixed because not solved OpenID / OAuth or implemeted one.
Seems foolish to put in a placeholder username.

So the whole demo uses one logged in user.

Secondly, the editor is rudimentary - I have not incoirporated anything from
Phil as yet.  

:Graphite:

  http://log.frozone.mikadosoftware.com/
  uses stasd to port 2003 on log. 
  see frozone.test.verify_graphite.py to test - otherwise every time you save it will log onto graphite.

:Logging: 

  via rsyslog to log.frozone.mikadosoftware.com:/var/log/syslog
  tail the logs as usual.

Known bugs
----------

* error checking modulename and module uniqueness broken.
  Unlikely to rush to fix - the file only approach has the above limitations
  so likely to abandon.

