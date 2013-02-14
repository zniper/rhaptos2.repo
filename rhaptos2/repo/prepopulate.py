#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012
# This software is subject to
# the provisions of the GNU Lesser General
# Public License Version 2.1 (LGPL).
# See LICENCE.txt for details.
###

"""
dbtest=> drop table CNXfolder cascade;
NOTICE:  drop cascades to constraint userrole_folder_folder_uuid_fkey on table userrole_folder
DROP TABLE
dbtest=> drop table userrole_folder cascade;
DROP TABLE
dbtest=>


"""


import decl
import os
import pprint
from rhaptos2.repo import backend, foldermodel2 as foldermodel
from rhaptos2.repo.backend import db_session
from rhaptos2.common import conf

HERE = os.path.abspath(os.path.dirname(__file__))
CONFD_PATH = os.path.join(HERE, "../../local.ini")
confd = conf.get_config(CONFD_PATH)

pprint.pprint(confd['app'])
backend.initdb(confd['app'])

print "Running simple prepopulation of database as connected by:"
print confd['app']

owner = "Testuser1"
incomingjsond = {'date_lastmodified_utc': None,
                      'title': u'Test Rhaptos folder',
                      'date_created_utc': None,
                      'contentjson': u'{some otehr json}' }

aclsd = [
        {'date_lastmodified_utc': None,
         'date_created_utc': None,
       'user_uuid': u'Testuser1',
      'role_type': 'aclrw'},
        {'date_lastmodified_utc': None,
        'date_created_utc': None,
      'user_uuid': u'testuser2',
      'role_type': 'aclrw'}
       ]


f2 = foldermodel.Folder(creator_uuid=owner)
foldermodel.populate_folder(incomingjsond, f2)
print f2.userroles

#>>> f2.set_acls(f2.folderid, aclsd)
#>>> print f2.userroles
#>>> db_session.add(f2)
#>>> db_session.commit()
