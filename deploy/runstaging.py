
import sys
import staginglib


import fab_lib
confd = fab_lib.get_config()

staginglib.overwrite(confd, sys.argv[1:][0])
