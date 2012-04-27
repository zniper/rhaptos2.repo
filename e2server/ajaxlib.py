

import httplib
import urllib
import common

def sendajax(datadict, tgturl, method='POST'):

    ''' send as ajax (json?) a payload to a tgturl, and return the response 
     
    this is a throwaway stub for a full featured library that is needed, inlcuding netowrk failure handling etc

    '''


    params = urllib.urlencode(datadict)
    # adjust headers etc.  Need finer control

    common.qlog('starting ajax client %s ' % datadict)
    dt = urllib.urlopen(tgturl, params).read()  
    common.qlog('results ajax client %s ' % dt)  
    return dt



     
if __name__ == '__main__':
    print sendajax({'moduletxt':'test'}, 'http://localhost:8002')
