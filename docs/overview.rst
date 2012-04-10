==================
Rhaptos-Editor-2.0
==================

:author: pbrian <paul@mikadosoftware.com>
:Week: Apr 9-13

DRAFT DISCUSSION 
================

Introduction
------------

I have been asked to provide a working, documented and tested
implementation of what I am calling Edna Mode. [#]_ It is intended to
encompass all the requirements set out in CNX Rewrite Requirements
<https://docs.google.com/a/mikadosoftware.com/spreadsheet/ccc?key=0ArvuSYeGW6GpdHJmNVJVWjBWOGVGM0RmMWJqdDRpeWc#gid=0>


I beleive that the essence of this project is to take weekly sprints,
and deliver a well documented and tested chunk of work each week,
whilst constantly looking for feedback and trying to fit it back into
the legacy system(s).


Overview
--------


.. figure :: rhaptos.jpg




* editor.client

  Runs TinyMCE, transmits back to editor.server.
  I think that I shall see this as a POST - that is we never update a module?  This will be hard without a clear history tied in.  Look to the git model.  
  Other capabilities of Client - not too much - most features seem best handled off on server.



* editor.server

  Flask behind uwsgi behind nginx.  Seems robust but not overly heavy.
  REST API - POST -> create a hash, store it in repo.  The new URL is the hash....
  

* editor.repository

  For now nothing clever - get a POST, create a store.  provide GET access to that URL.  Here I would create the linkages for version chaining.  Actually i cant.  Who knows which one is created after the next?  That needs to be said by the client.

* rhaptos.transmogrifier

  Really good example of queueing and asynch using REST.
  provide URL of pdf - but GET will fail till it is actually there - polling responsiblity is on the client.  



* testing.user

  Selenium RC tests.

  One so far :-)



Discussions
===========

There are a lot of unknowns (or known unknowns?) in this document.  As the design meetings progress, I am sure these will flesh out (I see this as a scaffolding document that will evolve over time).  However some areas for discussion are already obvious, and whilst i expect that much of this is old hat or already under discussion, I note it all here for my memory as much as anything else.


CNXML
-----



Authentication
--------------

For a distributed, service orientated system that we intend to create, 
a Kerberos-like authentication mechanism is correct.  However kerberos
has a high administrative overhead and requires a lot of per user initial setup (confirming they are who they say they re through some intermediate mechanism)

* Authentication, Authorisation and Accounting


There are two basic ways around this. OpenID and OAuth.

OpenID solves the problem of establishing identity - a truted thrid party with whom the user alrady has a relationship confirms to us that the user is who they claim.  This still leaves us with the problem of distributing this as a ticket.

OAuth provides google as the ticket granting service, for which other google services are the kerberos clients.
We can (for now?) simply rely on google as our Kerberos provider, assuming we want no Access control discrimination [#]_  I intend to create a simple OAuth service, users authenticate against that and I shall use the google provided ticket to pass around as the real ticket. Each service will then take the ticket and try to access back to google.
A success will validate that user, and so we have a working kerberos implementation with almost no infrastructure overhead, and can move forward knowing we are baking in security at a deep level and can replace it with fair amount of ease.  

I intend to use Google as the Ticket Granting Service for now.::

    Client ID:  
    494015227541.apps.googleusercontent.com
    Email address:	
    494015227541@developer.gserviceaccount.com
    Client secret:	
    Z92eQ8VrUAVYmJ_tAb7Ka3bM
    Redirect URIs:	http://cnx.mikadosoftware.com/oauth2callback
    JavaScript origins:	http://cnx.mikadosoftware.com



References
----------

.. [rewrite_requirements] https://docs.google.com/spreadsheet/ccc?key=0ArvuSYeGW6GpdHJmNVJVWjBWOGVGM0RmMWJqdDRpeWc#gid=0







.. [#]  If Debian can name releases after Toy Story characters, then I can name projects for other Pixar films.  It can be changed for clarity :-)

.. [#]  Actually we could use some form of ACL - by mapping different google API services to different levels of our own service, (ie publishing requires google+ access, editing requires google contacts access).  Frankly that seems a bit too ball and twine.

