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


######################## Part II - testing

### Create a virtualenv with the current rhaptos2 in it.
### run the tests from that venv, doctests, network tests, etc.

. Rhaptos2/scripts/update_venv.sh $rhaptos2_current_version-$GIT_COMMIT


# now test
nosetests_cwd=$ENV/lib/python2.7/site-packages/rhaptos2/
nosetests -w $nosetests_cwd  --with-doctest -v


#nosetests --with-coverage --with-xunit --cover-package=rhpatos2 --cover-erase --xunit-file $WORKSPACE/nosetests.xml
#pylint -f parseable $nosetests_cwd | tee $WORKSPACE/pylint.out
