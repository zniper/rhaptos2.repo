#!/usr/local/bin/bash

### Assuming run from the top level of frozone.
### This will deploy the current working copy, irrespective of Index / commit

# 1. stage the w/c
# 2. from the stage, run fabfiles

# 1. build a virtualenv of the working copy
# 2. run the nosetests, locally and remotely.


###

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

### already setup in Jenkins parameters
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
make stage localgitrepo=$LOCALGITREPO localstage=$LOCALSTAGE configfile=$CONFIGFILE host=devjenkins fabfile=deploy/fab_stage.py developer=True




cd $LOCALSTAGE
make clean-remote host=$WEBHOST fabfile=deploy/fab_app_frozone.py localstagingdir=$LOCALSTAGE
make remote-install-e2repo host=$WEBHOST fabfile=deploy/fab_app_frozone.py localstagingdir=$LOCALSTAGE configfile=$CONFIGFILE
make remote-install-cdn host=$WEBHOST fabfile=deploy/fab_app_frozone.py localstagingdir=$LOCALSTAGE
#dont bother most of the time...
#make remote-install-tiny host=$WEBHOST fabfile=deploy/fab_app_frozone.py