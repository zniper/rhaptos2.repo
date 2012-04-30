import datetime

def qlog(msg):
    d = datetime.datetime.today().isoformat()
    fo = open('/tmp/e2server.log','a')
    fo.write('%s %s \n'% (d, msg))
    fo.close()

