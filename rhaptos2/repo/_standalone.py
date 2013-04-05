#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012-13
# This software is subject to
# the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
###
"""Static assets that are normally only imported in a standalone server
situation.

"""
import os
from flask import g, send_from_directory
from rhaptos2.repo import get_app, dolog


app = get_app()


@app.route('/')
def index():
    dolog("INFO", "This is request %s" % g.requestid)
    directory = os.path.join(app.config["aloha_staging_dir"], 'test')
    return send_from_directory(directory, 'test-atc.html')

@app.route("/atc.js")
def serve_atc_js():
    filename = 'atc.js'
    directory = os.path.join(app.config["aloha_staging_dir"])
    filepath = os.path.join(directory, filename)
    dolog("INFO", filepath)
    return send_from_directory(directory, filename)

@app.route("/atc-nav-serialize.hbs")
def serve_atc_nav_serialize_hbs():
    filename = 'atc-nav-serialize.hbs'
    directory = os.path.join(app.config["aloha_staging_dir"])
    filepath = os.path.join(directory, filename)
    dolog("INFO", filepath)
    return send_from_directory(directory, filename)

@app.route("/bookish.css")
def serve_bookish_css():
    filename = 'bookish.css'
    directory = os.path.join(app.config["aloha_staging_dir"])
    filepath = os.path.join(directory, filename)
    dolog("INFO", filepath)
    return send_from_directory(directory, filename)

@app.route("/lib/<path:filename>")
def serve_libs(filename):
    directory = os.path.join(app.config["aloha_staging_dir"], 'lib')
    filepath = os.path.join(directory, filename)
    dolog("INFO", filepath)
    return send_from_directory(directory, filename)


@app.route("/config/<path:filename>/")
def serve_config(filename):
    directory = os.path.join(app.config["aloha_staging_dir"], 'config')
    filepath = os.path.join(directory, filename)
    dolog("INFO", filepath)
    return send_from_directory(directory, filename)

@app.route("/bookish/<path:filename>/")
def serve_bookish(filename):
    directory = os.path.join(app.config["aloha_staging_dir"], 'bookish')
    filepath = os.path.join(directory, filename)
    dolog("INFO", filepath)
    return send_from_directory(directory, filename)

@app.route("/node_modules/<path:filename>/")
def serve_node_modules(filename):
    directory = os.path.join(app.config["aloha_staging_dir"], 'node_modules')
    filepath = os.path.join(directory, filename)
    dolog("INFO", filepath)
    return send_from_directory(directory, filename)

@app.route("/helpers/<path:filename>/")
def serve_node_modules(filename):
    directory = os.path.join(app.config["aloha_staging_dir"], 'helpers')
    filepath = os.path.join(directory, filename)
    dolog("INFO", filepath)
    return send_from_directory(directory, filename)
