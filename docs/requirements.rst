
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


Currently Supported
===================


/e2repo/module/
---------------

GET
~~~

return list of all modules in this workspace

example::

    http://www.office.mikadosoftware.com/e2repo/workspace/
    returns application/json MIME type, with 

    GET /e2repo/workspace/ HTTP/1.1
    Host: www.office.mikadosoftware.com
    User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-gb,en;q=0.5
    Accept-Encoding: gzip, deflate



    HTTP/1.1 200 OK
    Server: nginx/1.0.5
    Date: Thu, 31 May 2012 13:25:45 GMT
    Content-Type: application/json
    Connection: keep-alive
    Content-Length: 123
    Access-Control-Allow-Origin: *

    ["test.1", "x.0", "test.0", "test.3", "test.5", "newmodule.1", ... ]


:Known bugs: this returns the (only) workspace in the repository.  The
             text file repo does not support multiple workspaces.  is
             a workspace a branch?
	     

POST
~~~~

Create a new module-version (each new save overwrites the previous)
accept a fromatted JSON doc, return JSON with just new name confirmed

example::

    {"modulename": "physics101",
    "txtarea":"<p>this is a document ... "
    }

    ...
  
    {"hashid":"physics101.123"}


PUT
~~~

NYI

DELETE
~~~~~~

NYI



/e2repo/module/test.0
---------------------

GET 
~~~

returns the complete JSON document stored, such as ::


    GET /e2repo/module/test.0 HTTP/1.1
    Host: www.office.mikadosoftware.com
    User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8
    Accept-Language: en-gb,en;q=0.5
    Accept-Encoding: gzip, deflate

    HTTP/1.1 200 OK
    Server: nginx/1.0.5
    Date: Thu, 31 May 2012 15:19:56 GMT
    Content-Type: text/html; charset=utf-8
    Transfer-Encoding: chunked
    Connection: keep-alive
    Access-Control-Allow-Origin: *
    Content-Encoding: gzip

    {
    "username": "xdddd",
    "modulename": "test",
    "txtarea": "

    Test first draft
    "
    } 
   

POST
~~~~

Not supported - this would allow a version to be chosen to be overwritten by the user.

PUT
~~~

As above

DELETE
~~~~~~

NYI



Proposed
========

pbrian/workspace/physics101
---------------------------



POST
~~~~

N/A
The closest will be a 'clone' function -
    POST /workspace/MyWorkSpace
    ...
    {'clonefrom': '/workspace/MyOrigWorkspace' ...}


PUT
~~~

N/A

DELETE
~~~~~~~

Remove this workspace


/pbrian/workspace/physics101/modules
------------------------------------

GET
~~~
    returns the *version history*, plus branching?? Or returns the HEAD/tip?

POST
~~~~
    Create a new module version and store it based on payload.

PUT
~~~ 
    N/A

DELETE
~~~~~~

    Deelte the whole history and storage

/pbrian/workspace/physics101/modules/Newton
-------------------------------------------

  
GET
~~~
     returns the HTML5 of latest version

POST
~~~~
    N/A

PUT
~~~
     changes the stored version ???  Should we ever do this?

DELETE
~~~~~~

     Not sure we ever want to do this either.


/workspace/<workspaceid>/modules/<name>/<version>
-------------------------------------------------
  
GET
~~~
     returns the HTML5 of specified version

POST
~~~~
     N/A the repor will control version numbering.
     
PUT
~~~ 
     changes the stored version ???  Should we ever do this?

DELETE
~~~~~~
     Not sure we ever want to do this either.


collections
-----------

cnx.org/pbrian/col/

GET
~~~
   List of all collections for this user

POST
~~~~
  
   Create a New collection, empty, and return its URL, a randomly generated 
   name.  Highly unlikely we need this.

PUT
~~~

   N/A
   (see cnx.org/col/mybook)

  
pbrian/col/mybook
-----------------   

GET
~~~

  I think this should return the listing of URLS - so that the ediotor can use to 'build' the book?


POST 
~~~~

   Create a new collection of this name.
   Expect to have a JSON list of name collist holding zero or more URLS referencing valid modules i.e. [cnx.org/pbrian/module/newton, cnx.org/edw/module/electrons,...]


PUT
~~~

   must have a JSON document which contains a list of valid 
   module URLS, any order, any owner.



DELETE
~~~~~~

  Delete that collection.

.. ::


    /pbrian/
    --------



    GET
    ~~~
	list of workspaces

    POST
    ~~~~

	create a new user.   How do we tie this into OpenID is still big question

    PUT
    ~~~

	TBC

    DELETE
    ~~~~~~

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
