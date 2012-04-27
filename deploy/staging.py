

'''
run over a given set of files in a given location, and replace certain tags with required conf 


useage::

  overwrite(contextdir, local_git_repo, local_staging_dir)



test location???

'''

import fabric
from fabric.api import local
import os, sys

def clone_and_clean(localgitrepodir, localstagingdir):
    '''This is a means to do a SVN EXPORT
    
    ''' 
    #first, clean up the tgt folder.
    if os.path.isdir(localstagingdir) is True:
        local('rm -rf %s' % localstagingdir) 
        local('mkdir -p -m 0755 %s' % localstagingdir) 

    local('git clone %s %s' % (localgitrepodir, localstagingdir))    
    local('rm -rf %s' % os.path.join(localstagingdir,'.git')) 


def overwrite(contextdict, local_git_repo,local_staging_dir):
    '''take src from one location, copy it out to tgt and replace 

    1. clone src repo, del .git dir 
    2. run the overwriter over it
    

    overwriter
    1. walk the tree from the local_staging_dir
    2. at each point identify right files via a glob
    3. for each file, open, replace, close.


    '''
    #prep dir
    clone_and_clean(local_git_repo, local_staging_dir)
    OKsuffix = ['.py', '.js', '.conf']
    for root, dirs, files in os.walk(local_staging_dir):
        okfiles = [os.path.join(root,f) for f in files if os.path.splitext(f)[-1] in OKsuffix]
        for f in okfiles:
            searchreplace(f, contextdict)
        
def searchreplace(f, contextdict):
    ''' I *should* use a regex to find all <<xx>> and error if we find one that is not in context.
    Wow this is a dumb replace. I woudl not pass this as code review

    '''
    txt_orig = open(f).read()
    txt_new = txt_orig

    for k in contextdict:
        txt_new = txt_new.replace(k, contextdict[k])
    open(f,'w').write(txt_new)



rackspace_context = {'<<AAA>>': 'replacedAAwithBB',
                     '<<BBB>>': 'replacedBBBwithCC',
                     }

office_context = {

'<<CDN-SERVER-NAME>>' : {'office': 'cdn.office.mikadosoftware.com', 
                         'rackspace': 'cdn.frozone.mikadosoftware.com',}


,'<<CDN-SERVER-ROOT>>': {'rackspace': '/usr/share/www/nginx/cdn'}



}


        

def main():

     
     src, tgt = sys.argv[1:]
     print '@@@@@', src, tgt
     overwrite(rackspace_context, src, tgt)





if __name__ == '__main__':
    main()
