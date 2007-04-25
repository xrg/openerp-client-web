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

import xmlrpclib, socket
import cherrypy
import time

class RPCException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.message = msg

    def __str__(self):
        return self.message

class RPCSession(object):
    """ Provides wrapper arround xmlrpclib and maintains HTTP session
    """

    def __init__(self):
        pass

    def list_db(self, host, port , secure=False):
        """Returns list of databases on the given server

        @param host: the host where TinyERP server is running
        @param port: the TinyERP server port
        @param secure: whether to use secured connection or not

        @return: list of all databases
        """
        url = 'http://'

        if secure:
            url = 'https://'

        url += "%s:%s/xmlrpc"%(host, str(port))

        sock = xmlrpclib.ServerProxy(url + '/db')
        try:
            return sock.list()
        except Exception, e:
            return -1

    def login(self, host, port, db, user, password, secure=False):
        """Login to a Tiny Server on given host using given database, username and password.

        @param host: the host on which tiny server is running
        @param db: the database
        @param user: user id
        @param password: password
        @param secure: use secured connection?

        @rtype: int
        @return: user id on success else error code
        """

        url = 'http://'

        if secure:
            url = 'https://'

        url += "%s:%s/xmlrpc"%(host, str(port))

        sock = xmlrpclib.ServerProxy(url + '/common')
        try:
            res = sock.login(db, user, password)
        except Exception, e:
            return -1

        if not res:
            cherrypy.session['open'] = False
            cherrypy.session['uid'] = None
            return -2

        cherrypy.session['open'] = True
        cherrypy.session['url'] = url
        cherrypy.session['uid'] = res
        cherrypy.session['uname'] = user
        cherrypy.session['passwd'] = password
        cherrypy.session['db'] = db

        lang = cherrypy.request.simple_cookie.get('terp_lang', None)
        cherrypy.session['context'] = (lang or {}) and {'lang': lang.value}

        # set host, port and uname in cookies
        cherrypy.response.simple_cookie['terp_host'] = host
        cherrypy.response.simple_cookie['terp_port'] = port
        cherrypy.response.simple_cookie['terp_db'] = db
        cherrypy.response.simple_cookie['terp_user'] = user

        expiration_time = time.strftime("%a, %d-%b-%Y %H:%M:%S GMT", time.gmtime(time.time() + ( 60 * 60 * 24 * 365 )))

        cherrypy.response.simple_cookie['terp_host']['expires'] = expiration_time;
        cherrypy.response.simple_cookie['terp_port']['expires'] = expiration_time;
        cherrypy.response.simple_cookie['terp_db']['expires'] = expiration_time;
        cherrypy.response.simple_cookie['terp_user']['expires'] = expiration_time;

        # get the full user name
        users = RPCProxy('res.users')
        res = users.read([res], ['name'])
        cherrypy.session['fullname'] = res[0]['name']

        return 1

    def logout(self):
        """Terminate the current session
        """
        try:
            del cherrypy.session['open']
            del cherrypy.session['uid']
            del cherrypy.session['uname']
            del cherrypy.session['passwd']
            del cherrypy.session['db']
            del cherrypy.session['url']
            del cherrypy.session['fullname']
        except:
            pass

    def is_logged(self):
        """Returns True if user is already logged-in otherwise returns False

        @rtype: bool
        @return: True if user is logged in otherwise false
        """
        return cherrypy.session.has_key('uid') and cherrypy.session['open']

    def context_reload(self):
        """Reload the context for the current user
        """
        self.context = {}
        # self.uid
        context = self.execute('/object', 'execute', 'ir.values', 'get', 'meta', False, [('res.users', self.uid or False)], False, {}, True, True, False)
        for c in context:
            if c[2]:
                cherrypy.session['context'][c[1]] = c[2]

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
        """A wrapper around xmlrpclib, will execute the given method of the object with
        all the provided arguments.

        @param obj: the tiny object
        @param method: a method of the object
        @param args: arguments to be passed to the method

        @rtype: list
        @return: list of dict, containing results
        """

        if self.is_logged():
            try:
                sock = xmlrpclib.ServerProxy(self.url + obj)
                result = getattr(sock, method)(self.db, self.uid, self.passwd, *args)
                return self.__convert(result)
            except socket.error, e:
                raise RPCException(69, 'Connection refused!')
            except xmlrpclib.Fault, e:
                raise RPCException(e.faultCode, e.faultString + str(args))
        else:
            raise RPCException(1, "not logged!")

    # access cherrypy session attributes at object attribute
    def __getattr__(self,name):
        if cherrypy.session.has_key(name):
            return cherrypy.session[name]
        else:
            raise AttributeError("no such attribute '%s'"%name)


# global session object
session = RPCSession()

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
        return session.execute("/object", "execute", self.object, self.func, *args)
