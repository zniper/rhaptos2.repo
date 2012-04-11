#!/usr/local/bin/python

'''
Just playground stuff

'''

from flask import Flask, request,  url_for
import datetime

app = Flask(__name__)

#test out app middleware based on rewriting method call

from werkzeug import Request

class MethodRewriteMiddleware(object):

    def __init__(self, app):
        self.app = app


    def __call__(self, environ, start_response):
        request = Request(environ)

#        method = request.form['foo'].upper()

#        if method in ['GET', 'POST', 'PUT', 'DELETE']:
#            environ['REQUEST_METHOD'] = method
        environ['REQUEST_METHOD'] = 'GET'
    
        return self.app(environ, start_response)

app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)


@app.route("/")
def hello():
    return "Hello World!" + datetime.datetime.today().strftime('%d%m%Y - %H%M%S') + repr(request.headers) 




if __name__ == "__main__":
    app.debug = True
    app.run()
