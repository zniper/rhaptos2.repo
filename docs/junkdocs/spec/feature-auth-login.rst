========================
Authentication and Login
========================

Ideally we want to securely authenticate users, but not handle
passwords ourselves, and yet still store details of users that most
other institutions would not want to.

We *could* outsource to a commercial company like JanRain.  However
this puts a great deal of trust in thier infrastrucutre and continued
existence.

Instead we shall act as a OpenID relying party for major Providers
(like Google, Facebook etc) and then map the OpenID provided to an
internally held UserID, and so a set of user details.


SUmmary:

We shall rely on a OpenID coming back verified, and map one or more OpenIDs to a 
UUID (UserID).  The UserID will be the key to retrieve :doc:`user-detail`. 




Use Cases
=========


1. Known User, known OpenID Login

2. Unknown User, Unknown OpenID Login (First time login)

3. Known User updates details

4. known user logs in with unknown openID

Also
====

See :doc:`/openid`
