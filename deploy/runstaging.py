
import sys
import staginglib


import fab_lib
confd = fab_lib.get_config()

print confd.keys()
staginglib.overwrite(confd, sys.argv[1:][0])
