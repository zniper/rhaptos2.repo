==================================================
Discussion on data structure behind repositor(ies)
==================================================

I hope this is a short discussion on the issues raised recently.


The basic probelm
-----------------

We want to agree how to structure a repository, its storage strategy
and the basic unit(s) of what will be stored.  This model repository
will store "fragments" - chunks of HTML written by the user, a set of
fragments in a specific order are called a *binder*.  When arranged in
the order in the binder, the fragments will form a complete *end-document*
which can be viewed as HTML, or converted to PDF etc etc.

I have proposed we create a single flat namespace for all documents and resources
stored in (any) Connexions- Other- Repo, and navigae through it using Collections
that are versioned via md5 hashes.  It should be noted that I think the main issues
that were of concern to people are solvable (I think they are the branch-merge issue
and the definition of latest) - but I think that we should not try this now - scale back
focus on the simpler solution - google docs for a single server.



So stop talking and show an example::

   org.cnx.frag:d3911c28-2a9e-4153-9546-f71d83e41126/e5df9b39e5b428a84341c100bfe260df
   ^^^                        ^^^^                    ^^^^
   name of namespace          UUID in that namespace  md5 hash of current content

   here we use org.cnx.frag as the namespace for a fragment.

Or::

   org.cnx.frag:e5df9b39e5b428a84341c100bfe260df
   ^^^                   ^^^^
   name of namespace     md5 hash of current content



The short version of the long one I just threwaway:

0. I think the concerns are 

   * what if two people in two repos work on the same document at the same time?  
     Which is latest? 

   * What about "derive".

   * surely we can track all this?


1. "Latest" : I *think* this is an attempt to allow me to follow
   someone else's chapter in my binder (Professor X is writing a
   history of europe, I am writing book on Roman Emperors, I use his
   chapter on Nero.)  I want to change his chapter, and I also want to
   get his updates.  How do we handle this - well, if i want to make
   changes I MUST derive.  That is there are now two documents.  So I
   can have his chapter on Nero, but i can never get his updates
   unless I never make changes.

2. Having external editors (outside of Connexions) be able to send
   chapters in is the same as having two repos - that is we will
   encounter a valid branched document at some point.  Our solutions
   to Latest was to derive *before* changes were made.  So the derived
   approach wont work here.  With two editors, or two repos, or
   offline editing and uploading as a zip etc ...  we have two valid
   documents, both from the same original doc, both holding valid
   changes.  and both with the same "name".  What do we do?


Solutions : we need to solve branch-and-merge - that is offer a
convincing solution, or prevent it happening.  I suggest the latter.

* Option 1 - wrap git-serve.
* Option 2 - a combination of UUIDs and binders / history
* Option 3 - extend the derive approach back to the new repo


Option 1 - we follow the growing DVCS trend and basically turn our
           "namespace" into one big git namespace, and each repo, or
           each workspace becomes its own git repo.  Its not bad but
           the common case is likely to be I just write my book and
           dont pull in chapters from others.  This is not as simple
           as you want in git.

Option 2 - Distributed GoogleDocs style approach.  Label each file
           with a UUID.  This instantly enables external editors,
           avoids reliance on central server(s) and the benefits of
           decoupling.  But it does not solve branch-and-merge.  To do
           that we need to version files - without central servers,
           that means hashing the content.  So we *could* do that -
           binders to represent the order, uuid/hash for each
           fragment.  Its quite a nice solution.

           But it does not really solve branch-and-merge - Latest has
           no sensible meaning

Option 3 - Single Server GoogleDocs - Label each file with UUID, version it
           how you like.  But if you want to make a change you are either 
           in a race condition with anyone else with permissions or you are
           "deriving" - and we dont do any merging or branching.


Option 4 - Distributed Single server - basically lock files before editing.  
           urgh. Across servers. urgh,urgh.


Summary
=======


Simplest solution - Option 3.


Really simple Implementation - Still use UUIDs. Versioning is
                 irrelevant and does not need to be supported except
                 for freezing.  The namespace does not need to be
                 flat - we just store files in folders, which means
                 the module m3090 is actually stored under
                 collection400 Therefore versioning is not needed to
                 avoid naming collisions and Latest is always True.
                 A collection is a file strucutre - I suspect this
                 is what Phil meant with Zips.


Conclusion
----------

I think Google Docs is offering an enticing solution - and they are not trying to 
solve branch and merge either (afaik).  So we should not either, as it is a small
use case for now.

The filesystem based implementation does have the virtue of extreme simplicity.
And I have already implemented it!


.. [#] Dont ask - its pretty horrible.
