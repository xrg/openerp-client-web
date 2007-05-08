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
This module provides wrappers arround xmlrpclib that allows accessing
Tiny resources in pythonic way.
"""

import time
import socket
import xmlrpclib

import tiny_socket

class RPCException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.message = msg

    def __str__(self):
        return self.message

class RPCGateway(object):
    """Gateway abstraction, that implement common stuffs for rpc gateways.
    All RPC gateway should extends this class.
    """

    def __init__(self, protocol, host, port):

        self.protocol = protocol
        self.host = host
        self.port = port

        self.uid = None
        self.user = None
        self.passwd = None

        self.open = None
        self.db = None

    def get_url(self):
        """Get the url
        """

        return "%s://%s:%s/"%(self.protocol, self.host, self.port)

    def listdb(self):
        """Get the list of databases.
        """
        pass

    def login(self, db, user, passwd):
        """Do login.

        @param db: the database
        @param user: the user
        @param passwd: the password

        @return: 1 on success else negative error value
        """
        pass

    def _login_result(self, db, user, passwd, result):

        if not result:
            self.open = False
            self.uid = None
            return -2

        self.uid = result
        self.user = user
        self.passwd = passwd

        self.db = db
        self.open = True

        return 1

    def execute(self, obj, method, *args):
        """Excecute the method of the obj with the given arguments.

        @param obj: the object
        @param method: the method to execute
        @param args: the arguments

        @return: the result of the method
        """
        pass

    def execute_db(self, method, *args):
        """Execute a database related method.
        """
        pass

    def __setattr__(self, name, value):
        setattr(session, name, value)

    def __getattr__(self, name):
        return getattr(session, name)

class XMLRPCGateway(RPCGateway):
    """XMLRPC implementation.
    """

    def __init__(self, host, port, protocol='http'):
        """Create new instance of XMLRPCGateway.

        @param host: the host
        @param port: the port
        @param protocol: either http or https
        """
        super(XMLRPCGateway, self).__init__(protocol, host, port)
        self.url =  self.get_url() + 'xmlrpc/'

    def listdb(self):
        sock = xmlrpclib.ServerProxy(self.url + 'db')
        try:
            return sock.list()
        except Exception, e:
            return -1

    def login(self, db, user, passwd):
        sock = xmlrpclib.ServerProxy(self.url + 'common')
        try:
            res = sock.login(db, user, passwd)
        except Exception, e:
            return -1

        return self._login_result(db, user, passwd, res)

    def execute(self, obj, method, *args):
        sock = xmlrpclib.ServerProxy(self.url + str(obj))
        try:
            result = getattr(sock, method)(self.db, self.uid, self.passwd, *args)
            return result
        except Exception, e:
            return -1

    def execute_db(self, method, *args):
        sock = xmlrpclib.ServerProxy(self.url + 'db')
        try:
            result = getattr(sock, method)(*args)
            return result
        except Exception, e:
            return -1

class NETRPCGateway(RPCGateway):
    """NETRPC Implementation.
    """

    def __init__(self, host, port):
        super(NETRPCGateway, self).__init__('socket', host, port)

    def listdb(self):
        sock = tiny_socket.mysocket()
        try:
            sock.connect(self.host, self.port)
            sock.mysend(('db', 'list'))
            res = sock.myreceive()
            sock.disconnect()
            return res
        except Exception, e:
            return -1

    def login(self, db, user, passwd):
        sock = tiny_socket.mysocket()
        try:
            sock.connect(self.host, self.port)
            sock.mysend(('common', 'login', db, user, passwd))
            res = sock.myreceive()
            sock.disconnect()
        except Exception, e:
            return -1

        return self._login_result(db, user, passwd, res)

    def _make_args(self, *args):
        """Passing unicode argument causes error, so convert each unicode argument into utf-8 encoded str.
        """
        result = []
        for arg in args:
            if isinstance(arg, unicode):
                arg = arg.encode('utf-8')
            result.append(arg)
        return result

    def execute(self, obj, method, *args):
        sock = tiny_socket.mysocket()
        try:
            sock.connect(self.host, self.port)
            sock.mysend(self._make_args(obj, method, self.db, self.uid, self.passwd, *args))
            res = sock.myreceive()
            sock.disconnect()
            return res
        except Exception, e:
            return -1

    def execute_db(self, method, *args):
        sock = tiny_socket.mysocket()
        try:
            sock.connect(self.host, self.port)
            sock.mysend(self._make_args('db', method, *args))
            res = sock.myreceive()
            sock.disconnect()
            return res
        except Exception, e:
            return -1

class RPCSession(object):
    """This is a wrapper class that provides Pythonic way to handle RPC (remote procedure call).
    It also provides a way to store session data into different kind of store.
    """

    def __init__(self, store={}):
        """Create new instance of RPCSession.

        @param store: the storage that will be used to store session data
        """
        self.store = store
        self.gateway = None

    def __getattr__(self, name):
        try:
            return super(RPCSession, self).__getattribute__(name)
        except:
            pass

        return self.store.get(name)

    def __setattr__(self, name, value):
        if name in ('store'):
            super(RPCSession, self).__setattr__(name, value)
        else:
            self.store[name] = value

    def get_url(self):
        return (self.gateway or None) and self.gateway.get_url()

    def listdb(self, host, port, protocol='http'):
        protocol = protocol or 'http'

        if protocol in ('http', 'https'):
            gw = XMLRPCGateway(host, port, protocol)
        elif protocol == 'socket':
            gw = NETRPCGateway(host, port)
        else:
            raise "Unsupported protocol:", protocol

        self.gateway = gw
        return gw.listdb()

    def login(self, host, port, db, user, passwd, protocol='http', lang=None):

        protocol = protocol or 'http'

        if protocol in ('http', 'https'):
            gw = XMLRPCGateway(host, port, protocol)
        elif protocol == 'socket':
            gw = NETRPCGateway(host, port)
        else:
            raise "Unsupported protocol:", protocol

        res = gw.login(db, user, passwd)

        if res != 1: return res

        self.gateway = gw
        # read the full name of the user
        self.user_name = self.execute('object', 'execute', 'res.users', 'read', [session.uid], ['name'])[0]['name']

        # set global context
        self.context = (lang or {}) and {'lang': lang}

        return res

    def logout(self):
        self.gateway = None
        try:
            del self.store['open']
            del self.store['uid']
            del self.store['user']
            del self.store['passwd']
            del self.store['db']
            del self.store['host']
            del self.store['port']
            del self.store['protocol']
            del self.store['user_name']
        except:
            pass

    def is_logged(self):
        return self.uid and self.open

    def context_reload(self):
        """Reload the context for the current user
        """
        self.context = {}
        # self.uid
        context = self.execute('object', 'execute', 'ir.values', 'get', 'meta', False, [('res.users', self.uid or False)], False, {}, True, True, False)
        for c in context:
            if c[2]:
                self.context[c[1]] = c[2]

    def __convert(self, result):

        if isinstance(result, basestring):
            return ustr(result)

        elif isinstance(result, list):
            return [self.__convert(val) for val in result]

        elif isinstance(result, dict):
            newres = {}
            for key, val in result.items():
                newres[key] = self.__convert(val)

            return newres

        else:
            return result

    def execute(self, obj, method, *args):

        if not self.is_logged():
            raise RPCException(1, "not logged!")

        result = self.gateway.execute(obj, method, *args)
        return self.__convert(result)

    def execute_db(self, method, *args):
        return self.gateway.execute_db(method, *args)

# client must initialise session with store, e.g. session = RPCSession(store=dict())
session = None

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
        self.resource = resource
        self.__attrs = {}

    def __getattr__(self, name):
        if not name in self.__attrs:
            self.__attrs[name] = RPCFunction(self.resource, name)
        return self.__attrs[name]

class RPCFunction(object):
    """A wrapper arround xmlrpclib, provides pythonic way to execute tiny methods.
    """

    def __init__(self, object, func_name):
        """Create a new instance of RPCFunction.

        @param object: name of a tiny object
        @param func_name: name of the function
        """
        self.object = object
        self.func = func_name

    def __call__(self, *args):
        return session.execute("object", "execute", self.object, self.func, *args)

if __name__=="__main__":

    session = RPCSession(store=dict())

    host = '192.168.0.13'
    port = '8069'
    protocol = 'http'

    res = session.listdb(host, port, protocol)
    print res

    res = session.login(host, port, 'etiny', 'admin', 'admin', protocol)
    print res

    res = RPCProxy('res.users').read([session.uid], ['name'])
    print res

    res = RPCProxy('ir.values').get('action', 'tree_but_open', [('ir.ui.menu', 73)], False, {})
    print res
