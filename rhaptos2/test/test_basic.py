

import rhaptos2


def test_canimport():
    try:
        f = rhaptos2.__file__ 
        return True
    except:
        return False


