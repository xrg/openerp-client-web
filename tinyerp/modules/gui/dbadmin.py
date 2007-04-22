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

import re

from turbogears import expose
from turbogears import widgets
from turbogears import controllers
from turbogears import redirect
import time

import cherrypy

from tinyerp import rpc
from tinyerp import common
import xmlrpclib
import base64


class DBAdmin(controllers.Controller):

    @expose(template="tinyerp.modules.gui.templates.dbadmin")
    def index(self, host, port):
        return dict(host=host, port=port)

    @expose(template="tinyerp.modules.gui.templates.dbadmin_create")
    def create(self, host='', port='', password='', db_name='', language=[], demo_data=False, *args, **kw):

        action=kw.get('submit','')
        message=''
        langlist=[]
        url = 'http://'
        url += "%s:%s/xmlrpc"%(host, str(port))

        sock = xmlrpclib.ServerProxy(url + '/db')

        langlist = sock.list_lang()
        langlist.append( ('en_EN','English') )

        if action=='':
            return dict(host=host, port=port, langlist=langlist, message=message)

        db_name=db_name
        language = language
        password=password
        demo_data=demo_data
        res=''

        try:
            res = sock.create(password, db_name, demo_data, language)
        except Exception, e:
                if e.faultString=='AccessDenied:None':
                    message = str(_('Bad database administrator password !')+ _("Could not create database."))
                else:
                    message = str(_("Could not create database.")+_('Error during database creation !'))


        if res:
            raise redirect("/dbadmin?host=" + host + "&&port=" + port)

        return dict(host=host, port=port, langlist=langlist, message=message)

    @expose(template="tinyerp.modules.gui.templates.dbadmin_drop")
    def drop(self, host, port, db_name='', passwd='', *args, **kw):


        message=''
        db= cherrypy.request.simple_cookie.get('terp_db','')
        dblist = rpc.session.list_db(host, port)
        action = kw.get('submit','')

        if dblist == -1:
            dblist = []

        if action=='':
            return dict(host=host, port=port, selectedDb=db, message=message, dblist=dblist)

        passwd=passwd
        res = ''
        url = 'http://'
        url += "%s:%s/xmlrpc"%(host, str(port))
        sock = xmlrpclib.ServerProxy(url + '/db')

        try:
            res = sock.drop(passwd,db_name)
        except Exception, e:
            message = str(_('Bad database administrator password !') + _("Could not drop database."))

        if res:
            raise redirect("/dbadmin?host=" + host + "&&port=" + port)

        return dict(host=host, port=port, selectedDb=db, message=message, dblist=dblist)

    @expose(template="tinyerp.modules.gui.templates.dbadmin_backup")
    def backup(self, host='', port='', password='', dblist='', *args, **kw):

        dblist_load = rpc.session.list_db(host, port)
        message=''
        db= cherrypy.request.simple_cookie.get('terp_db','')
        action=kw.get('submit','')

        if action=='':
            return dict(host=host, port=port, dblist=dblist_load, selectedDb=db, message=message)


        url = "http://%s:%s"%(host, str(port))


        res = ''

        sock = xmlrpclib.ServerProxy(url + '/xmlrpc/db')

        db = cherrypy.request.simple_cookie['terp_db'].value

        try:
            res = sock.dump(password, dblist)
            dump = base64.decodestring(res)

        except Exception, e:
            message = "Could not create backup..."
        if res:
            cherrypy.response.headers['Content-Type'] = "application/data"
            return dump

        return dict(host=host, port=port, dblist=dblist_load, selectedDb=db, message=message)

    @expose(template="tinyerp.modules.gui.templates.dbadmin_restore")
    def restore(self,host='', port='', passwd='', new_db='', *args, **kw):

        message=''
        action = kw.get('submit','')

        if action=='':
            return dict(host=host, port=port, message=message)

        new_db = new_db
        passwd=passwd
        path=kw.get('path')
        action = kw.get('submit')
        res=''

        try:
            url = 'http://'
            url += "%s:%s/xmlrpc"%(host, str(port))
            sock = xmlrpclib.ServerProxy(url + '/db')
            data_b64 = base64.encodestring(path.file.read())
            res = sock.restore(passwd, new_db, data_b64)
        except Exception,e:
            if e.faultString=='AccessDenied:None':
                message = str(_('Bad database administrator password !'))+ str(_("Could not restore database."))
            else:
                message = str(_("Couldn't restore database"))

        if res:
            raise redirect("/dbadmin?host=" + host + "&&port=" + port)

        return dict(host=host, port=port, message=message)

    @expose(template="tinyerp.modules.gui.templates.dbadmin_password")
    def password(self, new_passwd='', old_passwd='', new_passwd2='', host='', port='', *args, **kw):

        action = kw.get('submit','')
        message=''

        if action=='':
            return dict(host=host, port=port, message=message)

        old_passwd = old_passwd
        new_passwd = new_passwd
        new_passwd2 = new_passwd2
        res=''

        if new_passwd != new_passwd2:
            message = str(_("Confirmation password do not match new password, operation cancelled!")+ _("Validation Error."))
        else:
            try:
                  url = 'http://'
                  url += "%s:%s/xmlrpc"%(host, str(port))
                  sock = xmlrpclib.ServerProxy(url + '/db')
                  res = sock.change_admin_password(old_passwd, new_passwd)
            except Exception,e:
                if e.faultString=='AccessDenied:None':
                    message = str(_("Could not change password database.")+_('Bas password provided !'))
                else:
                    message = str(_("Error, password not changed."))
        if res:
            raise redirect("/dbadmin?host=" + host + "&&port=" + port)

        return dict(host=host, port=port, message=message)
