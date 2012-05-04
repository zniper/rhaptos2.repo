

'''

'''
import socket
import time
import random

CARBON_SERVER = 'cnx4.office.mikadosoftware.com'
CARBON_PORT = 2003
STATSD_PORT = 8125
STATSD_HOST = CARBON_SERVER

def check_graphite():
    ''' '''
    sock = socket.socket()
    try:
        sock.connect( (CARBON_SERVER,CARBON_PORT) )
    except Exception, e:
        print 'could not connect on %s %s' % (CARBON_SERVER,CARBON_PORT)
        raise e
    metric = 'frozone.foo.bar'
    val = 1

    for i in range(1000):
        if val % 2 == 0:
            mval = 1
        else:
            mval = 2
        now = int( time.time() )
        cmd = '\n%s %s %s\n' % (metric, mval, now)
        sock.sendall(cmd)
        time.sleep(1)
        val += 1


import statsd 

def check_statsd():

    c = statsd.StatsClient(STATSD_HOST, STATSD_PORT)
    for i in range(1000):
        c.incr('frozone.statsd.test') 

if __name__ == '__main__':
#    check_graphite()
    check_statsd()
