###############################################################################
#
# Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################################################

"""
This modules implements custom authorization logic for the eTiny!.
"""

import time
import types

from turbogears import expose
from turbogears import redirect
from turbogears import config

import cherrypy
import rpc
import pkg_resources

@expose(template="tinyerp.templates.login")
def _login(target, dblist=None, db= None, user=None, action=None, message=None, origArgs={}):
    """Login page, exposed without any controller, will be used by _check_method wrapper
    """
    url = rpc.session.get_url()
    url = str(url[:-1])

    return dict(target=target, url=url, dblist=dblist, user=user, passwd=None, db=db, action=action, message=message, origArgs=origArgs)

def secured(fn):
    """A Decorator to make a TinyResource controller method secured.
    """
    def clear_login_fields(kw={}):

        if not kw.get('login_action'):
            return

        if kw.has_key('db'): del kw['db']
        if kw.has_key('user'): del kw['user']
        if kw.has_key('passwd'): del kw['passwd']
        if kw.has_key('login_action'): del kw['login_action']

    def get_orig_args(kw={}):
        if not kw.get('login_action'):
            return kw

        new_kw = kw.copy()

        if new_kw.has_key('db'): del new_kw['db']
        if new_kw.has_key('user'): del new_kw['user']
        if new_kw.has_key('passwd'): del new_kw['passwd']
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
            passwd = None
            message = None

            action = kw.get('login_action')

            # get some settings from cookies
            try:
                db = cherrypy.request.simple_cookie['terp_db'].value
                user = cherrypy.request.simple_cookie['terp_user'].value
            except:
                pass

            db = kw.get('db', db)
            user = kw.get('user', user)
            passwd = kw.get('passwd', passwd)

            # See if the user just tried to log in
            if rpc.session.login(db, user, passwd) <= 0:
                # Bad login attempt
                dblist = rpc.session.listdb()
                if dblist == -1:
                    dblist = []
                    message = _("Could not connect to server !")

                if action == 'login':
                    message = _("Bad username or password !")

                return _login(cherrypy.request.path, message=message, dblist=dblist, db=db, user=user, action=action, origArgs=get_orig_args(kw))

            # Authorized. Set db, user name in cookies
            expiration_time = time.strftime("%a, %d-%b-%Y %H:%M:%S GMT", time.gmtime(time.time() + ( 60 * 60 * 24 * 365 )))
            cherrypy.response.simple_cookie['terp_db'] = db
            cherrypy.response.simple_cookie['terp_user'] = user.encode('utf-8')
            cherrypy.response.simple_cookie['terp_db']['expires'] = expiration_time;
            cherrypy.response.simple_cookie['terp_user']['expires'] = expiration_time;

            # User is now logged in, so show the content
            clear_login_fields(kw)
            return fn(*args, **kw)

    # restore the original values
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    wrapper.__dict__ = fn.__dict__.copy()
    wrapper.__module__ = fn.__module__

    wrapper.secured = True

    return wrapper

def unsecured(fn):
    """A Decorator to make a TinyResource controller method unsecured.
    """

    def wrapper(*args, **kw):
        return fn(*args, **kw)

    # restore the original values
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    wrapper.__dict__ = fn.__dict__.copy()
    wrapper.__module__ = fn.__module__

    wrapper.secured = False

    return wrapper

class TinyResource(object):
    """Provides a convenient way to secure entire TG controller
    """
    def __getattribute__( self, name ):
        value= object.__getattribute__(self, name)

        if isinstance(value, types.MethodType ) and hasattr(value, "exposed") and not (hasattr(value, "secured") and not value.secured):
            return secured(value)

        # Some other property
        return value
