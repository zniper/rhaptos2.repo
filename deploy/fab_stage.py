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


def clone_and_clean(localgitrepo, localstage, frozonehome):
    '''This is a means to do a SVN EXPORT
    
    ''' 
    #first, clean up the tgt folder.
    if os.path.isdir(localstage) is True:
        local('rm -rf %s' % localstage) 
        local('mkdir -p -m 0755 %s' % localstage) 


    local('git clone %s %s' % (localgitrepo, frozonehome))
    local('rm -rf %s' % os.path.join(frozonehome, '.git')) 

# def mkvirtualenv(localstage):
#     '''DEPRECATED '''
#     local('virtualenv --extra-search-dir=%s %s/venv' % (localstage, localstage))
#     #ensure I can import frozone from within virtualenv
#     local('echo export PYTHONPATH=%s >> %s/venv/bin/activate' % (localstage, localstage))
#     local('echo %s >> %s/venv/lib/python2.7/site-packages/frozone.pth' % (localstage, localstage))
#     local('%s/venv/bin/pip install Fabric' % (localstage))

def stage(localgitrepo, localstage, configfile):
    '''given a git working copy, clone to a staging area, apply a
    certain config, and prepare it so it can be deployed '''

    frozonehome = os.path.join(localstage, 'frozone')

    clone_and_clean(localgitrepo, localstage, frozonehome)
#    mkvirtualenv(localstage)

    #apply the desired config file ... 
    local('cp %s/deploy/%s %s/conf.py' % (frozonehome, configfile, frozonehome))    
    local('''cat >> %s/conf.py << EOF 

localstage      = '%s'
localgitrepo    = '%s'
localstagingdir = localstage    
EOF
''' % (frozonehome, localstage, localgitrepo))
    #### from this point on I need to use the virtualenv

    local('export PYTHONPATH=/tmp/staging && python %s/deploy/runstaging.py %s' % (frozonehome, frozonehome))