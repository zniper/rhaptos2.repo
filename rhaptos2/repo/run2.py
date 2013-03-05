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

from rhaptos2.repo.configuration import (
    find_configuration_file,
    Configuration,
    )


###### CONSTANTS

moduleuri = "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126"
collectionuri = "cnxcollection:be7790d1-9ee4-4b25-be84-30b7208f5db7"
folderuri = "cnxfolder:c192bcaf-669a-44c5-b799-96ae00ef4707"
gooduseruri = "cnxuser:1234"
userhost="http://localhost:8000/"

###



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







def stage1(wapp):
    """Create all modules """
    owner = gooduseruri
    for s in ["sect1",]:# "sect2", "sect3", "sect4", "sect5","sect6"]:
        jsond = json.dumps(decl.declarationdict[s])
        data = decl.declarationdict[s]
        data['id_'] = None
        url = userhost + "module" + "/"
        wapp_post(wapp, url, data, owner)

def wapp_post(wapp, url, data, owner):
    headers = {'X-Cnx-FakeUserId': owner,}
#    fo  = open("/tmp/errlog", 'w')
#    from webtest.debugapp import debug_app
#    wapp = webtest.TestApp(debug_app)
    try:
        resp = wapp.post_json(url, params=data, headers=headers)
#                          extra_environ={'wsgi.errors': fo}
    except Exception, e:
        import traceback
        tb = traceback.format_exc()
        print e, tb
    print resp.body

    
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
    


    
    
if __name__ == '__main__':

    opts, args = parse_args()
    CONFD_PATH = opts.conf
    print opts
    
#    confd = conf.get_config(CONFD_PATH)
    config = Configuration.from_file(CONFD_PATH)

    app = make_app(config)
    app.debug=True
    #from waitress import serve
    #serve(app.wsgi_app, host='0.0.0.0', port=8080)

    from webtest import TestApp
    wapp = TestApp(app.wsgi_app)
    
    stage1(wapp)    
    