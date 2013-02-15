

"""

This is to test the user service once it is up and running on http.


"""
from urlparse import urljoin
import requests
import os
import decl
import json

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
############################


def test_viewall():
    r = requests.get(urljoin(userhost, "folder/"))
    d = r.json
    assert len(d) > 0


EXAMPLEFOLDERID = "102c7a02-fb4f-48de-bbf0-28e16d6dad3c"
def test_get_known_folderid():
    r = requests.get(urljoin(userhost,
                     "folder/"+ EXAMPLEFOLDERID))
    d = r.json
    assert d['title'] == u'Test Rhaptos folder'


incomingjsond = {'date_lastmodified_utc': None,
 'title': u'Test Rhaptos folder',
 'date_created_utc': None,
 'contentjson': json.dumps(decl.declarationdict['folder']) }

def test_post():
    payload = json.dumps(incomingjsond)
    headers = {'X-Cnx-FakeUserId': 'fgfgfgf',
               'content-type':'application/json'}
    resp = requests.post(urljoin(userhost, "folder/"), data=payload,
                         headers=headers)
    print resp.text

def test_put():
    global incomingjsond
    incomingjsond['title'] = "New Name!"
    incomingjsond = {'rrrr':3}
    payload = json.dumps(incomingjsond)
    headers = {'X-Cnx-FakeUserId': 'fgfgfgf',
               'content-type':'application/json'}
    folderid = "c192bcaf-669a-44c5-b799-96ae00ef4707"
    resp = requests.put(urljoin(userhost, "folder/"+folderid+"/"),
                        data=payload,
                        headers=headers)
    print resp.text


    # requests.put(urljoin(userhost,
    #              "user/org.cnx.user-75e06194-baee-4395-8e1a-566b656f6920"))
    # r = requests.get(urljoin(userhost,
    #                  "openid/?user=https://paulbrian.myopenid.com"))
    # d = r.json
    # assert d['fullname'] == 'testput-fullname'


#test_post()
test_put()
