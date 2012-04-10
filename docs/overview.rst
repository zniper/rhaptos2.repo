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
encompass all the requirements set out in `CNX Rewrite Requirements
<https://docs.google.com/spreadsheet/ccc?key=0ArvuSYeGW6GpdHJmNVJVWjBWOGVGM0RmMWJqdDRpeWc#gid=0>`_


I beleive that the essence of this project is to take weekly sprints,
and deliver a well documented and tested chunk of work each week,
whilst constantly looking for feedback and trying to fit it back into
the legacy system(s).


Overview
--------


.. figure :: rhaptos.jpg



* editor.client

  Runs TinyMCE, transmits HTML5 back to editor.server.

  This is purely sending dummy data for now.  I do not think tinymce
  is yet setup for HTML5 and there are many ongoing disucssions with
  other providers.  The EIP editor is likely ot be a third party
  affair even if we require collection and workspace editing
  (presumably that will be in our own JQuery)
 

  :Question: I would like to POST module changes to the server.  That is
  any change to a module is an entirley new copy, stored ala git/hg
  This has many issues but I think is best approach. (Discuss issues)



* editor.server

  Flask behind uwsgi behind nginx.  Seems robust but not overly heavy.
  REST API - POST -> create a hash, store it in repo.  The new URL is
  the hash....

  :Question: I would like to discuss treating each module change as a
  seperate hashable object.  Its a fairly good idea, but has some
  implications that need to be thought through.  However its almost
  perfect to decouple services with.


  

* editor.repository

  For now nothing clever - get a POST, create a store.  provide GET
  access to that URL.  Have same delayed / polling requirements for storage 
  as transformation.

  As an close but seperate service from the editor.server.


* rhaptos.transmogrifier

  Really good example of queueing and asynch using REST.  Provide URL
  of pdf - but GET will fail till it is actually there - polling
  responsiblity is on the client.

  Using dummy data - quite likely I will not get this far this week.


* testing.user

  Selenium RC tests.  I am behind on the curve here - I am clearly
  unable to get selenium to work with TinyMCE - any pointers please?





CNXML
-----

My biggest concern (and there are a few) is hidden gotchas in the
semantics or the processing instructions.  Or anywhere for that
matter.


Authentication
--------------



For a distributed, service orientated system that we intend to create,
a Kerberos-like authentication mechanism is correct.  However kerberos
has a high administrative overhead and requires a lot of per user
initial setup (confirming they are who they say they re through some
intermediate mechanism)

So we slip back towards the less secure but more common OpenID / OAuth

This section was longer, but it seemed less useful than a series of questions

1. What level of security are we worried about here.  Can we quantify
loss?  is OpenID/OAuth OK?

2. if we use OpenID and get everyone to sign in through google, we
   will still need a centralised service to map openid -> Access
   control and workspace in Rhaptos.

3. That implies (for no shared backend) a ticket granting service.
   OAuth? Kerberos? To my mind there is not a simple easy packaged
   solution here.  OpenID assumes a consistent shared auth backend,
   kerberos assumes we know the person before they sign on.  Am I
   massively out of date here?




..    I intend to use Google as the Ticket Granting Service for now.::

..    Client ID:  
    494015227541.apps.googleusercontent.com
    Email address:	
    494015227541@developer.gserviceaccount.com
    Client secret:	
    Z92eQ8VrUAVYmJ_tAb7Ka3bM
    Redirect URIs:	http://cnx.mikadosoftware.com/oauth2callback
    JavaScript origins:	http://cnx.mikadosoftware.com



.. [#]  If Debian can name releases after Toy Story characters, then I can name projects for other Pixar films.  It can be changed for clarity :-)
