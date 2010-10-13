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
# -   All names, links and logos of Tiny, OpenERP and Axelor must be
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

import cherrypy
from openerp.utils import rpc

from openobject import tools
from openobject.tools import expose


__all__ = ["secured", "unsecured", "login"]


@expose(template="/openerp/controllers/templates/login.mako")
def login(target, db=None, user=None, password=None, action=None, message=None, origArgs={}):

    url = rpc.session.connection_string
    url = str(url[:-1])

    dblist = []
    try:
        dblist = rpc.session.listdb()
    except:
        message = _("Could not connect to server")

    dbfilter = cherrypy.request.app.config['openerp-web'].get('dblist.filter')
    if dbfilter:
        headers = cherrypy.request.headers
        host = headers.get('X-Forwarded-Host', headers.get('Host'))

        base = re.split('\.|:|/', host)[0]

        if dbfilter == 'EXACT':
            if dblist is None:
                db = base
                dblist = [db]
            else:
                dblist = [d for d in dblist if d == base]

        elif dbfilter == 'UNDERSCORE':
            base = base + '_'
            if dblist is None:
                if db and not db.startswith(base):
                    db = None
            else:
                dblist = [d for d in dblist if d.startswith(base)]

        elif dbfilter == 'BOTH':
            if dblist is None:
                if db and db != base and not db.startswith(base + '_'):
                    db = None
            else:
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

        if rpc.session.is_logged() and kw.get('login_action') != 'login':
            # User is logged in; allow access
            clear_login_fields(kw)
            return fn(*args, **kw)
        else:
            action = kw.get('login_action', '')
            # get some settings from cookies
            try:
                db = cherrypy.request.cookie['terp_db'].value
                user = cherrypy.request.cookie['terp_user'].value
            except:
                db = ''
                user = ''

            db = kw.get('db', db)
            user = kw.get('user', user)
            password = kw.get('password', '')

            # See if the user just tried to log in
            if rpc.session.login(db, user, password) <= 0:
                # Bad login attempt
                if action == 'login':
                    message = _("Bad username or password")
                else:
                    message = ''

                return login(cherrypy.request.path_info, message=message,
                        db=db, user=user, action=action, origArgs=get_orig_args(kw))

            # Authorized. Set db, user name in cookies
            cookie = cherrypy.response.cookie
            cookie['terp_db'] = db
            cookie['terp_user'] = user.encode('utf-8')
            cookie['terp_db']['max-age'] = 3600
            cookie['terp_user']['max-age'] = 3600
            cookie['terp_db']['path'] = '/'
            cookie['terp_user']['path'] = '/'

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


# vim: ts=4 sts=4 sw=4 si et
