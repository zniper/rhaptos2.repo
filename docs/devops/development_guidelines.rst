Dev guidelines
==============

OK, this is a sort of a style guide, sort of a how to and mostly a
justification and set of excuses.


My local setup
==============

This is a discussion of the architecture and setup we / I am using

We have two distinct locations to worry about.  The local (i.e. in my
office) setup, and the shared, ie public, setup. THe first is mostly
hosted on a single dedicated server in the corner of my office.  This
is the developer-local server.  The other is at the moment hosted on
rented rackspace virtual servers hosted physically 'somewhere in North
London'.

How to create the repo locally :

1. localhost only

   This is intended as a simple, try-me, setup.
   run 






config
------

There is one server wide configuraiton file stored in /usr/local/etc/rhaptos2/frozone.ini.  The settings here can be overridden using Environment variables - except that only settings beginning "rhaptos2_" will be taken.

so rhaptos2_current_version is set in frozone.ini and can be overrrideen

It is unclear how this interacts with virtualenvs

Github
------

Several years ago, hosting your own source code, bug tracker, issue
tracker and code review tool was the only game in town.

Now, especially for Open Source projects, other people are quite
capable of doing it for us.  They call it XXX As A Service.

I expect we shall gain a lot from just outsourcing some of our basic
sysadmin plumbing, and the risk?  Well, there is minimal risk - if
github turns around tomorrow and starts charging 100 USD per commit,
we can walk away, setup our own shared repo, and parseing commit
messages for [BUGID=1234] is well with our own capabilities.

So, I suggest we use github for frozone SCM, bug and issues, and code
reviews.  If it does not work lets find another solution, but try it
out in anger for at least two sprints.


Repositostories
---------------

1. Fork the main repo (for now this is https://github.com/lifeisstillgood/frozone, please can an admin fork 
that onto connexions.github and we can use that ?)



Basic workflow for a Frozone developer.
---------------------------------------

0. We shall use the now 'github-flow' approach.  This is from the git
   pro author and git hub founder Scott Chachon, and is fairly sane
   and easy to follow.  Basically, Master is always tested, reviewed
   and deployable.  Have a change to make?  branch off master,
   develop, test.  THen do a pull request from your banch to master.
   SOmeone reviews that pull request.  If its ok, merge into master.
   Repeat.
  

1. Create an Issue in github based on the story card in Trello
   I have created #4-stagingstep_needs_optparse.

2. Accept that issue, and create a feature branch based on the issue::


    git pull origin master

    git branch \#4-stagingstep_needs_optparse
 
    git checkout \#4-stagingstep_needs_optparse


3. do the development work we want...


4. commit the changes, back to git hub::

    git add ...
    git commit -m 'ready for review' 

    Yes, it is a good idea to put some sort of catch in github, a post commit hook, at stage 4, 
    A service called reviewth.is exists.  however yet another dependancy.

5. initiate a pull request from branch \#4-stagingstep_needs_optparse TO master

   ::

    Look at https://github.com/lifeisstillgood/frozone/pull/5



6. Someone reviews the pull request, and a discussion ensures on github

   ::

    Look at https://github.com/lifeisstillgood/frozone/pull/5



7. When the changes are approved, merge into master.  THat can now go live.

   ::

    Look at https://github.com/lifeisstillgood/frozone/pull/5



Line Length
-----------

This hoary old chesnut.  There are many discussions about this,
and I will just stick to the two that I think are the most relevant

1. For programmers working on one project, they should all stick to
   one set of style guidelines.  It does not matter if some folks
   think the guidelines are wrong, just that the style is *sane and
   the same*.  Using CamelCaseWhenReallyUnderlinesAreWhatGodIntended
   is fine as long as *everyone* in the project will use camelcase and
   not get involved in games of formatting tennis.

2. Typographers, who have had about 500 years to get it right, stick
   to 10-15 words per page/column (today's Times front page has 12
   words average on the first paragraph.)  The human eye tends to
   strain moving much further, so 12 words, 6 characters per word plus
   space gives 72 characters or so.  80 is entirely arbitrary but in
   the right area.  Me, I use 73 cos it's the best balance on my
   laptop.  YMMV

So, lets stick to ::

 PEP-8
 74 characters






Architecture
============

1. We shall use the Bezos SOA `approach
   <https://plus.google.com/110981030061712822816/posts/AaygmbzVeRq>`_ -
   nothing, absolutely nothing communicates with anything else except
   through defined agreed service APIs - basically, use http.

1.a. This has an implication for testing.  The first division in tests
  is not unit vs functional, but internal to the 'service' and
  external.  Internal tests are allowed to know something about the
  inner workings, allowed to go peak at the disk to see if the file
  actually got written.  External ones, no.  Just use the API and test
  what comes back.. Test it hard. Throw horrible edge cases, drop
  connections.  But no peaking.

2. document what is there, what has been done.  Not document what you hope to do - unlesss you label it bluesky.



Misc.
=====

THis is stuff I don't have a useful place for.

pip and Interpreter shutdown. 
-----------------------------

Fabric uses paramiko to do its ssh connection setup.  If you use pip install you will occassionally see 
::

  Exception in thread Thread-1 (most likely raised during interpreter shutdown):
  Traceback (most recent call last):
    File "/usr/lib/python2.7/threading.py", line 551, in __bootstrap_inner
    File "/usr/local/lib/python2.7/dist-packages/ssh/transport.py", line 1602, in run
  <type 'exceptions.AttributeError'>: 'NoneType' object has no attribute 'error'


This is because we have not close()d the ssh connection before the main() thread exits - which 
is the main thread on remote, presumably kept open by pip.

My workaround - stick a useless last sudo("ls") in after pip command and things shutdfown gracefully.
see: https://github.com/paramiko/paramiko/issues/17 for someone trying to fix it properly.


Biblio
------

http://headrush.typepad.com/creating_passionate_users/2006/03/code_like_a_gir.html
  Purely for the 'Wrap at 80 chars - thats Girrrrl code.  No that's "Metrosexual Programming"'
