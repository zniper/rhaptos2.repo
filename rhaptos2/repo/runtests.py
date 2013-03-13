#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""run.py - Launch the repo app.

Author: Paul Brian
(C) 2012 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.


.. todo::

   * replace mess of functions and @decorators with routes on routes
     (idea: name each route then can build route from name and vice versa with Routes.)

   * 
"""

from rhaptos2.repo import make_app
from rhaptos2.common import conf
import os, sys
import json
import decl
from webtest import TestApp
import webtest
from optparse import OptionParser
import urlparse
import backend

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
    

###### CONSTANTS FOR TESTING.
moduleuri = "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126"
collectionuri = "cnxcollection:be7790d1-9ee4-4b25-be84-30b7208f5db7"
folderuri = "cnxfolder:c192bcaf-669a-44c5-b799-96ae00ef4707"

gooduseruri = decl.users['paul'].useruri
rouseruri = decl.users['ed'].useruri
baduseruri = decl.users['ross'].useruri

userhost="http://localhost:8000/"
###


APIMAP = {'module':
                   {"POST" : urlparse.urljoin(userhost, "module/"),
                    "GET" : urlparse.urljoin(userhost, "module/%(id_)s"),
                    "PUT" : urlparse.urljoin(userhost, "module/%(id_)s"),
                    "DELETE" : urlparse.urljoin(userhost, "module/%(id_)s"),
                   },
          
          'collection':
                   {"POST" : urlparse.urljoin(userhost, "collection/"),
                    "GET" : urlparse.urljoin(userhost, "collection/%(id_)s"),
                    "PUT" : urlparse.urljoin(userhost, "collection/%(id_)s"),
                    "DELETE" : urlparse.urljoin(userhost, "collection/%(id_)s"),
                   },

          'folder':
                   {"POST" : urlparse.urljoin(userhost, "folder/"),
                    "GET" : urlparse.urljoin(userhost, "folder/%(id_)s"),
                    "PUT" : urlparse.urljoin(userhost, "folder/%(id_)s"),
                    "DELETE" : urlparse.urljoin(userhost, "folder/%(id_)s"),
                   },

           'module_acl':
                   {"POST" : urlparse.urljoin(userhost, "module/%(id_)s/acl/"),
                    "GET" : urlparse.urljoin(userhost, "module/%(id_)s/acl/"),
                    "PUT" : urlparse.urljoin(userhost, "module/%(id_)s/acl/"),
                    "DELETE" : urlparse.urljoin(userhost, "module/%(id_)s/acl/"),
                   },
          
          'collection_acl':
                   {"POST" : urlparse.urljoin(userhost, "collection/%(id_)s/acl/"),
                    "GET" : urlparse.urljoin(userhost, "collection/%(id_)s/acl/"),
                    "PUT" : urlparse.urljoin(userhost, "collection/%(id_)s/acl/"),
                    "DELETE" : urlparse.urljoin(userhost, "collection/%(id_)s/acl/"),
                   },

          'folder_acl':
                   {"POST" : urlparse.urljoin(userhost, "folder/%(id_)s/"),
                    "GET" : urlparse.urljoin(userhost, "folder/%(id_)s/acl/"),
                    "PUT" : urlparse.urljoin(userhost, "folder/%(id_)s/acl/"),
                    "DELETE" : urlparse.urljoin(userhost, "folder/%(id_)s/acl/"),
                   },
                    
          }


def get_url(resourcetype, id_=None, method=None):
    """ return the correct URL to call for various resource operations

    
    >>> get_url("collection", id_=None, method="POST")
    'http://localhost:8000/collection/'

    >>> get_url("folder", id_=None, method="POST")
    'http://localhost:8000/folder/'

    >>> get_url("module", method="POST")
    'http://localhost:8000/module/'
    
    >>> get_url("collection", id_="xxx", method="GET")
    'http://localhost:8000/collection/xxx'

    >>> get_url("collection", id_="xxx", method="GET")
    'http://localhost:8000/collection/xxx'

    >>> get_url("folder", id_="xxx", method="GET")
    'http://localhost:8000/folder/xxx'
    
    >>> get_url("folder", id_="xxx", method="PUT")
    'http://localhost:8000/folder/xxx'

    >>> get_url("module", id_="xxx", method="PUT")
    'http://localhost:8000/module/xxx'

    >>> get_url("collection_acl", id_="xxx", method="PUT")
    'http://localhost:8000/collection/xxx/acl/'

    >>> get_url("folder_acl", id_="xxx", method="PUT")
    'http://localhost:8000/folder/xxx/acl/'

    >>> get_url("module", id_="xxx", method="DELETE")
    'http://localhost:8000/module/xxx'

    >>> get_url("collection_acl", id_="xxx", method="DELETE")
    'http://localhost:8000/collection/xxx/acl/'

    >>> get_url("folder_acl", id_="xxx", method="DELETE")
    'http://localhost:8000/folder/xxx/acl/'
    
    Its pretty simple api so far...
    
    .. todo::
       ensure urljoin is done well - urlparse version not really as expected...
    
    """
    ##restype, id method
    ## what if invalid restype?
    baseurl = APIMAP[resourcetype][method]

    if baseurl.find("%")>=0:    
        url = baseurl % {"id_": id_}
    else:
        url = baseurl
    return url

def wapp_get(wapp, resourcetype, id_, owner):
    """ """
    headers = {'X-Cnx-FakeUserId': owner,}
    URL = get_url(resourcetype, id_=id_, method="GET")
    try:
        resp =  wapp.get(URL, status="*", headers=headers)    
    except Exception, e:
        import traceback
        tb = traceback.format_exc()
        print "\/" * 32
        print e, tb
        print "/\\" * 32 
    return resp

def wapp_post(wapp, resourcetype, data, owner):
    """ ?
    """
    URL = get_url(resourcetype, id_=None, method="POST")
    headers = {'X-Cnx-FakeUserId': owner,}
    
    try:
        resp = wapp.post_json(URL, params=data, headers=headers, status="*")
    except Exception, e:
        import traceback
        tb = traceback.format_exc()
        print "\/" * 32
        print e, tb,
        print "/\\" * 32
        print URL
    return resp

def wapp_delete(wapp, resourcetype, id_, owner):
    """
    """
    URL = get_url(resourcetype, id_=id_, method="DELETE")
    headers = {'X-Cnx-FakeUserId': owner,
               }
    resp = wapp.delete(URL, headers=headers, status="*")
    return resp
    
    
    
def wapp_put(wapp, resourcetype, data, owner, id_=None):
    headers = {'X-Cnx-FakeUserId': owner,}
    URL = get_url(resourcetype, method="PUT", id_=id_)
    print "Putting to %s" % URL
    try:
        resp = wapp.put_json(URL, params=data, headers=headers, status="*")
    except Exception, e:
        import traceback
        tb = traceback.format_exc()
        print e, tb
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


def test_post_module():
    resp = wapp_post(TESTAPP, "module", decl.declarationdict['module'], gooduseruri)
    returned_module_uri = resp.json['id_']
    assert returned_module_uri == moduleuri

def test_post_folder():
    resp = wapp_post(TESTAPP, "folder", decl.declarationdict['folder'], gooduseruri)
    returned_folder_uri = resp.json['id_']
    assert returned_folder_uri == folderuri

def test_post_collection():
    resp = wapp_post(TESTAPP, "collection", decl.declarationdict['collection'], gooduseruri)    
    returned_collection_uri = resp.json['id_']
    assert returned_collection_uri == collectionuri

def test_put_collection():
    data = decl.declarationdict['collection']
    data['Body'] = ["cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126",]
    resp = wapp_put(TESTAPP, "collection", data, gooduseruri, collectionuri)    
    assert len(resp.json['Body']) == 1

def test_put_collection_rouser():
    data = decl.declarationdict['collection']
    data['Body'] = ["cnxmodule:SHOULDNEVERHITDB0",]
    resp = wapp_put(TESTAPP, "collection", data, rouseruri, collectionuri)
    assert resp.status_int == 403

def test_put_collection_baduser():
    data = decl.declarationdict['collection']
    data['Body'] = ["cnxmodule:SHOULDNEVERHITDB1",]
    resp = wapp_put(TESTAPP, "collection", data, rouseruri, collectionuri)
    assert resp.status_int == 403


def test_put_module():
    data = decl.declarationdict['module']
    data['Body'] = "Declaration test text"
    resp = wapp_put(TESTAPP, "module", data, gooduseruri, moduleuri)
    print resp
    assert resp.json['Body'] == "Declaration test text"

def test_put_module_rouser():
    data = decl.declarationdict['module']
    data['Body'] = "NEVER HIT DB"
    resp = wapp_put(TESTAPP, "module", data, rouseruri, moduleuri)    
    assert resp.status_int == 403

def test_put_module_baduser():
    data = decl.declarationdict['module']
    data['Body'] = "NEVER HIT DB"
    resp = wapp_put(TESTAPP, "module", data, baduseruri, moduleuri)
    print "status =", resp.status
    assert resp.status_int == 403

def test_put_folder():
    data = decl.declarationdict['folder']
    data['Body'] =  ["cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126",]
    resp = wapp_put(TESTAPP, "folder", data, gooduseruri, folderuri)
    assert len(resp.json['Body']) == 1

def test_put_folder_ro():
    data = decl.declarationdict['folder']
    data['Body'] =  ["ROUSER",]
    resp = wapp_put(TESTAPP, "folder", data, rouseruri, folderuri)
    assert resp.status_int == 403

def test_put_folder_bad():
    data = decl.declarationdict['folder']
    data['Body'] =  ["BADUSER",]
    resp = wapp_put(TESTAPP, "folder", data, baduseruri, folderuri)
    assert resp.status_int == 403

def test_put_module_acl():
    data = decl.acllist
    resp = wapp_put(TESTAPP, "module_acl", data, gooduseruri, moduleuri)
    assert resp.status_int == 200

def test_read_module_rouser():
    resp = wapp_get(TESTAPP, "module", moduleuri, rouseruri)
    assert resp.status_int == 200

def test_read_module_baduser():
    resp = wapp_get(TESTAPP, "module", moduleuri, baduseruri)
    print resp, resp.status, baduseruri
    assert resp.status_int == 403

def test_delete_module_baduser():
    resp = wapp_delete(TESTAPP, "module", moduleuri, baduseruri)
    assert resp.status_int == 403
    
def test_delete_module_rouser():
    resp = wapp_delete(TESTAPP, "module", moduleuri, rouseruri)
    assert resp.status_int == 403
    
def test_delete_module_rouser():
    resp = wapp_delete(TESTAPP, "module", moduleuri, gooduseruri)
    assert resp.status_int == 200
    
    

    
    

#import doctest
#doctest.testmod()

TESTCONFIG = None
TESTAPP = None

def setup():

    global TESTCONFIG
    global TESTAPP
    CONFD_PATH = os.path.abspath("../../testing.ini")  ##pass in through nose...
    TESTCONFIG = Configuration.from_file(CONFD_PATH)
    cleardown(TESTCONFIG)
    initdb(TESTCONFIG)    
    app = make_app(TESTCONFIG)
    app.debug=True
        
        #from waitress import serve
        #serve(app.wsgi_app, host='0.0.0.0', port=8080)

    from webtest import TestApp
    TESTAPP = TestApp(app.wsgi_app)
        

    
    
    
def cleardown(config):
    backend.clean_dbase(config)

def initdb(config):
    backend.initdb(config)
    ### kind of useless as have not instantiated the models yet.
    
#    CONFD_PATH = os.path.abspath("../../testing.ini")  ##pass in through nose...    
    
if __name__ == '__main__':

    try:
        if sys.argv[1:][0] == "doctest":
            import doctest
            doctest.testmod()
            sys.exit()
    except:
        pass
        
    c = test_post()
    c.setup()

        
#    from waitress import serve
#    serve(c.wapp, host='0.0.0.0', port=8000)
    #its a test appp!!!
    try:
        pass#r = wapp_delete(c.wapp, "module", moduleuri, gooduseruri)
    except:
        pass
    r2 = wapp_post(c.wapp, "module", decl.declarationdict['module'], 'niceguyeddie')
    print r2
#    raw_input("?")
    r = wapp_get(c.wapp, "module", moduleuri)
    print r
    print "puttting///"
    #r = wapp_put(c.wapp, {}, rouseruri, "module", id_=moduleuri)
    r = wapp_delete(c.wapp, "module", id_=moduleuri, owner=rouseruri)    



#### So we should be able to nosetests runtests.py as well as runtests.py direct