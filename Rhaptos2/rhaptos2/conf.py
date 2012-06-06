#!/usr/local/bin/python                                                                    

'''                                                                                        
Generic routines etc
THIS IS A COPY OF FILE: fab_lib.py  - manually keep in synch till apply a new pacakge and mark as dep.                                                                                           
                                                                                           
'''

import os

############################# Get config 
import ConfigParser

class Rhaptos2ConfigError(Exception):
    '''Put this in common area'''
    pass


def get_config():

    parser = ConfigParser.SafeConfigParser()
    parser.read('/usr/local/etc/rhaptos2/frozone.ini')
    globaldict = dict(parser.items('frozone'))

    ### get from the environment anything labelled rhaptos2_ as well
    ### test here???
    expected_keys = ['rhaptos2_current_version',  # such as '0.0.2'
                    ] 
    thisdict = {}
    for k in os.environ:
        if k.find('rhaptos2_') == 0:
            thisdict[k] = os.environ[k]
    for k in expected_keys:
        if k not in thisdict.keys():
             raise Rhaptos2ConfigError('%s not found in os.environ.  It is required.' % k)

    thisdict['rhaptos2_pkg_name'] = 'Rhaptos2-%s.tar.gz' % thisdict['rhaptos2_current_version']

    globaldict.update(thisdict)    

    return globaldict

