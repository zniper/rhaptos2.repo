Dev guidelines
==============

OK, this is a sort of a style guide, sort of a how to and mostly a
justification and set of excuses.



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


Biblio
------

http://headrush.typepad.com/creating_passionate_users/2006/03/code_like_a_gir.html
  Purely for the 'Wrap at 80 chars - thats Girrrrl code.  No that's "Metrosexual Programming"'
