###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# The OpenERP web client is distributed under the "OpenERP Public License".
# It's based on Mozilla Public License Version (MPL) 1.1 with following
# restrictions:
#
# -   All names, links and logos of Tiny, Open ERP and Axelor must be
#     kept as in original distribution without any changes in all software
#     screens, especially in start-up page and the software header, even if
#     the application source code has been changed or updated or code has been
#     added.
#
# -   All distributions of the software must keep source code with OEPL.
#
# -   All integrations to any other software must keep source code with OEPL.
#
# If you need commercial licence to remove this kind of restriction please
# contact us.
#
# You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################

import re
import time
import types

import cherrypy

from openobject import tools

from openobject.tools import rpc
from openobject.tools import expose
from openobject.tools import redirect

from base.validators import Invalid

__all__ = ["secured", "unsecured", "login", "validate", "error_handler", "exception_handler"]


@expose(template="templates/login.mako")
def login(target, db=None, user=None, password=None, action=None, message=None, origArgs={}):

    url = rpc.session.connection_string
    url = str(url[:-1])

    dblist = rpc.session.listdb()
    if dblist == -1:
        dblist = []
        message = _("Could not connect to server!")
        
    dbfilter = cherrypy.request.app.config['openobject-web'].get('dblist.filter')    
    if dbfilter:

        headers = cherrypy.request.headers
        host = headers.get('X-Forwarded-Host', headers.get('Host'))

        base = re.split('\.|:|/', host)[0]

        if dbfilter == 'NONE':
            dblist = dblist

        if dbfilter == 'EXACT':
            base = base
            dblist = [d for d in dblist if d == base]

        if dbfilter == 'UNDERSCORE':
            base = base + '_'
            dblist = [d for d in dblist if d.startswith(base)]

        if dbfilter == 'BOTH':
            dblist = [d for d in dblist if d.startswith(base + '_') or d == base]
            
    info = None
    try:
        info = rpc.session.execute_noauth('common', 'login_message') or ''
    except:
        pass
    return dict(target=target, url=url, dblist=dblist, db=db, user=user, password=password,
            action=action, message=message, origArgs=origArgs, info=info)

def secured(fn):
    """A Decorator to make a SecuredController controller method secured.
    """
    def clear_login_fields(kw={}):

        if not kw.get('login_action'):
            return

        if kw.has_key('db'): del kw['db']
        if kw.has_key('user'): del kw['user']
        if kw.has_key('password'): del kw['password']
        if kw.has_key('login_action'): del kw['login_action']

    def get_orig_args(kw={}):
        if not kw.get('login_action'):
            return kw

        new_kw = kw.copy()

        if new_kw.has_key('db'): del new_kw['db']
        if new_kw.has_key('user'): del new_kw['user']
        if new_kw.has_key('password'): del new_kw['password']
        if new_kw.has_key('login_action'): del new_kw['login_action']

        return new_kw

    def wrapper(*args, **kw):
        """The wrapper function to secure exposed methods
        """

        if rpc.session.is_logged():
            # User is logged in; allow access
            clear_login_fields(kw)
            return fn(*args, **kw)
        else:
            # User isn't logged in yet.

            db = None
            user = None
            password = None
            message = None

            action = kw.get('login_action')

            # get some settings from cookies
            try:
                db = cherrypy.request.cookie['terp_db'].value
                user = cherrypy.request.cookie['terp_user'].value
            except:
                pass

            db = kw.get('db', db)
            user = kw.get('user', user)
            password = kw.get('password', password)

            # See if the user just tried to log in
            if rpc.session.login(db, user, password) <= 0:
                # Bad login attempt
                if action == 'login':
                    message = _("Bad username or password!")

                return login(cherrypy.request.path_info, message=message,
                        db=db, user=user, action=action, origArgs=get_orig_args(kw))

            # Authorized. Set db, user name in cookies
            expiration_time = time.strftime("%a, %d-%b-%Y %H:%M:%S GMT", time.gmtime(time.time() + ( 60 * 60 * 24 * 365 )))
            cherrypy.response.cookie['terp_db'] = db
            cherrypy.response.cookie['terp_user'] = user.encode('utf-8')
            cherrypy.response.cookie['terp_db']['expires'] = expiration_time;
            cherrypy.response.cookie['terp_user']['expires'] = expiration_time;
            cherrypy.response.cookie['terp_db']['path'] = tools.url("/");
            cherrypy.response.cookie['terp_user']['path'] = tools.url("/");

            # User is now logged in, so show the content
            clear_login_fields(kw)
            return fn(*args, **kw)

    return tools.decorated(wrapper, fn, secured=True)


def unsecured(fn):
    """A Decorator to make a SecuredController controller method unsecured.
    """

    def wrapper(*args, **kw):
        return fn(*args, **kw)

    return tools.decorated(wrapper, fn, secured=False)


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


# vim: ts=4 sts=4 sw=4 si et

