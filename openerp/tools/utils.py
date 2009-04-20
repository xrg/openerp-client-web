
import cherrypy

from openerp.validators import Invalid


__all__ = ["url", "redirect", "validate", "error_handler", "exception_handler", "attrs", "attr_if", "decorated"]


def check_request_exists():
    try:
        cherrypy.request._test_request_exists = 1
        del cherrypy.request._test_request_exists
        return True
    except:
        return False


def url(*args, **kw):
    """Returns url from the provided arguments...
    for example:

    >>> print url('/my', 'path', a=100, b=100)
    >>> "/my/path?a=100&b=100"

    """

    if not kw and isinstance(args[-1], dict):
        kw = args[-1]
        args = args[:-1]

    path = '/'.join(map(str, args))
    query = '&'.join(map(lambda a: '%s=%s' % (a[0], a[1]), kw.items()))

    if path and query:
        path = path + '?' + query
    elif query:
        path = query

    if path.startswith('/'):
        webpath = (cherrypy.config.get('server.webpath') or '').rstrip('/')
        if check_request_exists():
            path = cherrypy.request.app.script_name + path
        path = webpath + path

    return path


def redirect(*args, **kw):
    return cherrypy.HTTPRedirect(url(*args, **kw))


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


def attrs(*args, **kw):

    kv = {}

    if len(args):
        if isinstance(args[0], dict):
            kv = args[0].copy()
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
            result.append('%s="%s"' % (name, value))
    return " ".join(result)

def attr_if(name, expression):
    return (expression or '') and '%s="%s"' % (name, name)


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

