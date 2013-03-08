#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""run.py - Launch the repo app.

Author: Paul Brian
(C) 2012 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from rhaptos2.repo import make_app
from rhaptos2.common import conf
import os
import json
import decl
from webtest import TestApp
import webtest
from optparse import OptionParser
import urlparse

from rhaptos2.repo.configuration import (
    find_configuration_file,
    Configuration,
    )



def parse_args():
    parser = OptionParser()
    parser.add_option("--host", dest="host",
                      help="hostname to listen on")
    parser.add_option("--port", dest="port",
                      help="port to listen on", type="int")
    parser.add_option("--debug", dest="debug", action="store_true",
                      help="debug on.", default=False)

    parser.add_option("--conf", dest="conf",
                      help="Path to config file.")

    (options, args) = parser.parse_args()
    return (options, args)







    
def build_environ():
    """
    We are playing at a low level with WSGI - wanting to wrap repoze.
    http://www.python.org/dev/peps/pep-0333/

    To test manually we need to generate correct HTTP Headers
    """
    import StringIO
    request_fo = StringIO.StringIO()
    err_fo = StringIO.StringIO()
    
    ###wsgi reqd keys and default valus
    wsgi_specific_headers = {"wsgi.version": (1,0),
                             "wsgi.url_scheme": "http",
                             "wsgi.input": request_fo,
                             "wsgi.errors": err_fo,
                             "wsgi.multithread": False,
                             "wsgi.multiprocess": False,
                             "wsgi.run_once": False
                            }
    
    ### key = HEADER (RFCLOC, NOTNULL, validvalues)
    HTTP_HEADERS = {"REQUEST_METHOD": "GET",
                    "SCRIPT_NAME": "module",
                    "PATH_INFO": "/cnxmodule:1234/",
                    "QUERY_STRING": "",
                    "CONTENT_TYPE": "",
                    "CONTENT_LENGTH": "",
                    "SERVER_NAME": "1.2.3.4",
                    "SERVER_PORT": "80",
                    "SERVER_PROTOCOL": "HTTP/1.1"
                    }
    d = {}
    d.update(wsgi_specific_headers)
    d.update(HTTP_HEADERS)
    return d
    

###### CONSTANTS
moduleuri = "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126"
collectionuri = "cnxcollection:be7790d1-9ee4-4b25-be84-30b7208f5db7"
folderuri = "cnxfolder:c192bcaf-669a-44c5-b799-96ae00ef4707"

gooduseruri = "cnxuser:1234"
rouseruri = "cnxuser:5432"
baduseruri = "cnxuser:00000"

userhost="http://localhost:8000/"
###


APIMAP = {'modules':     urlparse.urljoin(userhost, "module/"),
          'collections': urlparse.urljoin(userhost, "collection/"),
          'folders':     urlparse.urljoin(userhost, "folder/"),
          'workspace':  urlparse.urljoin(userhost, "workspace/"),

          'module':     urlparse.urljoin(userhost, "module/%(id_)s"),
          'collection': urlparse.urljoin(userhost, "collection/%(id_)s"),
          'folder':     urlparse.urljoin(userhost, "folder/%(id_)s"),

          'moduleACL':     urlparse.urljoin(userhost, "module/%(id_)s/acl/"),
          'collectionACL': urlparse.urljoin(userhost, "collection/%(id_)s/acl/"),
          'folderACL':     urlparse.urljoin(userhost, "folder/%(id_)s/acl/"),
          
          }


def get_url(resourcetype, id_=None, method=None):
    """ return the correct URL to call for various resource operations

    
    >>> get_url("collections", id_=None)
    'http://localhost:8000/collection/'

    >>> get_url("folders", id_=None)
    'http://localhost:8000/folder/'

    >>> get_url("modules", id_=None)
    'http://localhost:8000/module/'
    
    >>> get_url("collection", id_="foo1", method="GET")
    'http://localhost:8000/collection/foo1'

    >>> get_url("collection", id_="foo1", method="POST")
    'http://localhost:8000/collection/foo1'
    

    >>> get_url("folder", id_="foo")
    'http://localhost:8000/folder/foo'

    >>> get_url("module", id_="foo")
    'http://localhost:8000/module/foo'

    >>> get_url("collectionACL", id_="foo")
    'http://localhost:8000/collection/foo/acl/'

    >>> get_url("folderACL", id_="foo")
    'http://localhost:8000/folder/foo/acl/'

    >>> get_url("moduleACL", id_="foo")
    'http://localhost:8000/module/foo/acl/'
    
    >>> get_url("collection", id_="cnxcollection:1234")
    'http://localhost:8000/collection/cnxcollection:1234'


    Its pretty simple api so far...
    
    .. todo::
       ensure urljoin is done well - urlparse version not really as expected...
    
    """
    baseurl = APIMAP[resourcetype]
    if baseurl.find("%")>=0:    
        url = baseurl % {"id_": id_}
    else:
        url = baseurl
    return url

def wapp_post(wapp, url, data, owner):
    headers = {'X-Cnx-FakeUserId': owner,}
    print "in wapp post"
    print "**********************"
    print url
    print wapp
    
    try:
        resp = wapp.post_json(url, params=data, headers=headers)
    except Exception, e:
        import traceback
        tb = traceback.format_exc()
        print e, tb
    return resp

    
def wapp_put(wapp, data, owner, resourcetype, id_=None):
    headers = {'X-Cnx-FakeUserId': owner,}
    url = get_url(resourcetype, id_=id_)
    print url, id_, resourcetype
    try:
        resp = wapp.put_json(url, params=data, headers=headers)
    except Exception, e:
        import traceback
        tb = traceback.format_exc()
        print e, tb
    return resp

    
def post_generic(wapp, resourcetype, owner):
    """Create all modules via the wsgi app provided"""
    print "post generic called", resourcetype
    data = decl.declarationdict["module"]
    url  = get_url("modules")
    resp = wapp_post(wapp, url, data, owner)
    return resp
    

def put_generic(wapp, resourcetype, owner, url, data, id_):
    print "putgeneric called", resourcetype
    wapp_put(wapp, url, data, owner, resourcetype, id_)

def put_module(wapp):
    owner = gooduseruri
    d = decl.declarationdict['sect1']
    d['content'] = "Dear King George, cup of tea?"
    wapp_put(wapp, d, owner, "module", d['id_'])

def put_folder():
    owner =gooduseruri
    d = decl.declarationdict['folder']
    d['content'] = [moduleuri,]
    wapp_put(wapp, d, owner, "folder", d['id_'])

def get_module(wapp):
    m = moduleuri
    resp = wapp.get(urlparse.urljoin(userhost,"module/" + m ))
    return resp


def setacl_collection():
    owner =gooduseruri
    acls = decl.acllist
    headers = {'X-Cnx-FakeUserId': owner,
               'content-type':'application/json'}
    resp = requests.put(urljoin(userhost, "collection/" +
                  collectionuri +
                  "/acl/"),
                  data=json.dumps(acls), headers=headers)
    capture_conversation(resp)
    print resp


def del_collection():
    owner =gooduseruri
    headers = {'X-Cnx-FakeUserId': owner,
              }
    resp = requests.delete(urljoin(userhost, "collection/" +
                        collectionuri
                        +"/"),
                        headers=headers)
    capture_conversation(resp)
    print resp

def wapp_del(wapp):
    owner = gooduseruri
    headers = {'X-Cnx-FakeUserId': owner,
               }
    resp = wapp.delete(urlparse.urljoin(userhost, "module/" +
                                   moduleuri+"/"),
                           headers=headers)
    print resp

def del_module():
    owner =gooduseruri
    headers = {'X-Cnx-FakeUserId': owner,
               }
    resp = requests.delete(urljoin(userhost, "module/" +
                                   moduleuri
                                   +"/"),
                           headers=headers)
    capture_conversation(resp)
    print resp


def _put(resource, json_to_send, fake_user_id, id_):

    headers = {'X-Cnx-FakeUserId': fake_user_id,
               'content-type':'application/json'}

    resp = requests.put(urljoin(userhost, "%s/%s/" % (resource, id_)),
                        data=json_to_send,
                        headers=headers)
    capture_conversation(resp)
    print resp.text


    # requests.put(urljoin(userhost,
    #              "user/org.cnx.user-75e06194-baee-4395-8e1a-566b656f6920"))
    # r = requests.get(urljoin(userhost,
    #                  "openid/?user=https://paulbrian.myopenid.com"))
    # d = r.json
    # assert d['fullname'] == 'testput-fullname'

def capture_conversation(resp):
    """ """
    rst = restrest.restrest(resp)
    fo = open("output.rst", "a")
    fo.write(rst)
    fo.close()

help = """

test_post_module
test_put_module
test_put_module_acl
test_acl_ro_ok
test_acl_ro_fail
test_acl_rw_ok
test_acl_rw_fail
test_delete_module

 """


### this is all so generic i should use test generators
class test_post(object):

    def setup(self):
#        opts, args = parse_args()
        CONFD_PATH = os.path.abspath("../../pbrian.ini")  ##pass in through nose...
        print "here"

    #    confd = conf.get_config(CONFD_PATH)
        config = Configuration.from_file(CONFD_PATH)

        app = make_app(config)
        app.debug=True
        #from waitress import serve
        #serve(app.wsgi_app, host='0.0.0.0', port=8080)

        from webtest import TestApp
        self.wapp = TestApp(app.wsgi_app)
        
    
    def test_post_module(self):
        resp = post_generic(self.wapp, "modules", gooduseruri)
        returned_module_uri = resp.json['id_']
        #assert returned_module_uri == moduleuri

    def test_post_folder(self):
        resp = post_generic(self.wapp, "folders", gooduseruri)
        returned_folder_uri = resp.json['id_']
        #assert returned_folder_uri == folderuri

    def test_post_collection(self):
        resp = post_generic(self.wapp, "collections", gooduseruri)
        returned_collection_uri = resp.json['id_']
        #assert returned_collection_uri == collectionuri


    ### PUTS
    #def test_put_module(self):
    #    url = get_url("module", id_=moduleuri)
    #    resp = wapp_put(self.wapp, "module", gooduseruri, moduleuri)


#import doctest
#doctest.testmod()


if __name__ == '__main__':
    c = test_post()
    c.setup()
#    from waitress import serve
#    serve(c.wapp, host='0.0.0.0', port=8000)
    #its a test appp!!!

    r2 = wapp_post(c.wapp, "http://localhost:8000/module/", decl.declarationdict['module'], 'niceguyeddie')
    r = get_module(c.wapp)
    r = wapp_del(c.wapp)
    print r