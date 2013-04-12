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

This is the suggested method for running a WSGI Server - we instantiate the repo
app, and pass it to the waitress server (To be replaced by gunicorn)::

  python run.py --config=../../testing.ini

"""

from rhaptos2.common import runner
from rhaptos2.repo import make_app
from rhaptos2.repo.configuration import Configuration
from optparse import OptionParser
import os
from paste.urlmap import URLMap
from paste.urlparser import StaticURLParser, make_static


def main():
    """Run the application, to be used to start up one instance"""
    runner.main(make_app)


def main_2():
    """
    creates and sets up the app, *but does not run it through flask server*
    This intends to return a valid WSGI app to later be called by say gunicorn

    todo: I would like to use @pumazi approach of only importing _standalone server as needed

    """
    opts, args = parse_args()
    config = Configuration.from_file(opts.conf)
    app = make_app(config)
    app.debug = True

    if opts.devserver:
        ### Creating a mapping of URLS to file locations
        ### TODO: simplify this - proabbly need change atc and this
        s = StaticURLParser(opts.jslocation)
        s_config = StaticURLParser(os.path.join(opts.jslocation, "config"))
        s_lib = StaticURLParser(os.path.join(opts.jslocation, "lib"))
        s_bookish = StaticURLParser(os.path.join(opts.jslocation, "bookish"))
        s_helpers = StaticURLParser(os.path.join(opts.jslocation, "helpers"))
        s_node_modules = StaticURLParser(os.path.join(
            opts.jslocation, "node_modules"))
        m = {"/js/": s,
             "/js/config/": s_config,
             "/js/lib/": s_lib,
             "/js/bookish/": s_bookish,
             "/js/helpers/": s_helpers,
             "/js/node_modules/": s_node_modules}
        u = URLMap()
        for k in m:
            u[k] = m[k]  # do not kersplunk, URLMap is a dict-like obj, it may have sideeffects
        ### give repo a simple response - /api/ will get rewritten
        ### todo: can I force URLMap not to adjust PATH info etc?
        u['/'] = app.wsgi_app
    else:
        u = app.wsgi_app
    return (u, opts, args)


def wsgi_run(app, opts, args):
    """ """
    from waitress import serve
    serve(app, host=opts.host,
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
                      action="store_true", default=False,
                      help="run as devserver.")
    parser.add_option("--jslocation", dest="jslocation",
                      help="Path to config file.")

    (options, args) = parser.parse_args()
    return (options, args)


if __name__ == '__main__':
    app, opts, args = main_2()
    wsgi_run(app, opts, args)
