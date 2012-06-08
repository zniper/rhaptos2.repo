#!/usr/local/bin/bash

### This is to run from the developer local copy, 
### It will install, with fabfiles, the repo + web stuff
### It will install NOT the git Index or HEAD but the W/C.  
###
### Repeat - it installs the current working copy.  So run from top dir.
###
### If you want to install from HEAD (i.e. use git clone as Jenkins will)
###  then set developer=False below.

#######  Git tool - used to extract the current SHA1 of the HEAD of the current branch.  Not *accurate* for working copy but its developer-local so ... 

### taken from
## http://sleeplesscoding.blogspot.co.uk/2010/04/find-sha1-of-latest-commit-in-git.html
## and
## elsewhere
## When run on a working copy will output the SHA1 of the last commit on that branch
##                                               
                                                 
                                                 
function whatbranch {                            
 git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/'
}                                                
                                                 
function whatsha {                               
 git log -1 --pretty=oneline $(whatbranch) | sed -E "s/^([^[:space:]]+).*/\1/"
}                                                

### already setup in Jenkins parameters, so create here
export WORKSPACE=/tmp/mikado
export GIT_COMMIT=$(whatsha)
export CONFIGFILE=conf.d/rhaptos2.ini
export WEBHOST=devweb

############### Part 1 (as seen in jenkins)
export LOCALGITREPO=./
export LOCALSTAGE=$WORKSPACE/stage/$GIT_COMMIT 
export rhaptos2_current_version=0.0.2
echo ***
echo LOCALGITREPO = $LOCALGITREPO
echo LOCALSTAGE = $LOCALSTAGE
echo CONFIGFILE = $CONFIGFILE
echo ***


cd $LOCALGITREPO
make clean
make stage localgitrepo=$LOCALGITREPO \
           localstage=$LOCALSTAGE \
           configfile=$CONFIGFILE \
           host=devjenkins \
           fabfile=deploy/fab_stage.py \
           developer=True
#host not important here - all fab calls are local()


cd $LOCALSTAGE

make clean-remote \
     host=$WEBHOST \
     fabfile=deploy/fab_app_frozone.py \
     localstagingdir=$LOCALSTAGE

make remote-install-e2repo \
     host=$WEBHOST \
     fabfile=deploy/fab_app_frozone.py \
     localstagingdir=$LOCALSTAGE \
     configfile=$CONFIGFILE

make remote-install-cdn host=$WEBHOST \
                        fabfile=deploy/fab_app_frozone.py \
                        localstagingdir=$LOCALSTAGE

#dont bother most of the time...
#make remote-install-tiny host=$WEBHOST \
#                          fabfile=deploy/fab_app_frozone.py



