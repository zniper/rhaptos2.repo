=======
Jenkins
=======

JENKINS_HOME = /var/lib/jenkins

Install from fab_sys_jenkins.py
Then Goto manager plugins, install github plugin.
I need to find a way to auto install jenkins plugins

http://blog.cloudbees.com/2012/01/better-integration-between-jenkins-and.html



git://github.com/lifeisstillgood/frozone.git


#export PYTHONPATH=`pwd`
mydir=`pwd`/frozone; export mydir
cd $mydir/deploy/preprocess
python mother_of_all_conf.py
cd $mydir
virtualenv
make stage-local host=cnx5 branch=master context=$CONTEXT

Manual config
-------------

We need github ssh access. (Its for tagging back to github, and is frankly easier cos the github plugin compains lot)

SO build a jenkins sshkey - I have one already registered on github.
Its not that secure...
And then ssh git@github.com as user jenkins on the box.

As jenkins user::

  git config --global user.email "jenkins@cnx.org"
  git config --global user.name "Jenkins-ci"

COnfig of the job

Branches to build */jenkins-example
Repoistory URL: git@github.com:lifeisstillgood/frozone.git
Local subdirectory for repo (optional): frozone  # I need to collate the whole into a importable pyhtonpath using from frozone import ...

Skip internal tag: tick

Wipe out workspace before build: tick


ignore build triggers for now


Frankly this is a insecure approach and there is a turn off tagging checkbox so I may rethink this one.




parameterised builds
====================
https://wiki.jenkins-ci.org/display/JENKINS/Parameterized+Build
http://server/job/myjob/buildWithParameters?PARAMETER=Value



Build slaves
============

just ssh in.
windows machines...

Future
======

1. we can consider generating branches at push time

    git push origin HEAD:refs/heads/myNewFeature

2. and we can merge on jenkins - that is git pulls down myNewFeature and master, 
   merges the two, and tests it.  if it succeeds then (jenkins merges and pushes it back / we should push it back)


   number 2 is very useful, but needs integration into our personal workflow

3. nodes, parallel builds etc
   
   One jenkins server can control an army of nodes to complete different parameterised builds and run different tests, on different OSes, with different configurations.

   When we have sufficient tests to make this worthwhile ...


Tips
----

* Restarting is not obvious http://<jenkins>/restart
* Use the CLI - http://<jenkins>/cli
  java -jar jenkins-cli.jar -s http://cnx5:8080/ help

  Basically visit cli page, download the above jar file and run it locally with the above command.  Mostly used for restarting and safe-restart

  * ubuntu puts the jenkins homedir in /var/lib/jenkins.  I am sure its a good :file:`man hier` idea, but frankly it confuses the heck out of me each time.


