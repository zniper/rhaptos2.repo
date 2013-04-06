#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012-13
# This software is subject to
# the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
###


"""run.py - Launch the repo app.

Author: Paul Brian
(C) 2012 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.


run.py
------

This is the suggested method for running a WSGI Server -
we instantiate the repo app, and pass it to the waitress server
(To be replaced by gunicorn)::

  python run.py --config=../../testing.ini

"""

from rhaptos2.common import runner
from rhaptos2.repo import make_app
from rhaptos2.repo.configuration import Configuration
from optparse import OptionParser

from paste.urlmap import URLMap
from paste.urlparser import StaticURLParser, make_static

def main():
    """Run the application, to be used to start up one instance"""
    runner.main(make_app)


def main_2():
    
    opts, args = parse_args()
    config = Configuration.from_file(opts.conf)
    app = make_app(config)
    app.debug = True

    if opts.devserver:
        s = StaticURLParser(opts.jslocation)
        u = URLMap()
        u['/js/'] = s
        u['/api/'] = app.wsgi_app
    else:
        u = app.wsgi_app
        
    from waitress import serve
    serve(u, host=opts.host,
          port=opts.port
          )


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

    parser.add_option("--devserver", dest="devserver",
                      action=store_true, default=False,
                      help="run as devserver.")
    parser.add_option("--jslocation", dest="jslocation",
                      help="Path to config file.")


    
    (options, args) = parser.parse_args()
    return (options, args)


if __name__ == '__main__':
    main_2()
