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

import socket
import xmlrpclib

from openobject.errors import AuthenticationError

import common

from tiny_socket import TinySocket
from tiny_socket import TinySocketError

class NotLoggedIn(common.TinyError, AuthenticationError): pass

class RPCException(Exception):
    """A common exeption class for RPC errors.
    """

    def __init__(self, code, backtrace):

        self.code = code
        self.args = backtrace

        if hasattr(code, 'split'):
            lines = code.split('\n')

            self.type = lines[0].split(' -- ')[0]
            self.message = ''
            if len(lines[0].split(' -- ')) > 1:
                self.message = lines[0].split(' -- ')[1]

            self.data = '\n'.join(lines[2:])

        else:
            self.type = 'error'
            self.message = backtrace
            self.data = backtrace

        self.backtrace = backtrace

    def __str__(self):
        return self.message


class RPCGateway(object):
    """Gateway abstraction, that implement common stuffs for rpc gateways.
    All RPC gateway should extends this class.
    """

    def __init__(self, session):
        if not isinstance(session, RPCSession):
            raise TypeError("RPCSession argument expected, got %s" % type(session))
        self.session = session

    def __rpc__(self, obj, method, args=(), auth=True):
        """Derived classes should owverride this method.

        @param obj: the remote object
        @param method: the method of the remote object
        @param args: arguments to be passed
        @param oauth: authentication is required or not

        @return: the result of the method
        """
        pass

    @property
    def connection_string(self):
        """Get the connection string...
        """
        return "%s://%s:%s/"%(self.session.protocol, self.session.host, self.session.port)

    def __convert(self, result):

        if isinstance(result, str):
            # try to convert into unicode string
            try:
                return ustr(result)
            except Exception, e:
                return result

        elif isinstance(result, list):
            return [self.__convert(val) for val in result]

        elif isinstance(result, tuple):
            return tuple([self.__convert(val) for val in result])

        elif isinstance(result, dict):
            newres = {}
            for key, val in result.items():
                newres[key] = self.__convert(val)

            return newres

        else:
            return result

    def __execute(self, obj, method, args=(), auth=True):
        try:
            result = self.__rpc__(obj, method, args, auth=auth)
            return self.__convert(result)
        except socket.error, e:
            raise common.TinyException(e.message or e.strerror, title=_('Application Error'))

        except RPCException, err:
            if err.type in ('warning', 'UserError'):
                if err.message in ('ConcurrencyException') and len(args) > 4:
                    common.concurrency(err.message, err.data, args)
                else:
                    common.warning(err.data)
            elif err.code.startswith('AccessDenied'):
                raise common.AccessDenied(err.code, _('Access Denied'))
            else:
                common.error(_('Application Error'), err.backtrace)

        except Exception, e:
            common.error(_('Application Error'), str(e))

    def execute(self, obj, method, *args):
        """Excecute the method of the obj with the given arguments.

        @param obj: the remote object
        @param method: the method of the remote object
        @param args: arguments to be passed

        @return: the result of the method
        """
        return self.__execute(obj, method, args)

    def execute_noauth(self, obj, method, *args):
        """Excecute the method of the obj with the given arguments without authentication.

        @param obj: the object
        @param method: the method to execute
        @param args: the arguments

        @return: the result of the method
        """
        return self.__execute(obj, method, args, auth=False)


class XMLRPCGateway(RPCGateway):
    """XMLRPC implementation.
    """

    def __init__(self, session):
        """Create new instance of XMLRPCGateway.

        @param session: a session
        """
        super(XMLRPCGateway, self).__init__(session)
        self._url = self.connection_string + 'xmlrpc/'

    def __rpc__(self, obj, method, args=(), auth=True):
        sock = xmlrpclib.ServerProxy(self._url + str(obj))
        try:
            if auth:
                args = (self.session.db, self.session.uid, self.session.password) + args
            return getattr(sock, method)(*args)
        except xmlrpclib.Fault, err:
            raise RPCException(err.faultCode, err.faultString)


class NETRPCGateway(RPCGateway):
    """NETRPC Implementation.
    """

    def __rpc__(self, obj, method, args=(), auth=True):
        sock = TinySocket()
        try:
            sock.connect(self.session.host, self.session.port)
            if auth:
                args = (self.session.db, self.session.uid, self.session.password) + args
            sock.send((obj, method) + args)
            res = sock.receive()
            sock.disconnect()
            return res

        except xmlrpclib.Fault, err:
            raise RPCException(err.faultCode, err.faultString)

        except TinySocketError, err:
            raise RPCException(err.faultCode, err.faultString)


# XXX: Fix openobject server to return PyTZ compatible timezone name
_TZ_ALIASES = {
    'IST' : 'Asia/Calcutta'
}


class RPCSession(object):
    """Maintains client session and provides way to authenticate
    client & invoce RPC requested by clients.
    """

    __slots__ = ['host', 'port', 'protocol', 'storage', 'gateway']

    def __init__(self, host, port, protocol='socket', storage={}):
        """Create new instance of RPCSession.

        @param host: the openobject-server host
        @params port: the openobject-server port
        @params protocol: the openobject-server protocol
        @param storage: a dict like storage that will be used to store session data
        """
        self.host = host
        self.port = port
        self.protocol = protocol
        self.storage = storage

        if protocol in ('http', 'https'):
            self.gateway = XMLRPCGateway(self)

        elif protocol == 'socket':
            self.gateway = NETRPCGateway(self)

        else:
            raise common.message(_("Unsupported protocol."))

    def __getattr__(self, name):
        try:
            return super(RPCSession, self).__getattribute__(name)
        except:
            pass

        return self.storage.get(name)

    def __setattr__(self, name, value):
        if name in self.__slots__:
            super(RPCSession, self).__setattr__(name, value)
        else:
            self.storage[name] = value

    def __getitem__(self, name):
        return self.storage[name]

    def __setitem__(self, name, value):
        self.storage[name] = value

    def __delitem__(self, name):
        try:
            del self.storage[name]
        except:
            pass

    def get(self, name, default=None):
        return self.storage.get(name, default)

    @property
    def context(self):
        return (self._context or {}).copy()

    @property
    def connection_string(self):
        return self.gateway.connection_string

    def listdb(self):
        try:
            return self.execute_noauth('db', 'list')
        except common.TinyError, e:
            if e.message == 'AccessDenied':
                return None
            raise

    def login(self, db, user, password):

        if not (db and user and password):
            return -1

        try:
            uid = self.execute_noauth('common', 'login', db, user, password)
        except Exception, e:
            return -1

        if uid <= 0:
            return -1

        self.storage['uid'] = uid
        self.storage['db'] = db
        self.storage['password'] = password
        self.storage['open'] = True

        # read the full name of the user
        res_users = self.execute('object', 'execute', 'res.users', 'read', [uid], ['name', 'company_id', 'login'])[0]
        self.storage['user_name'] = res_users['name']
        self.storage['company_id'], self.storage['company_name'] = res_users['company_id']
        self.storage['loginname'] = res_users['login']
        # set the context
        self.context_reload()

        return uid

    def logout(self):
        try:
            self.storage.clear()
        except Exception, e:
            pass

    def is_logged(self):
        return self.uid and self.open

    def context_reload(self):
        """Reload the context for the current user
        """

        self.storage['_context'] = {'client': 'web'}

        # self.uid
        context = self.execute('object', 'execute', 'res.users', 'context_get')
        self._context.update(context or {})

        self.storage['remote_timezone'] = 'utc'
        self.storage['client_timezone'] = self.context.get("tz", False)

        if self.storage.get('client_timezone'):
            self.storage['remote_timezone'] = self.execute('common', 'timezone_get')
            try:
                import pytz
            except:
                raise common.warning(_('You select a timezone but OpenERP could not find pytz library!\nThe timezone functionality will be disable.'))

        # set locale in session
        self.storage['locale'] = self.context.get('lang')

    def execute(self, obj, method, *args):
        if not self.is_logged():
            raise NotLoggedIn(_('Not logged...'), _('Authorization Error'))

        return self.gateway.execute(obj, method, *args)

    def execute_noauth(self, obj, method, *args):
        return self.gateway.execute_noauth(obj, method, *args)

    def execute_db(self, method, *args):
        return self.execute_noauth('db', method, *args)


# global session variable, will be initialized with connect
session = None


def initialize(host, port, protocol='socket', storage=None):
    """ Initialize the default rpc session.
    """
    global session
    session = RPCSession(host, port, protocol, storage=storage)


class RPCProxy(object):
    """A wrapper arround xmlrpclib, provides pythonic way to access tiny resources.

    For example,

    >>> users = RPCProxy("ir.users")
    >>> res = users.read([1], ['name', 'active_id'], session.context)
    """

    def __init__(self, resource):
        """Create new instance of RPCProxy for the give tiny resource

        @param resource: the tinyresource
        """
        self._resource = resource
        self._session = session
        self._attrs = {}

    def _func_getter(self, name):
        return lambda *args: self._session.execute("object", "execute", self._resource, name, *args)

    def __getattr__(self, name):
        if name not in self._attrs:
            return self._attrs.setdefault(name, self._func_getter(name))
        return self._attrs[name]


def name_get(model, id, context=None):

    id = (id or False) and int(id)
    name = (id or str('')) and str(id)

    if model and id:

        ctx = session.context.copy()
        ctx.update(context or {})

        proxy = RPCProxy(model)

        try:
            name = proxy.name_get([id], ctx)
            name = name[0][1] or ''
        except common.TinyWarning, e:
            name = _("== Access Denied ==")
        except Exception, e:
            raise e

    return name


if __name__=="__main__":

    host = 'localhost'
    port = 8070
    protocol = 'socket'

    initialize(host, port, protocol, storage=dict())

    res = session.listdb()
    print res

    res = session.login('t1', 'admin', 'admin')
    print res

    res = RPCProxy('res.users').read([session.uid], ['name'])
    print res

    print session.context


# vim: ts=4 sts=4 sw=4 si et
