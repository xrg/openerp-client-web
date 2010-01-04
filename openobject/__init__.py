import os
import sys
from locale import getlocale

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib')
if os.path.exists(libdir) and libdir not in sys.path:
    sys.path.insert(0, libdir)

del os
del sys
del libdir


def ustr(value):
    """This method is similar to the builtin `str` method, except
    it will return Unicode string.

    @param value: the value to convert

    @rtype: unicode
    @return: unicode string
    """

    if isinstance(value, unicode):
        return value
    
    try: # first try without encoding
        return unicode(value)
    except:
        pass
    
    try: # then try with utf-8
        return unicode(value, 'utf-8')
    except:
        pass

    try: # then try with extened iso-8858
        return unicode(value, 'iso-8859-15')
    except:
        pass

    # else use default system locale
    return unicode(value, getlocale()[1])

__builtins__['ustr'] = ustr

import i18n
i18n.install()


# vim: ts=4 sts=4 sw=4 si et

