

import httplib
import urllib


def sendajax(datadict, tgturl, method='POST'):

    ''' send as ajax (json?) a payload to a tgturl, and return the response 
     
    this is a throwaway stub for a full featured library that is needed, inlcuding netowrk failure handling etc

    '''

    params = urllib.urlencode(datadict)
    # adjust headers etc.  Need finer control
    dt = urllib.urlopen(tgturl, params).read()  



    return dt


     
