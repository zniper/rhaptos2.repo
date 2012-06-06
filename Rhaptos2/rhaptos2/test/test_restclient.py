

from rhaptos2.client import restclient

def test_create_module():
    modlist = restclient.getworkspace_module_list('http://www.office.mikadosoftware.com')

    print restclient.create_module('http://www.office.mikadosoftware.com', 
                        'testmod', 'test content')
    modlist2 = restclient.getworkspace_module_list('http://www.office.mikadosoftware.com')

    if len(modlist2) > len(modlist):
        return True
    else:
        return False
    


def test_create_module_text():
     content='xxddffgg'
     saved_file_name = restclient.create_module('http://www.office.mikadosoftware.com', 
                        'testmod', content)
     print saved_file_name
     txt = restclient.get_module_text('http://www.office.mikadosoftware.com', 
                           saved_file_name)
     if txt.find(content)>=0:
         return True
     else: 
         return False

if __name__ == '__main__':
    test_create_module_text()
