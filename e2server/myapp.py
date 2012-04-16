from flask import Flask, request,  url_for
import datetime

app = Flask(__name__)

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return 'Hello World'


