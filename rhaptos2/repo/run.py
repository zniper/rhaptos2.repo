#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""run.py - Launch the repo app.

Author: Paul Brian
(C) 2012 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
import os
from optparse import OptionParser
from flask import Flask
from rhaptos2.repo import APPTYPE, app, set_logger
from rhaptos2.common import conf


# def make_app(settings):
#     """Application factory function"""
#     app = Flask('rhaptos2.repo')
#     app.config.update(settings)
#     set_app(app)
#     #newapp = get_app()
#     # basically we want a pointer to the _app global stored in __init__
#     # this is now newapp.  WHilst we are passing in same object, 
#     # Import the views to initialize them
#     import rhaptos2.repo.views
#     return app

def parse_args():
    parser = OptionParser()
    parser.add_option("--host", dest="host",
                      help="hostname to listen on")
    parser.add_option("--port", dest="port",
                      help="port to listen on", type="int")
    parser.add_option("--debug", dest="debug", action="store_true",
                      help="debug on.", default=False)

    (options, args) = parser.parse_args()
    return (options, args)

def main():
    """Run the application, to be used to start up one instance"""
    opts, args = parse_args()
    #todo: Some validation here??

    if opts.debug:
        s = '########### ENV VARS WE START UP WITH HERE\n'
        for k in os.environ: s += '\n%s:%s' % (k, os.environ[k])
        s += '\n########### ENV VARS END'
        print(s)

##done in __init__
#    confd = conf.get_config(APPTYPE)
#    app = make_app(confd)
#    set_logger(APPTYPE, app.config)

    # NOTE Do not use module reloading, even in debug mode, because it
    #      produces new stray processes that supervisor does not ctl.
    app.run(host=opts.host,
            port=opts.port,
            debug=opts.debug,
            use_reloader=False
            )


if __name__ == '__main__':
    main()
