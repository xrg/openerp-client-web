import urllib

import cherrypy
from mako.filters import html_escape


__all__ = ["url", "url_plus", "redirect", "config", "content", "attrs", "attr_if", "decorated",
           "AuthenticationError"]

class AuthenticationError(Exception): pass

def url(_cppath, _cpparams=None, **kw):
    """
    Returns absolute url for the given _cppath, _cpparams and kw.

    If _cppath is a list, path will be created joining them with '/'.
    If _cpparams is given it should be a map or list of tuples to create a map.

    query string will be created from _cpparams and **kw.

    >>> url("/some/path", {"a": 1, "b": 2})
    >>> /some/path?a=1&b=2
    >>> url(["some", "path"], a=1, b=2)
    >>> /some/path?a=1&b=2
    """

    path = _cppath
    if not isinstance(_cppath, basestring):
        path = "/".join(list(_cppath))

    params = _cpparams or {}
    if isinstance(_cpparams, list):
        params = dict(_cpparams)
    params.update(kw)

    kv = []
    for k, v in params.iteritems():
        if isinstance(k, basestring) and isinstance(v, basestring):
            k = urllib.quote_plus(k)
            v = urllib.quote_plus(v)
        kv.append("%s=%s" % (k, v))

    query = '&'.join(kv)

    if path and query:
        path = path + '?' + query
    elif query:
        path = query

    if path.startswith('/') and cherrypy.request.app and \
        not path.startswith(cherrypy.request.app.script_name):
        path = cherrypy.request.app.script_name + path

    return path


def url_plus(_cppath, _cpparams=None, **kw):
    return url(_cppath, _cpparams, **kw)


def redirect(_cppath, _cpparams=None, **kw):
    if isinstance(_cppath, unicode):
        _cppath = _cppath.encode('utf-8')
    if 'X-Requested-With' in cherrypy.request.headers:
        kw['requested_with'] = cherrypy.request.headers['X-Requested-With']
    return cherrypy.HTTPRedirect(url(_cppath, _cpparams, **kw))


def config(key, section='global', default=None):
    """A handy function to access config values.
    """
    
    if section == 'global':
        return cherrypy.config.get(key)
    
    return cherrypy.request.app.config.get(section, {}).get(key, default)


class NoEscape(object):
    """A special callable class to prevent appying `html_escape` filter
    by the default `content` filter.
    """

    def __init__(self, value):
        self.value = value

    def __call__(self, *args, **kw):
        try:
            return unicode(self.value(*args, **kw))
        except:
            pass
        return unicode(self.value)

    def encode(self, encoding):
        return self().encode(encoding)

    def __unicode__(self):
        return self()

    def __str__(self):
        return self()


def content(value):
    """A Mako filter to return unicode string according to the given value.

    If value is None return empty string.
    If value is instance of NoEscape return unicode string.
    If value is not None nor instance of NoEscape return unicode string applying `html_escape` filter.
    """
    if value is None:
        return ""

    if isinstance(value, NoEscape):
        return ustr(value)

    return html_escape(ustr(value))


def attrs(*args, **kw):

    kv = {}

    for arg in args:
        kv.update(arg)

    kv.update(kw)

    alias = {
        'css_class': 'class',
    }

    result = []
    for name, value in kv.iteritems():
        if callable(value):
            value = value()
        if value is not None:
            name = alias.get(name, name)
            result.append('%s="%s"' % (name, content(value)))

    return NoEscape(" ".join(result))


def attr_if(name, expression):
    return NoEscape((expression or '') and '%s="%s"' % (name, content(name)))


def decorated(wrapper, func, **attrs):
    """Update decorated wrapper of the func with given attrs
    and make sure to keep original metadata.
    """

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__dict__ = func.__dict__.copy()
    wrapper.__module__ = func.__module__

    for k, v in attrs.iteritems():
        try:
            setattr(wrapper, k, v)
        except:
            pass

    return wrapper
