#!/usr/local/bin/python                                                                    

'''                                                                                        
Generic routines etc
THIS IS A COPY OF FILE: fab_lib.py  - manually keep in synch till apply a new pacakge and mark as dep.                                                                                           
                                                                                           
'''



############################# below here must match with fab_lib.py
import os
import ConfigParser

class Rhaptos2ConfigError(Exception):
    '''Put this in common area'''
    pass


def get_config():

    parser = ConfigParser.SafeConfigParser()
    parser.read('/usr/local/etc/rhaptos2/rhaptos2.ini')
    confd = dict(parser.items('rhaptos2'))

    ### get from the environment anything labelled rhaptos2_ as well
    ### test here???
    expected_keys = ['rhaptos2_current_version',  # such as '0.0.2'
                    ] 

    thisdict = {}
    for k in os.environ:
        if k.find('rhaptos2_') == 0:
            thisdict[k] = os.environ[k]

    #update the global conf
    confd.update(thisdict)    

    for k in expected_keys:
        if k not in confd.keys():
             raise Rhaptos2ConfigError('config key %s not found.' % k)

    confd['rhaptos2_pkg_name'] = 'Rhaptos2-%s.tar.gz' % confd['rhaptos2_current_version']
    return confd

