from flask import Flask, request,  url_for
import datetime
import reflector
import datetime
import md5, random
import os
import flask
import statsd
import json

from rhaptos2 import conf
from rhaptos2 import log

app = Flask(__name__)
REPO = '/tmp/repo' #conf.remote_e2repo

'''

Wanted:

onbjects to standarse the things like username lookups, username to directory, etc etc

'''

#from logging import FileHandler
#fh = FileHandler(filename=os.path.join(REPO, 'e2repo.log'))
lg = log.get_rhaptos2Logger('rhaptos2_e2repo')
app.logger.addHandler(lg)

def whoami():
    '''Not too sure how I will work this but I need a user, OpenID
  
    THis is hard coded to testuser@cnx.org'''
    return 'testuser@cnx.org'

def getfilename(modulename, REPO=REPO):
    '''find all files with this name, test.1 etc, then sort and find next highest numnber 
  
    >>> getfilename('test', REPO='/tmp')
    'test.0'
    >>> getfilename('test', REPO='/tmp')
    'test.1'

    '''
    qlog('+++++' + REPO)
    userdir = os.path.join(REPO, whoami())
    qlog(userdir)
    try:
        allfiles = [f for f in os.listdir(userdir) if 
                 os.path.splitext(os.path.basename(f))[0] == modulename]
    except OSError, IOError:
        allfiles = []
 
    if len(allfiles) == 0:
        return '%s.%s' % (modulename, 0)
    else:
        return '%s.%s' % (modulename, len(allfiles))

    
def callstatsd(dottedcounter):
    ''' '''
    c = statsd.StatsClient(conf.statsd_host, conf.statsd_port)
    c.incr(dottedcounter)
    #todo: really return c and keep elsewhere for efficieny I suspect

def qlog(msg):
    app.logger.error(msg)


def asjson(pyobj):
    '''just placeholder '''
    return json.dumps(pyobj)

def gettime():
    return datetime.datetime.today().isoformat()

def fetch_module(username, hashid):
    ''' '''
    folder = os.path.join(REPO, username)
    json = open(os.path.join(folder, str(hashid))).read()    
    return json 

def store_module(fulltext, jsondict):
    '''recieve and write to disk the json dict holding the text edtited

    '''


    myhash = getfilename(jsondict['modulename'])

    folder = whoami()
    pathtofolder = os.path.join(REPO, folder)

    qlog('******************** %s %s ' % (myhash, folder))
    newfile = os.path.join(pathtofolder, myhash)
    qlog(newfile)

    try:
        qlog('here')
        open(newfile,'w').write(fulltext)    
    except:
        #it will be far more efficient to write folder on first exception than check everytime
        os.mkdir(pathtofolder)
        app.logger.error('%s path did not exist - creating' % pathtofolder) 
        open(os.path.join(pathtofolder, str(myhash)),'w').write(fulltext)    
        
       
    return myhash

@app.route("/module/", methods=['POST'])
def modulePOST():
    app.logger.info('POST CALLED')
    callstatsd('rhaptos2.e2repo.module.POST')
    try:

        html5 = request.form['moduletxt']
        d = json.loads(html5)
        
        app.logger.info(repr(d))
                      
        myhash = store_module(html5, d)


    except Exception, e:
        qlog(repr(d))
        qlog(str(e))
        raise(e)

    s = asjson({'hashid':myhash})
    resp = flask.make_response(s)    
    resp.content_type='application/json'
    resp.headers["Access-Control-Allow-Origin"]= "*"
    return resp


@app.route("/workspace/", methods=['GET'])
def workspaceGET():
    ''' '''
    f = os.listdir(os.path.join(REPO, whoami()))
    json_dirlist = json.dumps(f)
    resp = flask.make_response(json_dirlist)    
    resp.content_type='application/json'
    resp.headers["Access-Control-Allow-Origin"]= "*"
    return resp


@app.route("/module/<mhash>", methods=['GET'])
def moduleGET(mhash):
    qlog('getcall %s' % mhash)
    try:
        jsonstr = fetch_module(whoami(), mhash)
    except Exception, e:
        raise e

    resp = flask.make_response(jsonstr)    
    resp.headers["Access-Control-Allow-Origin"]= "*"
    return resp

@app.route("/module/", methods=['DELETE'])
def moduleDELETE():
    return 'You DELETEed @ %s' %  gettime() 

@app.route("/module/", methods=['PUT'])
def modulePUT():
    return 'You PUTed @ %s' %  gettime() 


if __name__ == "__main__":
    import doctest
    doctest.testmod()
