import ajaxlib


reporesp = ajaxlib.sendajax({'moduletxt': 'wibble', 
                             'appid': 1, 
                             'user': 'fred', 
                             'auth':'12345'},
             'http://hadrian/e2repo/module/', 'POST')
print reporesp
