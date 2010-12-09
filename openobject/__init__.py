import os
import sys
from locale import getlocale

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib')
if os.path.exists(libdir) and libdir not in sys.path:
    sys.path.insert(0, libdir)

import cherrypy
import controllers._root
import openobject

__all__ = ['ustr', 'application', 'configure', 'enable_static_paths',
           'WSGI_STATIC_PATHS']

# handle static files & paths via the WSGI server
# (using cherrypy's tools.staticfile and tools.staticdir)
WSGI_STATIC_PATHS = False

def ustr(value):
    """This method is similar to the builtin `str` method, except
    it will return Unicode string.

    @param value: the value to convert

    @rtype: unicode
    @return: unicode string
    """

    if isinstance(value, unicode):
        return value

    if hasattr(value, "__unicode__"):
        return unicode(value)

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

    try:
        return ustr(str(value))
    except:
        return " ".join([ustr(s) for s in value])

__builtins__['ustr'] = ustr

import i18n
i18n.install()

application = cherrypy.tree.mount(controllers._root.Root(), '/')
def enable_static_paths():
    ''' Enables handling of static paths by CherryPy:
    * /openobject/static
    * /favicon.ico
    * LICENSE.txt
    '''
    global WSGI_STATIC_PATHS
    WSGI_STATIC_PATHS = True

    static_dir = os.path.abspath(
            openobject.paths.root('openobject', 'static'))
    application.merge(
        {'/openobject/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': static_dir
        }, '/favicon.ico': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(static_dir,
                                                      "images", "favicon.ico")
        }, '/LICENSE.txt': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(static_dir, '..', '..',
                                                      'doc', 'LICENSE.txt')
    }})

def configure(app_config):
    ''' Configures OpenERP Web Client. Takes a configuration dict
    (as output by cherrypy._cpconfig.as_dict), from it configures
    cherrypy globally and configure the OpenERP WSGI Application.
    '''
    _global = app_config.pop('global', {})
    _environ = _global.setdefault('server.environment', 'development')
    if _environ != 'development':
        _global['environment'] = _environ
    cherrypy.config.update(_global)
    application.merge(app_config)

# vim: ts=4 sts=4 sw=4 si et
