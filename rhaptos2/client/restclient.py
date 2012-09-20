#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###  
# Copyright (c) Rice University 2012
# This software is subject to
# the provisions of the GNU Lesser General
# Public License Version 2.1 (LGPL).
# See LICENCE.txt for details.
###


'''


nomenclature
baseURL = http://www.office.mikadosoftware.com
RI = /pbrian/myworkspace
'''

import requests
import json
import os

proxy_dict = {

'http': 'marcus.office.mikadosoftware.com:8888',
'https': 'marcus.office.mikadosoftware.com:8888',
'ftp': 'marcus.office.mikadosoftware.com:8888',

}

#turn off using proxies
#proxy_dict = None

def client_whoami(baseURL):
    """Get details of who repo thinks is logged in

    """
    url = os.path.join(baseURL, 'whoami/')
    c = {'Cookie': '''session="y8qe/xrnhdLHBVNXpOkKVp8xoOg=?openid=UydodHRwczovL3d3dy5nb29nbGUuY29tL2FjY291bnRzL284L2lkP2lkPUFJdE9hd2xjN29ZazhNTmx3Qmd4Q3dNaExEcXpYcTFCWEE0YWJiaycKcDEKLg=="'''}
    resp = requests.get(url, proxies=proxy_dict, headers=c)
    x = resp.json
    return x
    
   
def getworkspace_module_list(baseURL):
    ''' '''
    url = os.path.join(baseURL, 'e2repo/workspace')
    resp = requests.get(url, proxies=proxy_dict)
    list_of_modules = resp.json
    return list_of_modules

def create_module(baseURL, modulename, text):      
    url = os.path.join(baseURL, 'e2repo/module/')
    print url
    jsonpayload = json.dumps({'modulename': modulename, 'txtarea':text})
    payload = {'moduletxt':jsonpayload}
    print payload
    resp = requests.post(url, data=payload, proxies=proxy_dict)
    return resp.json

def get_module_text(baseURL, savedname):
    url = os.path.join(baseURL, 'e2repo/module/%s' % savedname)
    print url
    resp = requests.get(url, proxies=proxy_dict)
    return resp.json
