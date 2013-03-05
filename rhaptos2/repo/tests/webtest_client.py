
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

HERE = os.path.abspath(os.path.dirname(__file__))
CONFD_PATH = os.path.join(HERE, "../../pbrian.ini")
confd = conf.get_config(CONFD_PATH)

from rhaptos2.repo.configuration import (
    find_configuration_file,
    Configuration,
    )

config = Configuration.from_file(CONFD_PATH)


### wrap make app up
#userhost=config['globals']['bamboo_global']['userserviceurl']
userhost="http://localhost:8000/"
#userhost="http://www.frozone.mikadosoftware.com/"

############################

###### CONSTANTS

moduleuri = "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126"
collectionuri = "cnxcollection:be7790d1-9ee4-4b25-be84-30b7208f5db7"
folderuri = "cnxfolder:c192bcaf-669a-44c5-b799-96ae00ef4707"
gooduseruri = "cnxuser:1234"

def stage1(wapp):
    """Create all modules """
    owner = gooduseruri
    for s in ["sect1",]:# "sect2", "sect3", "sect4", "sect5","sect6"]:
        jsond = json.dumps(decl.declarationdict[s])
        data = decl.declarationdict[s]
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
        
if __name__ == '__main__':
    app = make_app(config)
    app.debug=True
    print app.wsgi_app
    #from waitress import serve
    #serve(app.wsgi_app, host='0.0.0.0', port=8080)


    wapp = TestApp(app.wsgi_app)
    stage1(wapp)