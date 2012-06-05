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
