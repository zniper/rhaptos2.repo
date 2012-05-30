#!/usr/local/python

'''
useage::

  overwrite(contextdir, local_git_repo, local_staging_dir)

Frankly its a bit pants making files in doctests...

>>> import os, shutil
>>> shutil.rmtree('/tmp/foo', ignore_errors=True)
>>> os.mkdir('/tmp/foo') 
>>> tgtf = '/tmp/foo/bar.py'
>>> open(tgtf, 'w').write('One line that needs this token <<AAA>> to be replaced')
>>> overwrite({'<<AAA>>': 'REPLACEOK'}, '/tmp/None', '/tmp/foo')
>>> print open(tgtf).read()
One line that needs this token REPLACEOK to be replaced


'''

#batteries
import os, sys
#3rd party
import fabric
from fabric.api import local


# def clone_and_clean(remotegitrepo, localstagingdir, branch):
#     '''This is a means to do a SVN EXPORT
    
#     ''' 
#     #first, clean up the tgt folder.
#     if os.path.isdir(localstagingdir) is True:
#         local('rm -rf %s' % localstagingdir) 
#         local('mkdir -p -m 0755 %s' % localstagingdir) 

#     local('git clone -b %s %s %s' % (branch, 
#                                   remotegitrepo, 
#                                   localstagingdir))    

#     local('rm -rf %s' % os.path.join(localstagingdir,'.git')) 



def overwrite(contextdict, local_staging_dir):
    '''take src from one location, copy it out to tgt and replace 

    1. clone src repo, del .git dir 
    2. run the overwriter over it
    

    overwriter
    1. walk the tree from the local_staging_dir
    2. at each point identify right files via a glob
    3. for each file, open, replace, close.


    '''
    #prep dir

    OKsuffix = ['.py', '.js', '.conf', '.html']
    for root, dirs, files in os.walk(local_staging_dir):
        okfiles = [os.path.join(root,f) for f in files 
                     if os.path.splitext(f)[-1] in OKsuffix]
        print
        print root,  
        for f in okfiles:
            print '.',
            searchreplace(f, contextdict)
        
def searchreplace(f, contextdict):
    ''' 
   I *should* use a regex to find all <<xx>> and error if we find one
    that is not in context.  Wow this is a dumb replace. I woudl not
    pass this as code review

    '''
    txt_orig = open(f).read()
    txt_new = txt_orig

    for k in contextdict:
        # only sed replace for keys that are like <<xxxx>>
        if k.find('<<') >=0: 
            if txt_new.find(k) >= 0:
                print k, f
                txt_new = txt_new.replace(k, contextdict[k])
    open(f,'w').write(txt_new)


       

if __name__ == '__main__':
    import doctest
    doctest.testmod()
