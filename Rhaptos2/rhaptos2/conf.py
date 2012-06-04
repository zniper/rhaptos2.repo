############################# Get config                                                   
import ConfigParser

def get_config():

    parser = ConfigParser.SafeConfigParser()
    parser.read('/usr/local/etc/rhaptos2/frozone.ini')
    globaldict = dict(parser.items('frozone'))
    return globaldict
