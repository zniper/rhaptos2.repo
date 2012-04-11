
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

  http://cnx.org/<user>/<workspace>/collection

  http://cnx.org/<user>/<workspace>/module

Note that it is assumed the user will only ever reach their modules
(editing area) from a user/workspace path.  We do not have to store it
like this (its probably good not to) but we will have to enforce this
partly for security but also cos this is the paradigm we are telling
people exists.  (Ie you a user have a set of workspaces and in those
are modules.  The ability to copy across is kind of ignored)

* /collections/

  GET
    Returns list of collections-hashids and URLS in Link header
  POST
    Expects a linked list of existing module hashes, plus meta data.  Creates a new collection and returns the URL
  DELETE
    N/A - return 404?
  PUT
    expects a *complete* list of existing collection-hash-ids, and will update the collections server accordingly (adding or deleting or moving).  

* /user/workspace/collections/<hashid>
  
  GET
     Will return the linked list of module-ids and any assoc meta data as JSON
  POST
     N/A
  PUT 
     Given linked list of module-ids it will update them.  ie this can do move of modules, delete of 1+ modules, or complete resetting.
  DELETE
     removes this collection from the users workspace.  Does not destructively affect the collection.  (Not sure how we do do that)


* /user/workspace/modules

  GET
    return list of all modules in workspace (this seems ridiculous)
  POST
    Create a new empty module, and its unique URL
  PUT
    N/A ???
  DELETE
    N/A - must be a modules list


* /user/workspace/modules/name

  GET
    returns the *version history*, plus branching?? Or returns the HEAD/tip?
  POST
    Create a new module version and store it based on payload.
  PUT 
    N/A
  DELETE
    Deelte the whole history and storage

* /user/workspace/modules/name/versionhash
  
   GET
     returns the HTML5
   POST
     N/A
   PUT 
     changes the stored version ???  Should we ever do this?
   DELETE
     Not sure we ever want to do this either.


* /pbrian/mybook/

  or /user/pbrian/workspace/mybook

  GET
    returns the collections, lenses and modules in workspace
  POST
    NA
  PUT
    NA
  DELETE
    NA
 
   I think most of this is covered in the areas underneath - no?


* /users/pbrian/

  GET
    list of workspaces
  POST
    create a new user.   How do we tie this into OpenID is still big question
  PUT
    TBC
  DELETE       
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
