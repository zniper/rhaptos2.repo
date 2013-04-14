
"""
Not really stub - assume Dbase is there.
I need a way to verify the base calls of cbxbase etc.
fixme - remove sqlalchemy

This is rapidly becoming a doctest example set...
"""

import os
import json
import pprint
from rhaptos2.repo import backend, model
from rhaptos2.repo.tests import decl
from rhaptos2.repo.backend import db_session
from rhaptos2.common import conf

owner = decl.users['paul'].useruri
ross = decl.users['ross'].useruri


CONFD_PATH = os.path.join(".", "../../../testing.ini")
confd = conf.get_config(CONFD_PATH)
backend.initdb(confd['app'])

#### now db_session is setup and ready.



m = model.Module(creator_uuid=owner)
m.title="foobar"
m.save(db_session)
print m.userroles
m.add_userole(model.UserRoleModule, usrdict={'user_uri':ross,
                                              'role_type':'aclrw'}
                                          )
m.save(db_session)
print m.userroles
m.prep_delete_userrole(ross)
m.save(db_session)
print m.userroles


