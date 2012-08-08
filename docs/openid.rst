=========================================
Searching for an OpenID Provider (Server)
=========================================

Summary
=======

I looked at a lot of Python and non-python servers.  There is no
drop-in, well supported server out there, giving us two less desirable
choices - either take on the support burden ourselves, or change our
business rules to do away with the problem.

We also need to discuss a means of maintaining an internal user id.

Background
==========

OpenID 'clients' (that run on your website and talk to Google) are
widespread and well supported.  However, the 'server' (that runs on
Google) are less common, less well supported and seem to be a
vanishing breed.

CNX.org has approx 10,000 existing client accounts, and intends to
release the new system using OpenID as the sole logon method.  For new
users, this should be simple, they will use their Gmail OpenID (or
create one).  For existing users, they either need a means to match
their old account to their new Gmail ID, or they will just want to 
keep using their old username and password.

We assumed 

1. That existing users would not have existing OpenIDs
2. That existing users would be unwilling to create a new third party OID 
3. So, we would run a provider just for them, that uses the existing username/password
   and they would essentially see no difference in login.

We also assumed

1. OpenID / OAuth would give us ability to store User details meaningfully.
2. We would not need a seperate user datastore


To this end we looked at finding a OpenID Provider that we could run
and maintain independantly.  THis gave us several criteria


1. Code base must be well supported or well within our expertise range
   to self-support
2. No / minimal development before use (ie we are looking for config
   and go)
3. No/ minimal ongoing costs to support


Initially I limited to looking at Python based servers 


JanRain 
-------
http://janrain.com/openid-enabled/

JanRain is the grand-daddy of Python OpenID support, contributed to
the 2.0 spec etc.  They are a commercial company offering hosted
OpenID / OAuth "solutions", but advertising by providing F/OSS libraries
to Ruby, Python and PHP worlds.

Their libraries are wrapped by all the other Python Providers that I
can find.

Their server.py example, I was unable to get working, despite
extensive monkey-patching, however I did write a simple Flask wrapper
around their library for a minimal implementation.  I would estimate
at least a weeks development to get to something test ready, and that
would be aiming at a cut down feature set.  

Django-OpenID 
-------------

(http://trac.nicolast.be/djangoid)

This is now several years without commits, and needed patches to be
written to get it to run, and still I was unable to make a simple
login work.  I decided this is best classed as abandon-ware.

ownOpenidserver
---------------

http://ownopenidserver.com/

This is one I only recently found, it works but is aimed at just
verifying one person and would need development to back onto say a
MySQL db.  It wraps JanRain in web.py, very similarly to the toy
example I wrote.


I also looked at a few mini projects in Python dotted around, but
nothing useful turned up.

I then looked around at non-python implementations, 

Overview of the market
----------------------

From http://openid.net/developers/libraries/ I obtained a list of
libraries / implementations that claim to offer Provder capabilites.
Please note that since our provider is intended *only* to authenticate
users for our own Replying Party (Consumer) (ie we own both ends of
client server) it really does not matter if the Provider only does
OpenID1, 1.1, 2.0 etc.



=================== =====================================================================
Name                Notes
=================== =====================================================================
DotNetOpenAuth      Windows Only, but now shipping as F/OSS 
                    as part of Visual Studio, so likely longevity.  
                    This is one I have not tested (it will add dramatically to TCO)
                    but if we really cannot take option 1, we should review this
                    before plumping for less well supported options on Unix.

JOID                JOID server example and tomcat 
                    did not play nicley, stopped debugging after an hour

OpenID4Java         Plays a similar role to JanRain in the Java world - almost all
                    Providers wrap this library.  Did not attempt to wrap it 
                    myself as JanRain seemed sufficient in Python

WS02 Identity Svr.  A wrapper around OpenID4Java, and supposedly a
                    one-stop binary install. Most attractive well
                    supported option, (commercial company, eBay use
                    their ESB server), but it took majority of a
                    working day to get up, https still an issue and
                    simply too heavyweight for our needs.

NetMesh InfoGrid    (Cursory) - Is a Graphing database framework that also for 
                    some reason supports OpenID. 
                    Not clear how central OID is to the main development goals

Atlassian Crowd     Not Tested.  Not OSS, in a similar position to DotNetAuth.

Packetizer          A Perl based openID implementation that actually installed 
                    and worked. Also it is MySQL backed so can easily handle 
                    volume we have.  It does not wrap a library but just printf 
                    formats messages, including yadis.  I quite like it :-)
                    Fails on the strong support community criteria however.

OpenID4Perl         Library in similar vein to Java.  Not Tested as have working 
                    Perl solution.

Net::OpenID::Server Not Tested

PHP OpenID Library  JanRain again

Zend                Written by Zend (?) - is a library and examples, but as we
                    have this style of solution in Python is not tested.

GAE Django          Seems primarily abandonware - wraps JanRain again, but not  
                    working on GAE when tested.

Ruby OpenID         JanRain again
=================== =====================================================================



Testing
-------
Testing was fairly limited - there is no common automated test suite for openID
and this was really a quick review (I had hoped!)

Does it actually return a OpenID to formatted requests

Then used relevant portions of OSIS (test-id.org) if successful and on rackspace.


Conclusion
==========

The preponderance of Google, Twitter et al supplying almost all the
OpenID Providers in the world has changed the OSS landscape from
2007/8 when most of the above projects began.

Most sites want 'client' access to authenticate users, but few want to
run their own server so there are fewer scratches to itch.  A minimal
implementation is feasible to develop or just plug-in, but production
level support will be up to us and with no real community.

We have three basic options, in ascending order of effort


1. Force all users to login in with 3rd party OpenIDs exclusively.
   (Will need to link old accounts with new IDs)

2. Implement Packetizer Provider, and accept the cost of support (Perl, unknown bugs)

3. Develop our own Python based Provider, and accept the cost of support


We are very unlikely to be able to have a OpenID implementation that
can manipulate the Ax fields to supply non standard info back - in
other words it is likely to be simpler to write our own REST client
that queries for the details of a given OID than develop, run and
support a Provider that does so.

As such we are looking at having a (simple) user-info database fronted
by REST and presumably a memcache instance on each repo server for
speed.

We are likely to want to support one UserID mapping to >1 OpenID so
people can link accounts and login as they want (StackOverflow model).
This may not be immediately necessary but is likely to be a trivial
first requirement for User Datastore


