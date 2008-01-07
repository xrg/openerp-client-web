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

from turbogears import expose
from turbogears import controllers
from turbogears import validators, validate
from turbogears import redirect
from turbogears import config

import cherrypy
import pkg_resources

from tinyerp import rpc
from tinyerp import common
from tinyerp import CONFIG_FILE

import xmlrpclib

conf = config.ConfigObj(CONFIG_FILE, unrepr=True, interpolation=True)

class MySchema(validators.Schema):
    host = validators.String(not_empty=True)
    port = validators.Int(not_empty=True)
    protocol = validators.String(not_empty=True)
    oldpwd = validators.OneOf([conf.get('etiny', {}).get('passwd', '')])
    newpwd = validators.String()
    repwd = validators.String()
    chained_validators = [validators.RequireIfPresent(present='oldpwd',required='newpwd'), validators.FieldsMatch('newpwd', 'repwd')]

class ConfEditor(controllers.Controller):

    @expose(template="tinyerp.subcontrollers.templates.confeditor")
    def index(self):
        password = conf.get('etiny', {}).get('passwd', '')

        if password == "":
            raise common.error(_("Error"), _("Administration password is empty..!"))

        return dict(message=None, passwd=None, tg_errors=None)

    @expose(template="tinyerp.subcontrollers.templates.confeditor")
    def connect(self, **kw):

        passwd = kw.get('passwd')
        password = conf['etiny']['passwd']

        if passwd == password:
            cherrypy.session['terp_passwd'] = passwd
            raise redirect("/configure/change_server")
        else:
            message = str(_('Invalid Password !'))
            return dict(message=message, passwd=None, host=None, port=None, protocol=None)

    @expose(template="tinyerp.subcontrollers.templates.confeditor")
    def change_server(self):
        spwd = cherrypy.session.get('terp_passwd')

        if spwd != conf['etiny']['passwd']:
            raise redirect("/configure/connect")
        else:
            host = config.get('host', path="tinyerp")
            port = config.get('port', path="tinyerp")
            protocol = config.get('protocol', path="tinyerp")
            comp_url = config.get('company_url', path='etiny')

            return dict(passwd=spwd, message=None, host=host, port=port, protocol=protocol, comp_url=comp_url)

    @validate(validators=MySchema())
    @expose(template="tinyerp.subcontrollers.templates.confeditor")
    def setconf(self, new_logo, tg_errors=None, **kw):

        datas = new_logo.file.read()
        
        if datas:
            try:
                logo_path = pkg_resources.resource_filename("tinyerp", "static/images/company_logo.png")
                logo_file = open(logo_path, 'wb')
                logo_file.write(datas)
                logo_file.close()
            except Exception, e:
                raise common.error(_('Error'), _('File reading or writing failed... !'))
        
        host = kw.get('host')
        port = kw.get('port')
        protocol = kw.get('protocol')
        newpwd = kw.get('newpwd')
        comp_url = kw.get('comp_url')
       
        if not comp_url.startswith('http'):
            comp_url = 'http://'+comp_url

        if tg_errors:
            return dict(message=None, passwd=None, host=host, port=port, protocol=protocol, comp_url=comp_url)

        oldpwd=kw.get('oldpwd')
        spwd = cherrypy.session.get('terp_passwd')

        if spwd == oldpwd and newpwd:
            cherrypy.session['terp_passwd'] = newpwd
            conf['etiny'] = {}
            conf['etiny']['passwd'] = str(newpwd)

        conf['tinyerp'] = {}
        conf['tinyerp']['host'] =  str(host)
        conf['tinyerp']['port'] = str(port)
        conf['tinyerp']['protocol'] = str(protocol)

        conf['etiny']['company_url'] = str(comp_url)
        
        conf.write()
        config.update(conf)

        cherrypy.session['terp_passwd'] = None

        raise redirect("/login")
