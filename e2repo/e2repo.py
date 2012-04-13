from flask import Flask, request,  url_for
import datetime
import reflector

app = Flask(__name__)

def gettime():
    return datetime.datetime.today().isoformat()

@app.route("/module/", methods=['POST'])
def modulePOST():
#    return 'You POSTed, this data: %s @ %s' %  (1, gettime()) 
    app.logger.info('test')
    return 'You POSTed, this data: %s @ %s' %  (reflector.dict2table(request.form), gettime()) 

@app.route("/module/<modulehash>", methods=['GET', 'POST'])
def moduleGET(modulehash):
    return 'this is text of %s.' % modulehash    

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
