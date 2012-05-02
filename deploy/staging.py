#!/usr/local/bin/python


'''

This is the main function side of staginglib.
It expects a call like ::


    staging.py --context=rackspace --src=/home/paul/code/frozone --tgt=/tmp/frozone --branch=fobar

And it will 'extract' code from the git repo in 





'''
#batteries
import os, sys
import optparse
#3rd party
import fabric
from fabric.api import local
#app
import frozoneErrors
import staginglib




def stage_repo(contextdict, remote_git_repo, local_staging_dir, branch):
    '''the main call if you will 

    'export' a git repo to a local folder
    now do simple token replace acorss all the files.

    I am sure it will gt more complex over time

    '''
    
    staginglib.clone_and_clean(remote_git_repo, local_staging_dir, branch) 
    staginglib.overwrite(contextdict, local_staging_dir)



def main(argv=None):


    if argv is None:
        argv = sys.argv

    parser = optparse.OptionParser()
    parser.add_option('-s', '--src', dest='src', 
                      help='The folder where the git repo is.')
    parser.add_option('-t', '--tgt', dest='tgt', 
                      help='The folder where the git repo will be \
                      "exported" to and then manipulated i.e. sed.')
    parser.add_option('-b', '--branch', dest='branch', 
                      help='The branch to clone out of repo.')
    parser.add_option('-c', '--context', dest='context', 
                      help='The dict, kept in this file, that will \
                   be used when replacing tokens in files in \
                   tgt folder.')

    (options, args) = parser.parse_args(args=argv[1:])

    thiscontext = CONTEXT_MAP[options.context]
    stage_repo(thiscontext, options.src, options.tgt, options.branch)



# CONSTANTS
rackspace_context = {
 '<<CDN-SERVER-NAME>>': 'cdn.frozone.mikadosoftware.com',
 '<<CDN-SERVER-ROOT>>': '/usr/share/www/nginx/cdn',

 '<<REPO-SERVER-NAME>>': 'cdn.frozone.mikadosoftware.com',
 '<<WWW-SERVER-NAME>>': 'cdn.frozone.mikadosoftware.com',
                     }

office_context = {
 '<<CDN-SERVER-NAME>>': 'cdn.office.mikadosoftware.com',
 '<<CDN-SERVER-ROOT>>': '/usr/share/www/nginx/cdn',
 '<<REPO-SERVER-NAME>>': 'repo.office.mikadosoftware.com',
 '<<WWW-SERVER-NAME>>': 'repo.office.mikadosoftware.com',

                     }

fillet_context = {
 '<<CDN-SERVER-NAME>>': 'cdn.fillet.mikadosoftware.com',
 '<<CDN-SERVER-ROOT>>': '/usr/share/www/nginx/cdn',
 '<<REPO-SERVER-NAME>>': 'repo.fillet.mikadosoftware.com',
 '<<WWW-SERVER-NAME>>': 'repo.fillet.mikadosoftware.com',

                     }


CONTEXT_MAP = {

    'office':office_context,
    'rackspace':rackspace_context,
    'fillet':fillet_context,
}




if __name__ == '__main__':
    sys.exit(main())

