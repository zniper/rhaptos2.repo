#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012
# This software is subject to
# the provisions of the GNU Lesser General
# Public License Version 2.1 (LGPL).
# See LICENCE.txt for details.
###

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

f = foldermodel.Folder()
f.title="Test Rhaptos folder"
f.contentjson = "{some json}"
usr = foldermodel.UserRole()
usr.folder_uuid = f.folderid
usr.user_uuid = "fleffefble-rrrrfff"
usr.role_type = "author"

f.userroles = [usr,]
# i.identifiertype = 'openid'
# i.user_id = u.user_id
# u.identifiers=[i,]

# db_session.add(u)
# db_session.commit()
