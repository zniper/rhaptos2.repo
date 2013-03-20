
import os, json
import pprint
from rhaptos2.repo import backend, model
from rhaptos2.repo.backend import db_session
from rhaptos2.common import conf

owner = "cnxuser:529d7edc-63ee-40c6-a4be-5c7a94c7ed26"



CONFD_PATH = os.path.join(".", "../../../testing.ini")
confd = conf.get_config(CONFD_PATH)
#backend.clean_dbase(confd['app'])
backend.initdb(confd['app'])
backend.clean_dbase(confd['app'])


