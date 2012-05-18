

'''

'''
import socket
import time
import random

CARBON_SERVER = 'devlog.office.mikadosoftware.com'
CARBON_PORT = 2003
STATSD_PORT = 8125
STATSD_HOST = CARBON_SERVER

import statsd 

def check_statsd():

    c = statsd.StatsClient(STATSD_HOST, STATSD_PORT)
    for i in range(100):
        c.incr('frozone.statsd.verify') 

if __name__ == '__main__':
    check_statsd()
