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
import types

from turbogears import expose
from turbogears import redirect

import cherrypy

import rpc

@expose(template="tinyerp.templates.login")
def _login(target, protocol='http', host='', port='8069', dblist=[], db= None, user=None, action=None, message=None, origArgs={}):
    """Login page, exposed without any controller, will be used by _check_method wrapper
    """
    return dict(target=target, protocol=protocol, host=host, port=port, dblist=dblist, user=user, db=db, action=action, message=message, origArgs=origArgs)

def _check_method(obj, fn):
    """A python decorator to secure exposed methods
    """
    def clear_login_fields(kw={}):

        if not kw.get('login_action'):
            return

        if kw.has_key('host'): del kw['host']
        if kw.has_key('port'): del kw['port']
        if kw.has_key('protocol'): del kw['protocol']
        if kw.has_key('db'): del kw['db']
        if kw.has_key('user'): del kw['user']
        if kw.has_key('passwd'): del kw['passwd']
        if kw.has_key('login_action'): del kw['login_action']

    def get_orig_args(kw={}):
        if not kw.get('login_action'):
            return kw

        new_kw = kw.copy()

        if new_kw.has_key('host'): del new_kw['host']
        if new_kw.has_key('port'): del new_kw['port']
        if new_kw.has_key('protocol'): del new_kw['protocol']
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

            host = ''
            port = ''
            protocol = ''
            db = ''
            user = ''
            passwd = ''
            message = None

            action = kw.get('login_action')

            # get some settings from cookies
            try:
                host = cherrypy.request.simple_cookie['terp_host'].value
                port = cherrypy.request.simple_cookie['terp_port'].value
                protocol = cherrypy.request.simple_cookie['terp_protocol'].value
                db = cherrypy.request.simple_cookie['terp_db'].value
                user = cherrypy.request.simple_cookie['terp_user'].value
            except:
                pass

            host = kw.get('host', host)
            port = kw.get('port', port)
            protocol = kw.get('protocol', protocol)
            db = kw.get('db', db)
            user = kw.get('user', user)
            passwd = kw.get('passwd', passwd)

            if kw.get('login_action') == 'connect':
                dblist = rpc.session.list_db(host, port, protocol)
                if dblist == -1:
                    dblist = None
                    message="Invalid Host or Host not found"

                cherrypy.response.status = 401
                return _login(cherrypy.request.path, message=message, protocol=protocol, host=host, port=port, dblist=dblist, db=db, user=user, action=action, origArgs=get_orig_args(kw))

            if kw.get('login_action') == 'login':
                message='Invalid user id or password.'

            # See if the user just tried to log in
            if rpc.session.login(host, port, db, user, passwd, protocol) != 1:
                # Bad login attempt
                dblist = rpc.session.list_db(host, port, protocol)
                if dblist == -1:
                    dblist = []

                cherrypy.response.status = 401
                return _login(cherrypy.request.path, message=message, protocol=protocol, host=host, port=port, dblist=dblist, db=db, user=user, action=action, origArgs=get_orig_args(kw))

            # User is now logged in, so show the content
            clear_login_fields(kw)
            return fn(*args, **kw)

   # restore the original values
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    wrapper.__dict__ = fn.__dict__.copy()
    wrapper.__module__ = fn.__module__

    return wrapper

class TinyResource(object):
    """Provides a convenient way to secure entire TG controller
    """
    def __getattribute__( self, name ):
        value= object.__getattribute__(self, name)
        if (isinstance(value, types.MethodType ) and hasattr( value, "exposed" )):
            return _check_method(self, value)

        # Some other property
        return value
