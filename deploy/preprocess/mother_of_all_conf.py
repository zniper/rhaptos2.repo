
# support - Makefile, fabfiles, python and js conf.
'''

Summary
-------

I have a seperate folder, _config, which is designed to hold 
ALL configuration files for the whole of frozone.

I have a make, fab, python and js configuration need, plus find/repalce need

So, this file holds the canonical configuration details, such as a pathname
This file then generates the other config files, and stops.

At deploy time, the staging process will pick up the _config files and move them as needed

so its a two stage process

1. _config -> take from one central point and prep other config files
2. using the _config now set up, run make, fab and find/replace



Handling configuration sanely. Slightly anyway.

1. have one configuration central point - this will be conf.py

1.a. conf.py populates where needed the OTHER configuration files

1.b. which are used by staging to find/replace the conf strings in all various actual code bits.


This may not seem a useful step, but it ensures that the different constants
files used by make, fab and js / python all come from one point.

Its small but sanity saving


* conf.js - holds a dict-like object that in raw form looks like::
  
       e2serverFQDN : "<<CDN-SERVER-NAME>>",

  NOACTIONHERE

* conf.py ::

   this file

* conf.mk - holds the conf used by the Makefile::

   localhome = /tmp/frozone  
   
  LOAD FROM HERE

* fab.conf - holds stuff that really is just to stop me passing in large numbers of constants as arguments.

'''

import os


### just making things more complicated...
localhomedir = '/tmp/mikado'
remotehomedir = '/home/deployagent'

confd = {

    'TINYMCE_STORE':'/usr/home/pbrian/frozone/thirdparty/tinymce',

    'localhomedir' : localhomedir,
    'localgitrepo' : os.path.join(localhomedir, 'git'),
    'localstagingdir' : os.path.join(localhomedir, 'staging'),
    'remote_git_repo' : 'git://github.com/lifeisstillgood/frozone.git',

    'remote_wwwd':'/usr/share/www/nginx/www',
    'remote_e2repo':'/usr/share/www/flask/e2repo',
    'remote_e2server':'/usr/share/www/flask/e2server',
    'remotehomedir' : remotehomedir,
    'remote_supervisor' : os.path.join(remotehomedir, 'supervisor'),
}

confmk = '''
srcdir = %(localgitrepo)s
TINYMCE_STORE = %(TINYMCE_STORE)s
localhome = %(localhomedir)s
localgit = %(localgitrepo)s
localstaging = %(localstagingdir)s
remote_git_repo = %(remote_git_repo)s
remote_wwwd = %(remote_wwwd)s
remote_e2repo = %(remote_e2repo)s
remote_e2server = %(remote_e2server)s
remotehomedir = %(remotehomedir)s
remote_supervisor = %(remote_supervisor)s
'''

def write_makeconf():
    ''' '''
    tgtf = 'conf.mk'
    open(tgtf, 'w').write(confmk % confd)


staging_conf = '''
# CONSTANTS
rackspace_context = {
 '<<CDN-SERVER-NAME>>': 'cdn.frozone.mikadosoftware.com',
 '<<CDN-SERVER-ROOT>>': '/usr/share/www/nginx/cdn',
 '<<REPO-SERVER-NAME>>': 'cdn.frozone.mikadosoftware.com',
 '<<WWW-SERVER-NAME>>': 'www.frozone.mikadosoftware.com',
 '<<WWW-SERVER-ROOT>>': '/usr/share/www/nginx/www',
                     }

office_context = {
 '<<CDN-SERVER-NAME>>': 'cdn.office.mikadosoftware.com',
 '<<CDN-SERVER-ROOT>>': '/usr/share/www/nginx/cdn',
 '<<REPO-SERVER-NAME>>': 'www.office.mikadosoftware.com',
 '<<WWW-SERVER-NAME>>': 'www.office.mikadosoftware.com',
 '<<WWW-SERVER-ROOT>>': '/usr/share/www/nginx/www',



                     }

fillet_context = {
 '<<CDN-SERVER-NAME>>': 'cdn.fillet.mikadosoftware.com',
 '<<CDN-SERVER-ROOT>>': '/usr/share/www/nginx/cdn',
 '<<REPO-SERVER-NAME>>': 'repo.fillet.mikadosoftware.com',
 '<<WWW-SERVER-NAME>>': 'www.fillet.mikadosoftware.com',
 '<<WWW-SERVER-ROOT>>': '/usr/share/www/nginx/www',

                     }

'''

def write_stagingconf():
    tgtf = 'staging_conf.py'
    open(tgtf, 'w').write(staging_conf % confd)
    s = ''
    for k in confd:
        s += "%s = '%s'\n" % (k, confd[k])
    open(tgtf, 'a').write(s)

def main():

   write_makeconf()
   write_stagingconf()


if __name__ == '__main__':
    main()
