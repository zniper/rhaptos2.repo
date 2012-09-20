=======
Jenkins
=======


sudo rm /usr/local/man

General considerations
======================

The first and for me primary consideration is I as a developer
want to be able to run locally, the same build that jenkins will 
run remotely.

Yes, annonying aren't I.

So the build scripts need to be flexible.

Secondly, Jenkins is not perfect, and it rather assumes you are not,
well, doing the first thing above.






Installing jenkins is pretty simple::

  make jenkins host=devjenkins fabfile=deploy/fab_sys_jenkins.py

This will apt-get the latest package and install on devjenkins(.office.mikadosoftare.com)

Then we have a series of *manual* installation steps, which may be automatable but I 
have not been successful doing so and see little need as this will be a long running server.


Configuration
=============

Security
--------

Crerate people in system, turn on security.  Note you create a person in matrix,m then they logon.

ENable security, ensure ANonymous only has Read access (Overasll) and your username has the lot.
 


Supporting stuff
----------------

FIX: Need /etc/rhaptos2.ini installed.. migrate to all ENV setup.



Install plugins
---------------

We want to install git/github plugins.
Goto the top left corner, [Manage Jenkins] and then [Manage Plugins], click the Available tab, and search for::

   git
   github 

   Violations
   Cobertura

plugins, tick their install boxes and apply.

NB - 1.406 of Jenkins simply refuses to install Violations or Cobertura, so likely will upgrade.



ssh keys
--------

We need github ssh access. (Its for tagging back to github, and is
frankly easier cos the github plugin compains lot)

The process of getting the provate key I created and gave access to on
github is left as an exercise.  Its been pretty painful so far :-)

As jenkins user::

  git config --global user.email "jenkins@cnx.org"
  git config --global user.name "Jenkins-ci"



Create a job
============

We shall create a job that stages the repo deploy as a test.

Manual 
------

::

  git clone git@github.com:lifeisstillgood/frozone.git -b statsd-lib-work


  make stage_local host=devjenkins fabfile=deploy/fab_app_frozone.py 


Config of the job
-----------------

1. Create a new job, choose [Build a free-style software project] and name it 'test'

2. configuration::

      Branches to build */jenkins-example
      Repoistory URL: git@github.com:lifeisstillgood/frozone.git

      Local subdirectory for repo (optional): frozone 

      Skip internal tag: tick

      Wipe out workspace before build: tick

      Ignore build triggers for now

We are not triggering a build on each check-in (CI) - I want to be clearer on the destination boxes.

Frankly this is a insecure approach and there is a turn off tagging checkbox so I may rethink this one.

::

    export PYTHONPATH=`pwd`
    mydir=`pwd`/frozone; export mydir
    cd $mydir/deploy/preprocess
    python mother_of_all_conf.py
    cd $mydir
    make stage-local host=cnx5 branch=master context=$CONTEXT



parameterised builds
====================
https://wiki.jenkins-ci.org/display/JENKINS/Parameterized+Build
http://server/job/myjob/buildWithParameters?PARAMETER=Value



Future
======

1. we can consider generating branches at push time

    git push origin HEAD:refs/heads/myNewFeature

2. and we can merge on jenkins - that is git pulls down myNewFeature
   and master, merges the two, and tests it.  if it succeeds then
   (jenkins merges and pushes it back / we should push it back)

   number 2 is very useful, but needs integration into our personal workflow

3. nodes, parallel builds etc
   
   One jenkins server can control an army of nodes to complete
   different parameterised builds and run different tests, on
   different OSes, with different configurations.

   When we have sufficient tests to make this worthwhile ...


Tips
----

* Restarting is not obvious http://<jenkins>/restart

* Use the CLI - http://<jenkins>/cli
  java -jar jenkins-cli.jar -s http://cnx5:8080/ help

  Basically visit cli page, download the above jar file and run it
  locally with the above command.  Mostly used for restarting and
  safe-restart

* ubuntu puts the jenkins homedir in /var/lib/jenkins.  I am sure its
  a good :file:`man hier` idea, but frankly it confuses the heck out
  of me each time.



Chain of jobs
=============


Useful plugin - downstreambuild

Because tests often dominates the execution time, a Jenkins best
practice involves splitting test executions into different jobs,
possibly in multiple different jobs.


Branches to build
THis is part of git plugin
It is very important - if left as default (**) then 
all remote repositories and all branches in them will 
be examined for changes and built

So bob commits to brnach fix-bug1234 and alice commits to addBlueButton
then both brnaches will be built, and run and tested.

THis is probably what we want to do.

Another copy of this job could however just track master branch...

What not to do - try and create an overarching job - a master job.
DO this one step at a time.
