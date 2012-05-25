
Mapping requirements docs to Service features.
==============================================





Draft REST defintions
=====================

I expect the URL structure to be set out as below.

Resources
---------

* Modules
* Collections
* Users
* Workspaces
* (TBC)

Examples
--------
::

  http://cnx.org/<workspace>/

  http://cnx.org/<workspace>/module



Note that it is assumed the user will only ever reach their modules
(editing area) from a workspace path.  We do not have to store it
like this (its probably good not to) but we will have to enforce this
partly for security but also cos this is the paradigm we are telling
people exists.  (Ie you a user have a set of workspaces and in those
are modules.  The ability to copy across is kind of ignored)

collections
-----------

Collections are not supported (possibly not supportable) in the 
text-file only repository.  This probably will be a reason to move away 
from text-file only, taking its learnings.


/workspace/<workspaceid>
------------------------

:GET: return list of all modules in this workspace
:POST: N/A
:PUT: N/A
:DELETE: remove this workspace


workspace/<workspaceid>/modules
-------------------------------

:GET:
    returns the *version history*, plus branching?? Or returns the HEAD/tip?
:POST:
    Create a new module version and store it based on payload.
:PUT: 
    N/A
:DELETE:
    Deelte the whole history and storage

/workspace/<workspaceid>/modules/<name>
---------------------------------------
  
:GET:
     returns the HTML5 of latest version
:POST:
     N/A
:PUT: 
     changes the stored version ???  Should we ever do this?
:DELETE:
     Not sure we ever want to do this either.


/users/pbrian/
--------------
:GET:
    list of workspaces
:POST:
    create a new user.   How do we tie this into OpenID is still big question
:PUT:
    TBC
:DELETE:
    TBC





Issues
------

1. How do we (currently) deal with user A and B having the same module
in their books, then User C coming along and changing all the words to
Spanish.  Do their books get altered to have a spanish section?  If
its all versioned, how do we track the changes What if someone does
want the changes proposed?  But not everyone?  THis all sounds very
git-branch ...

2. do we see a workspace as a content addressable filesystem - ala git.
   Where is basically does not matter what or how many modules are there,
   we version and refer to the whole.
   or
   do we have a system like module/name/version
