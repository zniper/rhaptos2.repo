
import sys
from frozone import conf
from frozone.deploy import staginglib

staginglib.overwrite(conf.context, sys.argv[1:][0])
