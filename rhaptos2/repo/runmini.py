from flask import Flask, make_response, request, abort
from webob import Request, Response
from waitress import serve
from paste.auth import open_id
import paste.urlmap
import pprint
import restrest
from webtest import TestApp

app = Flask("test")

def htmlpprint(obj):
     s = pprint.pformat(obj)
     s = s.replace("\n", "<br/>")
     return s

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path):
    longstr = "0"*10024
    r = make_response(path + ":::::::" +  htmlpprint(request.environ)+longstr)
    return r


    
### vaguely useful profiling info.    
#import paste.debug.profile
#wsgi_app = paste.debug.profile.make_profile_middleware(app.wsgi_app, {})

m = paste.urlmap.URLMap()

m['/api/'] = app.wsgi_app
TESTAPP = TestApp(m)
resp = TESTAPP.get('/api/')

print restrest.restrest(resp)
#serve(m,host="0.0.0.0",port=8000)  