
import cherrypy

from openerp.tools import tools

__all__ = ["url", "redirect", "validate", "error_handler", "exception_handler", "attrs", "attr_if"]


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
    result = []
    for k, v in kw.items():
        result += ['%s=%s'%(k, v)]

    path = '/'.join([str(a) for a in args])
    path = ((path or '') and path + '?') + '&'.join(result)

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

from openerp.validators import Invalid

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

        return tools.decorated(func_wrapper, func)

    return validate_wrapper

def error_handler(handler):

    def wrapper(func):

        def func_wrapper(*args, **kw):

            tg_errors = getattr(cherrypy.request, 'validation_errors', None)
            if tg_errors:
                kw['tg_errors'] = tg_errors
                return handler(*args, **kw)

            return func(*args, **kw)

        return tools.decorated(func_wrapper, func)

    return wrapper

def exception_handler(*args, **kw):
    return lambda f: f


def attrs(**kw):

    alias = {
        'css_class': 'class',
    }

    result = []
    for name, value in kw.iteritems():
        if callable(value):
            value = value()
        if value is not None:
            name = alias.get(name, name)
            result.append('%s="%s"' % (name, value))
    return " ".join(result)

def attr_if(name, expression):
    return (expression or '') and '%s="%s"' % (name, name)


