#!/usr/local/bin/python

'''
Given an local git working copy, extract it to a staging area, apply configs

We shall ask Jenkins to download/pull a branch, and that will be *localgitrepo*
We shall then run :py:clone_and_clean which will mv the code to a new *staging* location.
After that we shall apply the config necessary for the given server environment target (ie is this going into beta)
then we shall run *staging* which is at the moment a simple token based search/replace




'''

import fabric
from fabric.operations import put, open_shell, prompt
from fabric.api import sudo, run, local
import os

def set_ini(configfile, localstage, localgitrepo):
    '''Write the config file chosen by the make cmd to this environment

    I suspect ENV vars would be better. 

    example: we want to put the office.ini file in as the /etc/frozone.ini
    '''

    local('cp %s/%s /usr/local/etc/rhaptos2/frozone.ini' % (localgitrepo, configfile) )
 

def clone_and_clean(localgitrepo, localstage):
    '''This is a means to do a SVN EXPORT
    
    ''' 
    #first, clean up the tgt folder.
    if os.path.isdir(localstage) is True:
        local('rm -rf %s' % localstage) 
        local('mkdir -p -m 0755 %s' % localstage) 

    local('git clone %s %s' % (localgitrepo, localstage))
    local('rm -rf %s' % os.path.join(localstage, '.git')) 

def stage(localgitrepo, localstage, configfile):
    '''given a git working copy, clone to a staging area, apply a
    certain config, and prepare it so it can be deployed 
    i.e. copy everything to /tmp/stage/frozone, sed, then run fab files from there.
    '''


    set_ini(configfile, localstage, localgitrepo)
    clone_and_clean(localgitrepo, localstage)

    local('python %s/deploy/runstaging.py %s' % (localstage, localstage))
