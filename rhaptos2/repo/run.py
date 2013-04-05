#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012-13
# This software is subject to
# the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
###


"""
Launch the repo application with a standalone server.


This is the suggested method for running a WSGI Server -
we instantiate the repo app, and pass it to the waitress server
(To be replaced by gunicorn)::

  python run.py --config=../../testing.ini

"""

from rhaptos2.repo import make_app
from rhaptos2.repo.configuration import Configuration
from optparse import OptionParser


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

def main():
    """Run the application with a standalone server."""
    opts, args = parse_args()
    config = Configuration.from_file(opts.conf)
    app = make_app(config, as_standalone=True)
    app.debug = True

    from waitress import serve
    serve(app.wsgi_app, host=opts.host,
          port=opts.port
          )

if __name__ == '__main__':
    main()
