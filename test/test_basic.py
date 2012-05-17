

import frozone


def test_canimport():
    try:
        f = frozone.__file__ 
        return True
    except:
        return False


