#!/usr/local/bin/python
#! -*- coding: utf-8 -*-

'''
Just launch the main Flask repo app.

'''

from optparse import OptionParser
from rhaptos2.repo import e2repo
from rhaptos2 import conf


def parse_args():

    parser = OptionParser()
    parser.add_option("--host", dest="host",
                      help="hostname to listen on")

    parser.add_option("--port", dest="port",
                      help="port to listen on", type="int")

    parser.add_option("--debug", dest="debug",
                      help="debug on or off.", default=False)


    (options, args) = parser.parse_args()
    return (options, args)

def main():
    '''run the main Flask application, to be used to start up one instance

    
    '''
    opts, args = parse_args()
    #todo: Some validation here??

    e2repo.app.run(host=opts.host, 
                   port=opts.port, 
                   debug=opts.debug,
                   use_reloader=False 
                   )#do not reload even in debug mode - produces new stray processes that supervisor does not ctl.

    

if __name__ == '__main__':
    main()


