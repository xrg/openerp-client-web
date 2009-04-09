import cherrypy

def url(*args, **kw):
    """Returns url from the provided arguments...
    for example:

    >>> print url('/my', 'path', a=100, b=100)
    >>> "/my/path?a=100&b=100"

    """
    result = []
    for k, v in kw.items():
        result += ['%s=%s'%(k, v)]

    path = '/'.join([ustr(a) for a in args])
    path = ((path or '') and path + '?') + '&'.join(result)

    if path.startswith('/'):
        webpath = (cherrypy.config.get('server.webpath') or '').rstrip('/')
        #TODO: extend webpath with cherrypy mount point
        path = webpath + path

    return path

def redirect(*args, **kw):
    cherrypy.HTTPRedirect(url(*args, **kw)

def validate(*args, **kw):
    return lambda f: f

def error_handler(*args, **kw):
    return lambda f: f

def exception_handler(*args, **kw):
    return lambda f: f
