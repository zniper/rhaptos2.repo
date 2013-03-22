============================
Difficult issues discussions
============================

I want to touch on some areas that are a little opaque to me right now.




OpenID
======

see :doc:`/openid`

User Data store
===============

see :doc:`user-detail-store`


Security Model
==============

Worth reviewing - seems weak.


Sections vs Modules
===================

How granualr do we want the individual sections to be?


Storage format for a section
============================

I am currently looking at using JSON modules as they are easily transportable between Javascript and Python.  However we are likely to want to mix microformats, HTML5 and other
things for various reasons.
How best do we do that - or shall we just stick to JSON as its simpler.


Transition from Unpub to Pub
============================

This is the recent discussion with Phil - I am unclear of the parameters here and think more discussion is needed.


Automating testing adn deployment
=================================

Jenkins, and rackspace


Aloha collaborative editing
===========================


Running the collab server might be an extra effort - should this be best efforts only.


Versioning
==========

Same old discussion - do we create a section and give it a unique ID (UUID) 
for its whole "life".  Just do some form of versioning.  Or do we go git style and have uuid for each change? 

With life-long numbering a couple of questions arise:

1. who is the life time decided?  Presumably when a user deletes the section.
2. derivation of works - we allow someone to copy a section, put it in their end.  Then to   change it.  OK.  What about copyright here? What about attribution?

I suggest we combine 

* all versions have authors 
* Each new version (PUT) is archived (best effort) and stored with sha1hash.
  THe sha1hash is then also stored with the authors of *just that change*


That the editor prominently suggests who the author is and who is
actually typing things up.  And who is copyright holder. Across all
changed / changing docs.



Federation
==========

This ties in strongly with the unpub -> pub transition. 
How do we properly maintain and manage documents when we could concievably 
have one HTML doc with one section written on www.cnx.org and the next section
written on www.mit.edu and there are *no* changes so no need to copy / derive / etc.

Should we have unique ids for each section and each version of that section.
If we do, then ID:version is useless becasue it requiores co-0ordination between
mit.edu and cnx.org to ensure id:1 and id:2 are in order.

We tend back to sha1 hashes.  

So can a collection be built up of fragments from around the globe?
And if they are, does it matter at all that we know where the originating fragemnt came from - I mean UUID 12345-12345-12345 is globally unique, adding mit.edu:12345 seems both redundant and having little benefit (how do we know if rhaptos.mit.edu will stay up?  What if its laptop.professorSmith.mit.edu)




The transofmration services 
===========================

We shall ignore entirely cnxml - html issues - all data stored by the
new system will consist of HTML5.  If necessary we shall convert en
mass all current documents, and reconvert to CNXML for printing only
at publish repo.  unpub is HTML5 only.


UUIDs
=====


1. UUIDs are unique. Really.  /dev/random in Ubuntu and FreeBSD is
   sufficiently high in entropy these days that the asteroid will hit
   throwing up sufficient dust to offset global warming long before
   our app finds a UUID collision.



Document stores not RDBMSes
===========================

1. documents are really really easy to stub out.
2. we are mostly passing around not atomic bits of data but 
  documents (ie a tree of chapters, a list of user info)
  Storing those in SQL correctly is breaking a doc out into fields, and
  reassembling them.
  I have spent 15 years adovazting SQL backed systems.  It takes a lot to risk 
  document stores.
3. Really it does not matter - the interfaces are using documents,
  so maybe we swap them out one day.



Outline of spans of interaction
===============================

Bascially sensibly documenting interfaces and contracts.  Untill we start using Eiffel
I guess its read the docs.
