#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###  
# Copyright (c) Rice University 2012
# This software is subject to
# the provisions of the GNU Lesser General
# Public License Version 2.1 (LGPL).
# See LICENCE.txt for details.
###


from rhaptos2.client import restclient



def test_create_module():
    modlist = restclient.getworkspace_module_list('http://www.office.mikadosoftware.com')

    print restclient.create_module('http://www.office.mikadosoftware.com', 
                        'testmod', 'test content')
    modlist2 = restclient.getworkspace_module_list('http://www.office.mikadosoftware.com')

    if len(modlist2) > len(modlist):
        return True
    else:
        return False
    


def test_create_module_text():                   
     content='xxddffgg'
     saved_file_name = restclient.create_module('http://www.office.mikadosoftware.com',
                        'testmod', content)
     print saved_file_name['hashid']
     txtd = restclient.get_module_text('http://www.office.mikadosoftware.com',
                           saved_file_name['hashid'])
     txt = txtd['txtarea']
     if txt.find(content)>=0:
         return True
     else:
         return False

if __name__ == '__main__':
    test_create_module_text()
