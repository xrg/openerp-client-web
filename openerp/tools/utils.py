import os
import urllib

import cherrypy
from mako.filters import html_escape

from openerp.validators import Invalid


__all__ = ["url", "url_plus", "redirect", "validate", "error_handler", "exception_handler", 
           "attrs", "attr_if", "decorated"]


def url(_cppath, _cpparams=None, _cpquote=False, **kw):
    """
    Returns absolute url for the given _cppath, _cpparams and kw.
    
    If _cppath is a list, path will be created joining them with '/'.
    If _cpquote if True, url_quote the params/kw
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
        if _cpquote and isinstance(k, basestring) and isinstance(v, basestring):
            k = urllib.quote_plus(k)
            v = urllib.quote_plus(v)
        kv.append("%s=%s" % (k, v))

    query = '&'.join(kv)

    if path and query:
        path = path + '?' + query
    elif query:
        path = query

    if path.startswith('/'):
        webpath = (cherrypy.config.get('server.webpath') or '').rstrip('/')
        if cherrypy.request.app:
            path = cherrypy.request.app.script_name + path
        path = webpath + path

    return path


def url_plus(_cppath, _cpparams=None, **kw):
    return url(_cppath, _cpparams, True, **kw)


def redirect(_cppath, _cpparams=None, **kw):
    return cherrypy.HTTPRedirect(url(_cppath, _cpparams, **kw))


from itertools import izip, islice
from inspect import getargspec

def to_kw(func, args, kw):

    argnames, defaults = getargspec(func)[::3]
    defaults = defaults or []

    kv = zip(islice(argnames, 0, len(argnames) - len(defaults)), args)
    kw.update(kv)

    return args[len(argnames)-len(defaults):], kw

def from_kw(func, args, kw):

    argnames, defaults = getargspec(func)[::3]
    defaults = defaults or []

    newargs = [kw.pop(name) for name in islice(argnames, 0, len(argnames) - len(defaults)) if name in kw]
    newargs.extend(args)

    return newargs, kw


def validate(form=None, validators=None):

    def validate_wrapper(func):

        if callable(form) and not hasattr(form, "validate"):
            init_form = lambda self: form(self)
        else:
            init_form = lambda self: form

        def func_wrapper(*args, **kw):

            # do not validate a second time if already validated
            if hasattr(cherrypy.request, 'validation_state'):
                return func(*args, **kw)

            form = init_form(args and args[0] or kw["self"])
            args, kw = to_kw(func, args, kw)

            errors = {}

            if form:
                value = kw.copy()
                value.pop('self', None)
                try:
                    kw.update(form.validate(value, None))
                except Invalid, e:
                    errors = e.unpack_errors()
                    cherrypy.request.validation_exception = e
                    cherrypy.request.validation_value = value
                cherrypy.request.validated_form = form

            if validators:

                if isinstance(validators, dict):
                    for field, validator in validators.iteritems():
                        try:
                            kw[field] = validator.to_python(
                                kw.get(field, None), None)
                        except Invalid, error:
                            errors[field] = error
                else:
                    try:
                        value = kw.copy()
                        kw.update(validators.to_python(value, None))
                    except Invalid, e:
                        errors = e.unpack_errors()
                        cherrypy.request.validation_exception = e
                        cherrypy.request.validation_value = value

            cherrypy.request.validation_errors = errors
            cherrypy.request.input_values = kw.copy()
            cherrypy.request.validation_state = True

            args, kw = from_kw(func, args, kw)
            return func(*args, **kw)

        return decorated(func_wrapper, func)

    return validate_wrapper

def error_handler(handler):

    def wrapper(func):

        def func_wrapper(*args, **kw):

            tg_errors = getattr(cherrypy.request, 'validation_errors', None)
            if tg_errors:
                kw['tg_errors'] = tg_errors
                return handler(*args, **kw)

            return func(*args, **kw)

        return decorated(func_wrapper, func)

    return wrapper

def exception_handler(*args, **kw):
    return lambda f: f


def config(key, section, default=None):
    """A handy function to access config values.
    """
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
        if isinstance(arg, dict):
            kv.update(arg)
        else:
            raise TypeError

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

