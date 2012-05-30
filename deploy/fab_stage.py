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


def clone_and_clean(localgitrepo, localstage, tgtdir):
    '''This is a means to do a SVN EXPORT
    
    ''' 
    #first, clean up the tgt folder.
    if os.path.isdir(localstage) is True:
        local('rm -rf %s' % localstage) 
        local('mkdir -p -m 0755 %s' % localstage) 

    local('git clone %s %s' % (localgitrepo, tgtdir))
    local('rm -rf %s' % os.path.join(tgtdir, '.git')) 

def stage(localgitrepo, localstage, configfile):
    '''given a git working copy, clone to a staging area, apply a
    certain config, and prepare it so it can be deployed 
    i.e. copy everything to /tmp/stage/frozone, sed, then run fab files from there.
    '''

    tgtdir = os.path.join(localstage, 'frozone')

    clone_and_clean(localgitrepo, localstage, tgtdir)

    #apply the desired config file ... 
    local('cp %s/deploy/%s %s/conf.py' % (tgtdir, configfile, tgtdir))    
    local('''cat >> %s/conf.py << EOF 

localstage      = '%s'
localgitrepo    = '%s'
localstagingdir = localstage    
EOF
''' % (tgtdir, localstage, localgitrepo))

    local('python %s/deploy/runstaging.py %s' % (tgtdir, tgtdir))
