#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012-13
# This software is subject to
# the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
###


"""run.py - Launch the repo app.


.. todo::

   * replace mess of functions and @decorators with routes on routes
     (idea: name each route then can build route
      from name and vice versa with Routes.)

   *
"""
import decl
from rhaptos2.repo import make_app, backend, restrest
from webtest import TestApp
from wsgiproxy.app import WSGIProxyApp
from optparse import OptionParser
import urlparse


def capture_conversation(resp):
    """Need to adapt the requests specicfic capture to WebTest """
    rst = restrest.restrest(resp)
    fo = open("/tmp/output.rst", "a")
    fo.write(rst)
    fo.close()


def simplelog(r):
    fo = open("foo.log","a")
    fo.write(str(r.json))
    fo.close()

    ##FIXME - handle this problem then find out why it happens
    ## suspect \n detection in webob.
#     capture_conversation(r)
#   File "build/bdist.freebsd-9.1-RC2-amd64/egg/webob/request.py", line 1528, in readinto
#     + "(%d more bytes were expected)" % self.remaining
# DisconnectionError: The client disconnected while sending the POST/PUT body (634 more bytes were expected)


    
from rhaptos2.repo.configuration import (  # noqa
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

    # wsgi reqd keys and default valus
    wsgi_specific_headers = {"wsgi.version": (1, 0),
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

gooduseruri = decl.users['paul'].openid
rouseruri = decl.users['ed'].openid
baduseruri = decl.users['ross'].openid

userhost = "http://localhost:8000/"
### THis header is where we put the authenticated ID
HTTPHEADER_STORING_USERAUTH = "REMOTE_AUTHID"
HTTPHEADER_STORING_USERURI = "REMOTE_USERURI"
###


APIMAP = {'module':
         {"POST": urlparse.urljoin(userhost, "module/"),
          "GET": urlparse.urljoin(userhost, "module/%(id_)s"),
          "PUT": urlparse.urljoin(userhost, "module/%(id_)s"),
          "DELETE": urlparse.urljoin(userhost, "module/%(id_)s"),
          },

          'collection':
         {"POST": urlparse.urljoin(userhost, "collection/"),
          "GET": urlparse.urljoin(userhost, "collection/%(id_)s"),
          "PUT": urlparse.urljoin(userhost, "collection/%(id_)s"),
          "DELETE": urlparse.urljoin(userhost, "collection/%(id_)s"),
          },

          'folder':
         {"POST": urlparse.urljoin(userhost, "folder/"),
          "GET": urlparse.urljoin(userhost, "folder/%(id_)s"),
          "PUT": urlparse.urljoin(userhost, "folder/%(id_)s"),
          "DELETE": urlparse.urljoin(userhost, "folder/%(id_)s"),
          },

          'module_acl':
         {"POST": urlparse.urljoin(userhost, "module/%(id_)s/acl/"),
          "GET": urlparse.urljoin(userhost, "module/%(id_)s/acl/"),
          "PUT": urlparse.urljoin(userhost, "module/%(id_)s/acl/"),
          "DELETE": urlparse.urljoin(userhost, "module/%(id_)s/acl/"),
          },

          'collection_acl':
         {"POST": urlparse.urljoin(userhost, "collection/%(id_)s/acl/"),
          "GET": urlparse.urljoin(userhost, "collection/%(id_)s/acl/"),
          "PUT": urlparse.urljoin(userhost, "collection/%(id_)s/acl/"),
          "DELETE": urlparse.urljoin(userhost, "collection/%(id_)s/acl/"),
          },

          'folder_acl':
         {"POST": urlparse.urljoin(userhost, "folder/%(id_)s/"),
          "GET": urlparse.urljoin(userhost, "folder/%(id_)s/acl/"),
          "PUT": urlparse.urljoin(userhost, "folder/%(id_)s/acl/"),
          "DELETE": urlparse.urljoin(userhost, "folder/%(id_)s/acl/"),
          },

          'workspace':
         {"GET": urlparse.urljoin(userhost, "workspace/"),
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

    >>> get_url("workspace", id_=None, method="GET")
    'http://localhost:8000/workspace/'

    
    Its pretty simple api so far...

    .. todo::
       ensure urljoin is done well - urlparse version not really as expected...

    """
    # restype, id method
    ## what if invalid restype?
    baseurl = APIMAP[resourcetype][method]

    if baseurl.find("%") >= 0:
        url = baseurl % {"id_": id_}
    else:
        url = baseurl
    return url


def wapp_get(wapp, resourcetype, id_, owner, URL=None):
    """ """
    ## bit specific exceotion here todo:: fix this whole wappget approach
    if URL is None:
        headers = {HTTPHEADER_STORING_USERAUTH: owner, }
        URL = get_url(resourcetype, id_=id_, method="GET")
    else:
        headers = {HTTPHEADER_STORING_USERAUTH: owner, }
        #URL = get_url(resourcetype, id_=id_, method="GET")
        
    try:
        resp = wapp.get(URL, status="*", headers=headers)
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
    headers = {HTTPHEADER_STORING_USERAUTH: owner, }

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
    headers = {HTTPHEADER_STORING_USERAUTH: owner,
               }
    resp = wapp.delete(URL, headers=headers, status="*")
    return resp


def wapp_put(wapp, resourcetype, data, owner, id_=None):
    headers = {HTTPHEADER_STORING_USERAUTH: owner, }
    URL = get_url(resourcetype, method="PUT", id_=id_)
    print "Putting to %s" % URL
    try:
        resp = wapp.put_json(URL, params=data, headers=headers, status="*")
    except Exception, e:
        import traceback
        tb = traceback.format_exc()
        print e, tb
    return resp



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
    resp = wapp_post(TESTAPP, "module", decl.declarationdict[
                     'module'], gooduseruri)
    returned_module_uri = resp.json['id']
    assert returned_module_uri == moduleuri


def test_post_folder():
    resp = wapp_post(TESTAPP, "folder", decl.declarationdict[
                     'folder'], gooduseruri)
    returned_folder_uri = resp.json['id']
    assert returned_folder_uri == folderuri


def test_post_collection():
    resp = wapp_post(TESTAPP, "collection", decl.declarationdict[
                     'collection'], gooduseruri)
    returned_collection_uri = resp.json['id']
    assert returned_collection_uri == collectionuri


def test_put_collection():
    data = decl.declarationdict['collection_small']
    resp = wapp_put(TESTAPP, "collection", data, gooduseruri, collectionuri)
    assert resp.json['body'].find('href="cnxmodule:d3911c28') > -1
    simplelog(resp)

def test_put_collection_rouser():
    data = decl.declarationdict['collection']
    data['body'] = ["cnxmodule:SHOULDNEVERHITDB0", ]
    resp = wapp_put(TESTAPP, "collection", data, rouseruri, collectionuri)
    assert resp.status_int == 403


def test_put_collection_baduser():
    data = decl.declarationdict['collection']
    data['body'] = ["cnxmodule:SHOULDNEVERHITDB1", ]
    resp = wapp_put(TESTAPP, "collection", data, rouseruri, collectionuri)
    assert resp.status_int == 403


def test_put_module():
    data = decl.declarationdict['module']
    data['body'] = "Declaration test text"
    resp = wapp_put(TESTAPP, "module", data, gooduseruri, moduleuri)
    assert resp.json['body'] == "Declaration test text"


def test_dateModifiedStamp():
    data = decl.declarationdict['module']
    data['body'] = "Declaration test text"
    resp = wapp_put(TESTAPP, "module", data, gooduseruri, moduleuri)
    assert resp.json['dateLastModifiedUTC'] != resp.json['dateCreatedUTC']
    
def test_put_module_rouser():
    data = decl.declarationdict['module']
    data['body'] = "NEVER HIT DB"
    resp = wapp_put(TESTAPP, "module", data, rouseruri, moduleuri)
    assert resp.status_int == 403


def test_put_module_baduser():
    data = decl.declarationdict['module']
    data['body'] = "NEVER HIT DB"
    resp = wapp_put(TESTAPP, "module", data, baduseruri, moduleuri)
    print "status =", resp.status
    assert resp.status_int == 403


def test_put_folder():
    data = decl.declarationdict['folder']
    data['body'] = ["cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126", ]
    resp = wapp_put(TESTAPP, "folder", data, gooduseruri, folderuri)
    assert len(resp.json['body']) == 1


def test_put_folder_ro():
    data = decl.declarationdict['folder']
    data['body'] = ["ROUSER", ]
    resp = wapp_put(TESTAPP, "folder", data, rouseruri, folderuri)
    assert resp.status_int == 403


def test_put_folder_bad():
    data = decl.declarationdict['folder']
    data['body'] = ["BADUSER", ]
    resp = wapp_put(TESTAPP, "folder", data, baduseruri, folderuri)
    assert resp.status_int == 403


def test_put_module_acl():
    data = decl.acllist
    resp = wapp_put(TESTAPP, "module_acl", data, gooduseruri, moduleuri)
    assert resp.status_int == 200


def test_read_module_rouser():
    resp = wapp_get(TESTAPP, "module", moduleuri, rouseruri)
    assert resp.status_int == 200

def test_read_folder_gooduser():
    resp = wapp_get(TESTAPP, "folder", folderuri, gooduseruri)
    assert resp.status_int == 200
    simplelog(resp)
    
    

def test_read_module_baduser():
    resp = wapp_get(TESTAPP, "module", moduleuri, baduseruri)
    print resp, resp.status, baduseruri
    assert resp.status_int == 403
    
    
def test_get_workspace_good():
    resp = wapp_get(TESTAPP, "workspace", None, gooduseruri)
    print resp
    print resp.json
    assert len(resp.json) == 3   
    assert resp.status_int == 200
    simplelog(resp)
    
    
###############    

def test_delete_module_baduser():
    resp = wapp_delete(TESTAPP, "module", moduleuri, baduseruri)
    assert resp.status_int == 403


def test_delete_module_rouser():
    resp = wapp_delete(TESTAPP, "module", moduleuri, rouseruri)
    assert resp.status_int == 403

def test_delete_module_good():
    resp = wapp_delete(TESTAPP, "module", moduleuri, gooduseruri)
    assert resp.status_int == 200

###
    
def test_delete_collection_baduser():
    resp = wapp_delete(TESTAPP, "collection", collectionuri, baduseruri)
    assert resp.status_int == 403


def test_delete_collection_rouser():
    resp = wapp_delete(TESTAPP, "collection", collectionuri, rouseruri)
    assert resp.status_int == 403


def test_delete_collection_good():
    resp = wapp_delete(TESTAPP, "collection", collectionuri, gooduseruri)
    assert resp.status_int == 200

###
    
def test_delete_folder_baduser():
    resp = wapp_delete(TESTAPP, "folder", folderuri, baduseruri)
    assert resp.status_int == 403


def test_delete_folder_rouser():
    resp = wapp_delete(TESTAPP, "folder", folderuri, rouseruri)
    assert resp.status_int == 403


def test_delete_folder_good():
    resp = wapp_delete(TESTAPP, "folder", folderuri, gooduseruri)
    assert resp.status_int == 200

def test_whoami():
    resp = wapp_get(TESTAPP, "-", None,
                    "https://paulbrian.myopenid.com",
                    URL="http://localhost:8000/me/"
    )
    assert resp.status_int == 200
    assert resp.json["name"] == "Paul Brian" 
    assert resp.json["id"] == "cnxuser:75e06194-baee-4395-8e1a-566b656f6920" 

    ########################################################################

TESTCONFIG = None
TESTAPP = None


def convert_config(config):
    defaultsection = 'app'
    for k in config[defaultsection]:
        config[k] = config[defaultsection][k]
    del config[defaultsection]
    return config


def setup():
    global TESTCONFIG
    global TESTAPP

    # using nose-testconfig we obtain the config dict passed in through the
    # nosetests command line
    from testconfig import config
    ## now "convert" to app-style dict
    TESTCONFIG = convert_config(config)

    if 'HTTPPROXY' in config.keys():
        app = WSGIProxyApp(config['HTTPPROXY'])
        TESTAPP = TestApp(app, extra_environ={'REMOTE_ADDR': '1.2.3.4'})
    else:
        app = make_app(TESTCONFIG)
        app.debug = True
        TESTAPP = TestApp(app.wsgi_app)


    print "Running setup"
    print "cookies", TESTAPP.cookies 

def cleardown(config):
    backend.clean_dbase(config)


def initdb(config):
    backend.initdb(config)
    ### kind of useless as have not instantiated the models yet.


if __name__ == '__main__':
    import doctest
    doctest.testmod()

