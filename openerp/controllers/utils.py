

import re
import time
import types

import cherrypy

from openerp import tools

from openerp.tools import rpc
from openerp.tools import expose
from openerp.tools import redirect


__all__ = ["secured", "unsecured", "login"]


@expose(template="templates/login.mako")
def login(target, db=None, user=None, password=None, action=None, message=None, origArgs={}):

    url = rpc.session.connection_string
    url = str(url[:-1])

    dblist = rpc.session.listdb()
    if dblist == -1:
        dblist = []
        message = _("Could not connect to server!")
        
    dbfilter = cherrypy.request.app.config['openerp-web'].get('dblist.filter')    
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

