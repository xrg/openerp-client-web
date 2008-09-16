###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
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
# along with this program; if not, write to the 
# Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
# Boston, MA  02111-1307, USA.
#
###############################################################################

import re

from turbogears import expose
from turbogears import widgets
from turbogears import controllers
from turbogears import validators, validate
from turbogears import redirect
from turbogears import config

import time

import cherrypy
import pkg_resources

from tinyerp import rpc
from tinyerp import common
import xmlrpclib
import base64
from tinyerp.subcontrollers import actions
from tinyerp import CONFIG_FILE

conf = config.ConfigObj(CONFIG_FILE, unrepr=True, interpolation=True)

class MySchema(validators.Schema):
    host = validators.String(not_empty=True)
    port = validators.Int(not_empty=True)
    protocol = validators.String(not_empty=True)
    oldpwd = validators.OneOf([conf.get('etiny', {}).get('passwd', '')])
    newpwd = validators.String()
    repwd = validators.String()
    chained_validators = [validators.RequireIfPresent(present='oldpwd',required='newpwd'), validators.FieldsMatch('newpwd', 'repwd')]
    
class Admin(controllers.Controller):

    @expose(template="tinyerp.subcontrollers.templates.admin")
    def index(self, message='', id=None, db='', url='', selectedDb='', password=None, db_name=None, language=[], demo_data=False):
        
        if cherrypy.session.get('auth_check'):
            mode = cherrypy.session.get('auth_check')
        else:
            mode = id
                
        if demo_data:
            demo_data = eval(demo_data)
                                            
        url = rpc.session.get_url()
        url = str(url[:-1])
        
        langlist = []
        dblist = []
        
        try:
            langlist = rpc.session.execute_db('list_lang') or []
        except Exception, e:
            pass
        
        spwd = cherrypy.session.get('terp_passwd')
        db = cherrypy.request.simple_cookie.get('terp_db')

        try:
            dblist = rpc.session.execute_db('list')
        except:
            pass

        langlist.append(('en_EN','English'))

        host = config.get('host', path="tinyerp")
        port = config.get('port', path="tinyerp")
        protocol = config.get('protocol', path="tinyerp")
        comp_url = config.get('company_url', path='etiny')
        
        return dict(langlist=langlist, passwd=spwd, dblist=dblist, selectedDb=selectedDb,
                    db=db, url=url, db_name=db_name, demo_data=demo_data,
                    password=password, message=message, mode=mode, host=host,
                    port=port, protocol=protocol, comp_url=comp_url)

    @expose()
    def login(self, **kw):
        
        confpass = conf.get('etiny', {}).get('passwd', '')
        cherrypy.session['auth_check'] = ''
        
        passwd = kw.get('passwd')        
        
        if passwd:
            if passwd == confpass:
                cherrypy.session['terp_passwd'] = passwd
                raise redirect("/admin")
            else:
                message = str(_('Invalid Password...!'))
                raise common.error(_('Error'), _(message))
        
        if confpass:
            cherrypy.session['auth_check'] = 'authorize'            
            auth = 'connect_config'
            raise redirect("/admin")
            
        if confpass == "":
            raise common.error(_("Error"), _("Administration password is empty..!"))
    
    @validate(validators=MySchema())
    @expose(template="tinyerp.subcontrollers.templates.admin")
    def setconf(self, new_logo, tg_errors=None, **kw):
        mode = ''
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
       
        if comp_url and not comp_url.startswith('http'):
            comp_url = 'http://'+comp_url

        if tg_errors:
            return dict(mode='db_config', message=None, passwd=None, host=host, port=port, protocol=protocol, comp_url=comp_url)

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

        cherrypy.session['terp_passwd'] = None

        raise redirect("/admin")
            
    @expose()
    def createdb(self, langlist=[], password=None, db_name=None, language=[], demo_data=False):
                
        if not db_name:
            return

        message = None
        res = None
    
        if ((not db_name) or (not re.match('^[a-zA-Z][a-zA-Z0-9_]+$', db_name))):
            message = _('The database name must contain only normal characters or "_".\nYou must avoid all accents, space or special characters.') + "\n\n" + _('Bad database name !')
        else:
            try:
                res = rpc.session.execute_db('create', password, db_name, demo_data, language)
        
                time.sleep(5) # wait for few seconds
            except Exception, e:
                if ('faultString' in e and e.faultString=='AccessDenied:None') or str(e)=='AccessDenied':
                    message = _('Bad database administrator password !') + "\n\n" + _("Could not create database.")
                else:
                    message = _("Could not create database.") + "\n\n" + _('Error during database creation !')
            
            if res:        
                raise redirect("/admin")
            else:
                raise common.error(_('Error'), _(message))
            
    @expose()
    def dropdb(self, db='', dblist=None, db_name=None, passwd=None):
        
        message=None
        res = None

        if not db_name:
            return
        
        try:
            res = rpc.session.execute_db('drop', passwd, db_name)
        except Exception, e:
            if ('faultString' in e and e.faultString=='AccessDenied:None') or str(e)=='AccessDenied':
                message = _('Bad database administrator password !') + "\n\n" + _("Could not drop database.")
            else:
                message = _("Couldn't drop database")

        if res:        
            raise redirect("/admin")
        else:
            raise common.error(_('Error'), _(message))
    
    @expose()
    def backupdb(self, password=None, dblist=None):

        if not dblist:
            return

        message=None
        res = None

        try:
            res = rpc.session.execute_db('dump', password, dblist)
        except Exception, e:
            message = _("Could not create backup.")

        if res:
            cherrypy.response.headers['Content-Type'] = "application/data"
            return base64.decodestring(res)
        else:
            raise common.error(_('Error'), _(message))
        
        raise redirect("/admin")
   
    @expose()
    def restoredb(self, passwd=None, new_db=None, path=None):

        if path is None:
            return

        message = None
        res = None

        try:
            data_b64 = base64.encodestring(path.file.read())
            res = rpc.session.execute_db('restore', passwd, new_db, data_b64)
        except Exception, e:
            if e.faultString=='AccessDenied:None':
                message = _('Bad database administrator password !') + "\n\n" + _("Could not restore database.")
            else:
                message = _("Couldn't restore database")

        if res:        
            raise redirect("/admin")
        else:
            raise common.error(_('Error'), _(message))
    
    @expose()
    def passworddb(self, new_passwd=None, old_passwd=None, new_passwd2=None):

        message = None
        res = None

        if not new_passwd:
            return
        
        if new_passwd != new_passwd2:
            message = _("Confirmation password do not match with new password, operation cancelled !") + "\n\n" + _("Validation Error.")
        else:
            try:
                res = rpc.session.execute_db('change_admin_password', old_passwd, new_passwd)
            except Exception,e:
                if e.faultString=='AccessDenied:None':
                    message = _("Could not change password database.") + "\n\n" + _('Bas password provided !')
                else:
                    message = _("Error, password not changed.")

        if res:        
            raise redirect("/admin")
        else:
            raise common.error(_('Error'), _(message))

# vim: ts=4 sts=4 sw=4 si et

