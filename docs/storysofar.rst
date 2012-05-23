============
Story So Far
============


Use this page to discover recent changes
========================================

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

