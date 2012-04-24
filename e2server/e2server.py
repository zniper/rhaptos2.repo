from flask import Flask, request,  url_for
import datetime
import reflector
import ajaxlib

app = Flask(__name__)

def gettime():
    return datetime.datetime.today().isoformat()

@app.route("/module/", methods=['POST'])
def modulePOST():
#    return 'You POSTed, this data: %s @ %s' %  (1, gettime()) 
    app.logger.info('test')
    #get the txt, and send it on to repo for storage
    moduletxt = request.form['moduletxt']
    reporesp = ajaxlib.sendajax({'moduletxt': moduletxt, 'appid': 1, 'user': 'fred', 'auth':'12345'},
                                'http://e2repo.office.mikadosoftware.com/e2repo/module/', 'POST')
    
    return 'You POSTed, this data: %s @ %s.  \
            This was the response from repo %s' %  (reflector.dict2table(request.form), \
                                                     gettime(), reporesp) 

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
    app.run()
