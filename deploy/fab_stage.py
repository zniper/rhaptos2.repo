#!/usr/local/bin/python

'''
Fab file to do staging - given a git branch, extract it, and apply all necessary cofs - ready to deploy from.


'''

import fabric
import fabpass
from fabric.operations import put, open_shell, prompt
from fabric.api import sudo, run, local
import os


def clone_and_clean(localgitrepo, localstage, frozonehome):
    '''This is a means to do a SVN EXPORT
    
    ''' 
    #first, clean up the tgt folder.
    if os.path.isdir(localstage) is True:
        local('rm -rf %s' % localstage) 
        local('mkdir -p -m 0755 %s' % localstage) 


    local('git clone %s %s' % (localgitrepo, frozonehome))
    local('rm -rf %s' % os.path.join(frozonehome, '.git')) 

def mkvirtualenv(localstage):
    ''' '''
    local('virtualenv --extra-search-dir=%s %s/venv' % (localstage, localstage))
    #ensure I can import frozone from within virtualenv
    local('echo export PYTHONPATH=%s >> %s/venv/bin/activate' % (localstage, localstage))
    local('echo %s >> %s/venv/lib/python2.7/site-packages/frozone.pth' % (localstage, localstage))
    local('%s/venv/bin/pip install Fabric' % (localstage))

def stage(localgitrepo, localstage, configfile):
    '''given a git working copy, clone to a staging area, apply a
    certain config, and prepare it so it can be deployed '''

    frozonehome = os.path.join(localstage, 'frozone')

    clone_and_clean(localgitrepo, localstage, frozonehome)
#    mkvirtualenv(localstage)

    #apply the desired config file ... 
    local('cp %s/deploy/%s %s/conf.py' % (frozonehome, configfile, frozonehome))    
    
    #### from this point on I need to use the virtualenv

    local('python %s/deploy/runstaging.py %s' % (localstage, frozonehome))
