from flask import Flask, make_response, request, abort
from webob import Request, Response
from waitress import serve
from paste.auth import open_id
import paste.urlmap
import pprint

app = Flask("test")

def htmlpprint(obj):
     s = pprint.pformat(obj)
     s = s.replace("\n", "<br/>")
     return s

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path):
    r = make_response("hi" + path + ":::::::" +  htmlpprint(request.environ))
    return r


    
### vaguely useful profiling info.    
#import paste.debug.profile
#wsgi_app = paste.debug.profile.make_profile_middleware(app.wsgi_app, {})

m = paste.urlmap.URLMap()

m['/api/'] = app.wsgi_app
serve(m,host="0.0.0.0",port=8000)  