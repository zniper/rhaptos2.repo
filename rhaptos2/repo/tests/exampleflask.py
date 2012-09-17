#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###  
# Copyright (c) Rice University 2012
# This software is subject to
# the provisions of the GNU Lesser General
# Public License Version 2.1 (LGPL).
# See LICENCE.txt for details.
###


from flask import Flask
import flask
import json

app = Flask(__name__)

@app.route("/")
def hello():
    jsontxt = json.dumps({"msg":"hello world"})
    resp = flask.make_response(jsontxt)
    resp.content_type='application/json'
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5005)
