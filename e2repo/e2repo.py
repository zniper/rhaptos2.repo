from flask import Flask, request,  url_for
import datetime
import reflector

app = Flask(__name__)

def qlog(msg):
    fo = open('q.log','a')
    fo.write(msg + "\n")
    fo.close()


def gettime():
    return datetime.datetime.today().isoformat()

@app.route("/module/", methods=['POST'])
def modulePOST():
    qlog('postcall')
    app.logger.info('test')
    importantbit = request.form['moduletxt']
    open('/tmp/654321','w').write(importantbit)
    return 'repo response: new module txt of %s saved id: 654321' % importantbit  

@app.route("/module/<modulehash>", methods=['GET'])
def moduleGET(modulehash):
    qlog('getcall')
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
