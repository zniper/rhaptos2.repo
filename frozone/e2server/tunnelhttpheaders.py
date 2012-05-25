#!/usr/local/bin/python

'''
We want to 'tunnel' non GET/POST request methods into WSGI for handling 
as if the requests were really sent as DELETE.

Background
----------

HTTP protocol can accept many methods - GET POST PUT DELETE (see `here <http://en.\
wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods>`_).

However almost all browsers will only use GET and POST when dealing with interactive HTML forms.  There is a sort of reasonable argument that no-one has a clear idea how to represent DELETE in a textarea.  But frankly its weak.

Anyway, if we use AJAX, we use XmlHttpRequest - which is well supported by all major browsers, and will do PUT and DELETE and OPTIONS and HEAD.  basically we can use JQuery to send DELETE, but not a web form.

And TinyMCE is a web form.

So as a hedge, I have got a wsgi middleware that will look for a trigger
element in the form, and then replace the POST method in the CGI environ variables with
the methid in the trigger - ie. we POST a form that says trigger=DELETE and then
this before any new processing is done, flips the environ to be DELETE.


'''

from flask import Flask, request,  url_for
import datetime
import tmpl
from werkzeug.exceptions import BadRequestKeyError


#test out app middleware based on rewriting method call

from werkzeug import Request

class MethodRewriteMiddleware(object):

    def __init__(self, app):
        self.app = app


    def __call__(self, environ, start_response):
        request = Request(environ)

        try:
            method = request.form['methodtrigger'].upper()

            if method in ['GET', 'POST', 'PUT', 'DELETE']:
                environ['REQUEST_METHOD'] = method
            else:
                flask.abort(405) #405 - method not supported.
        except BadRequestKeyError:
            pass #this will hit almost everytime.  Heavy load for rubbish tunnelling.

    
        return self.app(environ, start_response)

app = Flask(__name__)
app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)



@app.route("/")
def hello():

    return tmpl.simpleform



@app.route('/seeall')
def seeall():
    s = '<h2>%s</h2>' % datetime.datetime.today().strftime('%d%m%Y - %H%M%S')
    for hdrtype in request.headers:
        s += repr(hdrtype)
    return s 

if __name__ == "__main__":

    app.debug = True
    app.run(host='0.0.0.0', port=5000)
