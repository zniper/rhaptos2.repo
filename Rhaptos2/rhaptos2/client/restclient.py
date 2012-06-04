#!/usr/local/bin/python


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

def test_workspaceisempty(baseURL):
    ''' '''
    url = os.path.join(baseURL, 'e2repo/workspace')
    resp = requests.get(url, proxies=proxy_dict)
    list_of_modules = resp.json
    return list_of_modules

def test_create_module(baseURL, modulename, text):      
    url = os.path.join(baseURL, 'e2repo/module/')
    print url
    jsonpayload = json.dumps({'modulename': modulename, 'txtarea':text})
    payload = {'moduletxt':jsonpayload}
    print payload
    resp = requests.post(url, data=payload, proxies=proxy_dict)
    return resp.json

print test_workspaceisempty('http://www.office.mikadosoftware.com')
print test_create_module('http://www.office.mikadosoftware.com', 
                        'testmod', 'test test')
print test_workspaceisempty('http://www.office.mikadosoftware.com')
