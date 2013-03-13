#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""run.py - Launch the repo app.

Author: Paul Brian
(C) 2012 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from rhaptos2.common import runner
from rhaptos2.repo import make_app
from rhaptos2.repo.configuration import (
    find_configuration_file,
    Configuration,
    )
from optparse import OptionParser

def main():
    """Run the application, to be used to start up one instance"""
    runner.main(make_app)

def main_2():
    opts, args = parse_args()
    config = Configuration.from_file(opts.conf)
    app = make_app(config)
    app.debug=True

    from waitress import serve
    serve(app.wsgi_app, host=opts.host,
                        port=opts.port
                        )
    
#    app.run(host=opts.host,
#            port=opts.port,
#            debug=opts.debug,
#            use_reloader=False
#            )

def parse_args():
    parser = OptionParser()
    parser.add_option("--host", dest="host",
                      default="0.0.0.0",
                      help="hostname to listen on")
    parser.add_option("--port", dest="port",
                      default="8000",
                      help="port to listen on", type="int")
    parser.add_option("--debug", dest="debug", action="store_true",
                      help="debug on.", default=False)

    parser.add_option("--config", dest="conf",
                      help="Path to config file.")

    (options, args) = parser.parse_args()
    return (options, args)

def mainold():
    """Run the application, to be used to start up one instance"""
    opts, args = parse_args()

    confd = conf.get_config(opts.conf)
    app = make_app(confd)
    set_logger(APPTYPE, app.config)
    print app, "<-- Intialised app"

    # NOTE Do not use module reloading, even in debug mode, because it
    #      produces new stray processes that supervisor does not ctl.
    app.run(host=opts.host,
            port=opts.port,
            debug=opts.debug,
            use_reloader=False
            )


if __name__ == '__main__':
    main_2()
