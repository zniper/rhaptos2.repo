
======================
Chapter 4 - A new hope
======================

Following our discussion just now, a few comments and thoughts have
come into focus in my little grey cells.  Ross mentioned reasons why
connexions has survived, , with Kathi and Michael talking about
federation and other editors and Phil trying to explain to my brain
why the zip file is a good.  Anyway this may be obvious to others but
it's taken me a while !

For a decade CNX has been doing something right, and this is not the time 
to go off doing what everyone else has been trying and failing with.
As Ross pointed out it seems to be permanance and reusability that
keeps folks coming back.

So, we want our solution to do the following (I think)


* Versioning of files (permanance)
* Modules are seperately linkable (anyone can reuse your chapter)
* Follow a certain file (get latest)
* Allow friendly names vs UUIDs 
* Allow federation - we will not be the only Connexions repo.
* Allowing other editors to be used (online, offline, combination)



Idea
====

We (I) are focused very much on the editor, and although Ed is trying hard to get
us to look at the protocol we still come back.  But Ed is right.

The thing that counts is the *collection*, not the modules.

If people gave us a collection document that 

  * linked to files on our repo
  * in order
  * with notes on what was changed since the last collection was sent
  
Then we could update / maintain our repo, even if they edited on a different server, or in Dreamweaver, or notepad.  All we would want is a set of files,
and their assurance that the collection was right as far as they knew

So, lets write a bunch of Javascript that does that

First time user:
----------------

* Fire up authtool.js, by clicking link on cnx.org
* Start a new book, there in the browser.
* You are given a blank collection doc - with a UUID
* Ask "where are the files you want to turn into a connexions book?"
* User loads the first chapter into your browser.
* Javascript grabs the contents of that tab and sends it to cnx.org
* we update the Table of contents (collection doc)
* repeat

Existing user
-------------

* fire up authtool.js, by clicking link on cnx.org
* choose the book to work on
* load up the file you want to add into a tab
* tell us if it used to be one of the chapters in the current collection (even see a diff)
* We save it as above


Mapping friendly names / UUIDs
------------------------------

* we *must* do this now - but it is pretty simple.  
* The collection keeps a list of friendly names to UUIDs
* we map at the webserver level. That is we do not need to change the links in
  html - you click on "chapter1.html" and ... errr... maybe.


We *must* because the editing of files is now *outside* our protocol.
We are going to still provide best of breed editing on site - its just that 
anyone with any editor should be able to easily upload - Phil is right here.
I just think we can make them do *less* work on the client end.


CHange propogation
------------------

Since we (optionally) know that file XXX used to be file YYY (you told us on upload)
we can reasonably tell anyone who wants the latest of file YYY to now look at file XXX.

Since latest of a file is a very mutable concept, this is probably the best we can do.
(As an example, Ross writes a module about Emperor Nero and Rome burning.  I link to it and hit "follow latest" to get his updates.  Then Ross changes the chapter to be about 
Nero burning Christians, and moves his ROme burning notes to the "Marble" chapter.  It is still the chapter Ross, wrote, it is still the latest version.  But it is not what I want to follow.  C'est la vie.  Can't have everything)


Publication step
----------------

* because each file is a snapshot we can set permissions.  So the
  *same repo* can store unpublished files only one person can see /
  edit and store publicaly available files (Or at least they can be in
  same namespace if not in same filesystem for Ops reasons)

* Because you are publishing a snapshot of files, as linked to by a collection
  then 



Implementation
--------------

You want to store something on Connexions - we give you a UUID for a *collection*.


Please note that this approach, whilst based on us doing clever
Javascript, is entiurely outsourceable - as long as you follow simple
guidelines, any one can wirte code that immedaitely prepares stuff to
be published.



Possible issues:

* file access - we dont I think need it - we are reading form the tabs.



