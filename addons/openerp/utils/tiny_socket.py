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
import cPickle
import sys

import cherrypy

DNS_CACHE = {}

class TinySocketError(Exception):

    def __init__(self, faultCode, faultString):
        self.faultCode = faultCode
        self.faultString = faultString
        self.args = (faultCode, faultString)

SOCKET_TIMEOUT = cherrypy.config.get('openerp.server.timeout')
socket.setdefaulttimeout(SOCKET_TIMEOUT)
class TinySocket(object):

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.sock.settimeout(SOCKET_TIMEOUT)

    def connect(self, host, port=False):
        if not port:
            protocol, buf = host.split('//')
            host, port = buf.split(':')
        if host in DNS_CACHE:
            host = DNS_CACHE[host]
        self.sock.connect((host, int(port)))
        DNS_CACHE[host], port = self.sock.getpeername()

    def disconnect(self):
        # on Mac, the connection is automatically shutdown when the server disconnect.
        # see http://bugs.python.org/issue4397
        if sys.platform != 'darwin':
            self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def send(self, msg, exception=False, traceback=None):
        msg = cPickle.dumps([msg,traceback])
        self.sock.sendall('%8d%s%s' % (len(msg), exception and "1" or "0", msg))

    def receive(self):

        def read(socket, size):
            buf=''
            while len(buf) < size:
                chunk = self.sock.recv(size - len(buf))
                if chunk == '':
                    raise RuntimeError, "socket connection broken"
                buf += chunk
            return buf

        size = int(read(self.sock, 8))
        buf = read(self.sock, 1)
        exception = buf != '0' and buf or False
        res = cPickle.loads(read(self.sock, size))

        if isinstance(res[0],Exception):
            if exception:
                raise TinySocketError(ustr(res[0]), ustr(res[1]))
            raise res[0]
        else:
            return res[0]

# vim: ts=4 sts=4 sw=4 si et
