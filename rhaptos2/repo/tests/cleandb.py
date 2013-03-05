
import decl

import os, json
import pprint
from rhaptos2.repo import backend, foldermodel
from rhaptos2.repo.backend import db_session
from rhaptos2.common import conf

HERE = "/usr/home/pbrian/src/public/Connexions/rhaptos2.repo/rhaptos2/repo"
CONFD_PATH = os.path.join(HERE, "../../local.ini")
confd = conf.get_config(CONFD_PATH)



backend.clean_dbase(confd['app'])
backend.initdb(confd['app'])
