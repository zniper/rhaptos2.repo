Weekly reports
==============

This is an area for my evaluation of the week just gone.

I hope it will reflect honestly the value you guys are getting.  Of course, Ed's report may look quite different ! :-)


Week 3 April 16-20
------------------

Of the three things I aimed at - deployments, tests and logging only
deployments really worked.  We now use the / an industry standard
deployment tool (fabric) and have a (well) tested virtual server
environment

I have got a fabric deploy for rolloing out Linux COntainers - I did
have 100 virtual servers installed on my box and it took it quite well
as a test.

But that means we have the space and flexibility to design and develop
the same architecture at every stage of the development process,
increasing our confidence that when we go for QA or go live, things
will work.


Next week : 

* smoother deployments with Jenkins CI
* some tests for Jenkins to run
* logging. 


Week 2 April 9 -13
------------------

Infrastructure, Infrastructure, Infrastructure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The weeks intention was to build out basic infrastructure - and to do
this by creating a end-to-end demo that took a piece of text from
JQuery / TinyMCE and pushed it out to servers running REST api.  That
way we do the nice Scrum thing of technical stories that deliver a
small sliver of customer functionality.

We are there in the letter of the law if not the spirit.  A number of
things such as nginx configuration problems, silly bugs that took a
while to hunt down, all just ate up dev time.  This is I think common
in the first 'surface the product' parts - and despite it being
frustrating (and obviously invisible to anyone in Texas) progress is
made and I can see real value in this.

What have we got?

Well we have working Editor-> JQuery -> REST server
-> REST repo chain, that is more or less installable from scripts, and
using fairly sane choices of frameworks.

Its not quite there - I cannot pull the text out of TinyMCE via
JQuery, the server->repo hop just seems unnecessary (there is a design
discussion here), and the install script is just that (it does not
cover the nginx server etc).

Overall - B+.  Would have expected to be further along, but going in
right direction.



Next week
---------

I propose the following:

We are still at building basic infrastructure level.  Get this right early will pay us back manyfold in the weeks to come.

* Better deployments - I would like to see this either on GAE or on my own US server simply so you can see some action.  Plus the poormansfabfile shell script joke will only last a couple more days.

* Tests - I want to have one test suite covering the 4 main end points, and they will be radically different test frameworks.  More infrastructure.

* Logging - the logging from Flask / uWSGI and in JQuery is poor and needs to be top notch


