from flask import Flask, request,  url_for
import datetime
import reflector
import ajaxlib
import flask
import datetime

app = Flask(__name__)


def qlog(msg):
    d = gettime()
    fo = open('/tmp/e2server.log','a')
    fo.write('%s %s \n' % (d, msg))
    fo.close()


def gettime():
    return datetime.datetime.today().isoformat()

@app.route("/module/", methods=['POST'])
def modulePOST():
#    return 'You POSTed, this data: %s @ %s' %  (1, gettime()) 
    qlog('startpost')
    #get the txt, and send it on to repo for storage

    moduletxt = request.form['moduletxt']
    qlog('found ... %s' % moduletxt)

    reporesp = ajaxlib.sendajax({'moduletxt': moduletxt, 'appid': 1, 'user': 'fred', 'auth':'12345'},
                                'http://cnx1/e2repo/module/', 'POST')
    
    qlog(repr(reporesp))
     
    s =  'You POSTed, this data: %s @ %s.  \
            This was the response from repo %s' %  (reflector.dict2table(request.form), \
                                                     gettime(), reporesp) 
    resp = flask.make_response(s)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp 

@app.route("/module/", methods=['GET'])
def moduleGET():
    return 'You GETed @ %s' %  gettime() 

@app.route("/module/", methods=['DELETE'])
def moduleDELETE():
    return 'You DELETEed @ %s' %  gettime() 

@app.route("/module/", methods=['PUT'])
def modulePUT():
    return 'You PUTed @ %s' %  gettime() 


if __name__ == "__main__":
    #app.debug = True
  
    from logging import FileHandler
    fh = FileHandler(filename='/tmp/myapp.log')
    app.logger.addHandler(fh)
    app.run(host="0.0.0.0", debug=True)
