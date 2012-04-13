from flask import Flask, request,  url_for, make_response
import flask
import datetime
import copy
import random

app = Flask(__name__)


def dict2table(d):

    s = '<table>'
    row = '<tr>%s</tr>'
    for k in d:
        s += row % '<td>%s</td><td>%s</td>' % (k, d[k])
    return s + '</table>'

def obj2table(obj):
    '''use getattr() and getitem and dir to nab as much as possible.  be brutal at first '''
    l = [attr for attr in dir(obj) if attr.find('__') != 0]
    s = 'breakdown of the request object,  want to make this more searchable link to docs etc<table>'
    row = '<tr>%s</tr>'

    for attr in l:
        s += row % '<td>%s</td><td>%s</td>' % (attr, getattr(obj, attr))


    return s + '</table>'


def obj2table(obj):
    '''use getattr() and getitem and dir to nab as much as possible.  be brutal at first '''
    l = [attr for attr in dir(obj) if attr.find('__') != 0]
    s = ''
    row = '%s'

    for attr in l:
        s += row % '%s::%s\n' % (attr, getattr(obj, attr))


    return s


@app.route("/simple")
def simple():
    print 'somple'
    s = '<html><body>Hello world</body></html>'
    r = flask.make_response(s)
    print obj2table(r)
    return r


@app.route("/reflect")
def hello():
    print 'got here'
    s =  "<h2>%s</h2>" % datetime.datetime.today().strftime('%d%m%Y - %H%M%S') 
    s += obj2table(request)
    
    return s



@app.route("/reflect2", methods=['POST', 'GET'])
def hello2():
    print 'got here2'
    print request.args
    print request.form
    s =  '''<ratings><average>%s</average><count>1234567</count></ratings>''' % random.randint(1,100)
    resp = flask.make_response(s)
    #resp.headers["Content-Type"] = "text/xml"

    return resp



if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
