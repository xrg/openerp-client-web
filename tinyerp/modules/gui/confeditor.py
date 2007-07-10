###############################################################################
#
# Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id:  $
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

import re

from turbogears import expose
from turbogears import controllers
from turbogears import redirect
from turbogears import config

import cherrypy
import pkg_resources

from tinyerp import rpc
from tinyerp import common
import xmlrpclib

fname = pkg_resources.resource_filename('tinyerp.config', "app.cfg")
conf = config.ConfigObj(fname, unrepr=True, interpolation=True)

class ConfEditor(controllers.Controller):

    @expose(template="tinyerp.modules.gui.templates.confeditor")
    def index(self):
        passwd=None
        message=None

        return dict(message=message, passwd=passwd)

    @expose(template="tinyerp.modules.gui.templates.confeditor")
    def connect(self, **kw):

        passwd = kw.get('passwd')
        password = conf['etiny']['password']

        if passwd == password:
            cherrypy.session['terp_passwd'] = passwd
            raise redirect("/configure/change_server")
        else:
            message = str(_('Invalid Password !'))
            return dict(message=message, passwd=passwd)

    @expose(template="tinyerp.modules.gui.templates.confeditor")
    def change_server(self):
        message=None
        pwd = cherrypy.session.get('terp_passwd')

        if pwd != conf['etiny']['password']:
            raise redirect("/configure/connect")
        else:
            host = config.get('host', path="tinyerp")
            port = config.get('port', path="tinyerp")
            protocol = config.get('protocol', path="tinyerp")

            return dict(passwd=pwd, message=message, host=host, port=port, protocol=protocol)

    @expose(template="tinyerp.modules.gui.templates.confeditor")
    def setconf(self, **kw):

        host=kw.get('host')
        port=kw.get('port')
        protocol=kw.get('protocol')

        conf['tinyerp'] = {}
        conf['tinyerp']['host'] =  str(host)
        conf['tinyerp']['port'] = str(port)
        conf['tinyerp']['protocol'] = str(protocol)

        conf.write()
        config.update(conf)

        cherrypy.session['terp_passwd'] = None

        raise redirect("/login")


