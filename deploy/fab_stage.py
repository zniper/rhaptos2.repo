#!/usr/local/bin/python

'''
Fab file to do staging - given a git branch, extract it, and apply all necessary cofs - ready to deploy from.


'''

import fabric
import fabpass
from fabric.operations import put, open_shell, prompt
from fabric.api import sudo, run, local
import os

def clone_and_clean(localgitrepo, localstage):
    '''This is a means to do a SVN EXPORT
    
    ''' 
    #first, clean up the tgt folder.
    if os.path.isdir(localstage) is True:
        local('rm -rf %s' % localstage) 
        local('mkdir -p -m 0755 %s' % localstage) 

    local('git clone %s %s/frozone' % (localgitrepo, localstage))

    local('rm -rf %s' % os.path.join(localstage,'.git')) 

def mkvirtualenv(localstage):
    ''' '''
    local('virtualenv %s/venv' % localstage)
    #apply PYTHONPATH?

def stage(localgitrepo, localstage, configfile):
    '''given a git working copy, clone to a staging area, apply a
    certain config, and prepare it so it can be deployed '''

    clone_and_clean(localgitrepo, localstage)
    mkvirtualenv(localstage)

    #apply the desired config file ... 
    local('cp %s/frozone/deploy/%s %s/frozone/conf.py' % (localstage, configfile, localstage))    

