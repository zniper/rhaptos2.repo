#!/usr/local/bin/python                                                                    

'''                                                                                        
Generic routines etc
THIS IS A COPY OF FILE: fab_lib.py  - manually keep in synch till apply a new pacakge and mark as dep.                                                                                           
                                                                                           
'''



############################# below here must match with fab_lib.py
import os
import ConfigParser
from rhaptos2.exceptions import Rhaptos2Error

def sanitycheck():
    '''What are the things we want to be sure we have right at runtime?

    '''
    try:
        configfile = os.environ['CONFIGFILE']
        #assert os.path.isfile(configfile)
    except Exception, e:
        s = ''
        for k in os.environ: s += '\n%s:%s' % (k, os.environ[k]) 
        raise  Rhaptos2Error('#1 Cannot find ENV VAR of CONFIGFILE or cannot find it' + s)


def get_config():


    parser = ConfigParser.SafeConfigParser()
    try:
        parser.read(os.environ['CONFIGFILE'])
        confd = dict(parser.items('rhaptos2'))
    except Exception, e:
        print '*** Failed conf: %s' % os.environ['CONFIGFILE'] 
        raise e




    thisdict = {}
    for k in os.environ:
        if k.find('rhaptos2_') == 0:
            thisdict[k] = os.environ[k]

    #update the global conf
    confd.update(thisdict)    

    #### Grab expected os.environ
    confd['CONFIGFILE'] = os.environ['CONFIGFILE']

    return confd

sanitycheck()
confd = get_config()

