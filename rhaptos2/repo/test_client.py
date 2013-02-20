"""

This is to test the user service once it is up and running on http.
Basic test layout

1. create from decl, all modules.
2. create a folder of modules
3. create a collection of modules
4. adjust one of the modules
5. adjust one of the collections and folders
6. Test security.
7. delete all



"""
from urlparse import urljoin
import requests
import os, sys
import decl
import json
import restrest

###### config - should be replaced with generic runner?

HERE = os.path.abspath(os.path.dirname(__file__))
CONFD_PATH = os.path.join(HERE, "../../local.ini")
from rhaptos2.common.configuration import (
    find_configuration_file,
    Configuration,
    )
config = Configuration.from_file(CONFD_PATH)

#userhost=config['globals']['bamboo_global']['userserviceurl']
userhost="http://localhost:8000/"
#userhost="http://www.frozone.mikadosoftware.com/"

############################

def stage1():
    """Create all modules """
    owner = "cnxuser:1234"
    for s in ["sect1", "sect2", "sect3", "sect4", "sect5","sect6"]:
        jsond = json.dumps(decl.declarationdict[s])
        res = "module"
        test_post(res, jsond, owner)

def stage2():
    """Create all folders """
    owner = "cnxuser:1234"
    for s in ["folder",]:
        jsond = json.dumps(decl.declarationdict[s])
        res = "folder"
        test_post(res, jsond, owner)


def stage3():
    """Create all cols """
    owner = "cnxuser:1234"
    for s in ["collection",]:
        jsond = json.dumps(decl.declarationdict[s])
        res = "collection"
        test_post(res, jsond, owner)


def stage4_collection():
    owner = "cnxuser:1234"
    d = decl.declarationdict['collection']
    d['content'] = ["cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126",]
    test_put("collection", json.dumps(d), owner, d['id_'])

def stage4_module():
    owner = "cnxuser:1234"
    d = decl.declarationdict['sect1']
    d['content'] = "Dear King George, cup of tea?"
    test_put("module", json.dumps(d), owner, d['id_'])

def stage4_folder():
    owner = "cnxuser:1234"
    d = decl.declarationdict['folder']
    d['content'] = ["cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126",]
    test_put("folder", json.dumps(d), owner, d['id_'])

def get_module():
    m = "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126"
    resp = requests.get(urljoin(userhost,"module/" + m + "/"))
    capture_conversation(resp)


def setacl_collection():
    owner = "cnxuser:1234"
    acls = decl.acllist
    headers = {'X-Cnx-FakeUserId': owner,
               'content-type':'application/json'}
    resp = requests.put(urljoin(userhost, "collection/" +
                  "cnxcollection:be7790d1-9ee4-4b25-be84-30b7208f5db7" +
                  "/acl/"),
                  data=json.dumps(acls), headers=headers)
    capture_conversation(resp)
    print resp


def del_collection():
    owner = "cnxuser:1234"
    headers = {'X-Cnx-FakeUserId': owner,
              }
    resp = requests.delete(urljoin(userhost, "collection/" +
                        "cnxcollection:be7790d1-9ee4-4b25-be84-30b7208f5db7"
                        +"/"),
                        headers=headers)
    capture_conversation(resp)
    print resp

def test_post(resource, json_to_send, fake_user_id):

    headers = {'X-Cnx-FakeUserId': fake_user_id,
               'content-type':'application/json'}
    resp = requests.post(urljoin(userhost, resource + "/"), data=json_to_send,
                         headers=headers)
    capture_conversation(resp)
    print resp.text

def test_put(resource, json_to_send, fake_user_id, id_):

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

help = """SImple test client for demo

         it fires HTTP requests and we can see results on browser with GET.
         * firstly clean down dbase with python cleandb.py
         * Now python test_client.py loadmod
           view all modules
         * test_client.py loadfolder
         * test_client.py loadcollection
         * test_client.py putmodule
         * test_client.py putcollection
         * test_client.py putfolder
         * test_client.py baduser_module
         * test_client.py baduser_folder
         * test_client.py baduser_collection
         * test_client.py delete_collection
         * test_client.py delete_folder
         * test_client.py delete_module
 """
if __name__ == '__main__':
    cmd = sys.argv[1:][0]
    if cmd == "-h":
        print help
    elif cmd == "loadmod": stage1()
    elif cmd == "loadfolder": stage2()
    elif cmd == "loadcollection": stage3()
    elif cmd == "putfolder": stage4_folder()
    elif cmd == "putcollection": stage4_collection()
    elif cmd == "putmodule": stage4_module()

    elif cmd == "setacl_folder" : setacl_folder()
    elif cmd == "setacl_collection" : setacl_collection()

    elif cmd == "baduser_module": print "TBD"
    elif cmd == "baduser_folder": print "TBD"
    elif cmd == "baduser_collection": print "TBD"
    elif cmd == "delete_module": print "TBD"
    elif cmd == "delete_collection": del_collection()
    elif cmd == "delete_folder": print "TBD"

    elif cmd == "get_module": get_module()
    else: print "bad arglook here for details test_client.py -h"
