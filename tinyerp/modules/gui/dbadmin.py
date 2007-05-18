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
from tinyerp.modules import actions


class DBAdmin(controllers.Controller):

    @expose(template="tinyerp.modules.gui.templates.dbadmin")
    def index(self):
        return dict()

    @expose(template="tinyerp.modules.gui.templates.dbadmin_create")
    def create(self, password=None, db_name=None, language=[], demo_data=False):

        url = rpc.session.get_url()
        url = str(url[:-1])
        langlist = rpc.session.execute_db('list_lang')
        langlist.append(('en_EN','English'))

        if not db_name:
            return dict(url=url, langlist=langlist, message=None)

        res=None

        if ((not db_name) or (not re.match('^[a-zA-Z][a-zA-Z0-9_]+$', db_name))):
            message = str(_('The database name must contain only normal characters or "_".\nYou must avoid all accents, space or special characters.') + _('Bad database name !'))
        else:
            try:
                res = rpc.session.execute_db('create', password, db_name, demo_data, language)
            except Exception, e:
                message = str(_('Bad database administrator password !') + _("Could not create database."))

        if res !=-1:
            raise redirect("/dbadmin")
        else:
            message = str(_('Bad database administrator password !') + _("Could not create database."))

        return dict(url=url, langlist=langlist, message=message)

    @expose(template="tinyerp.modules.gui.templates.dbadmin_drop")
    def drop(self, db_name=None, passwd=None):
        message=None

        url = rpc.session.get_url()
        url = str(url[:-1])
        db = cherrypy.request.simple_cookie.get('terp_db')
        dblist = rpc.session.execute_db('list')

        if dblist == -1:
            dblist = []

        if not db_name:
            return dict(url=url, selectedDb=db, message=message, dblist=dblist)

        try:
            res = rpc.session.execute_db('drop', passwd, db_name)
        except Exception, e:
            message = str(_('Bad database administrator password !') + _("Could not drop database."))

        if res != -1:
            raise redirect("/dbadmin")
        else:
            message = str(_('Bad database administrator password !') + _("Could not drop database."))

        return dict(url=url, selectedDb=db, message=message, dblist=dblist)

    @expose(template="tinyerp.modules.gui.templates.dbadmin_backup")
    def backup(self, password=None, dblist=None):

        url = rpc.session.get_url()
        url = str(url[:-1])
        db= cherrypy.request.simple_cookie.get('terp_db')

        dblist_load = rpc.session.execute_db('list')
        message=None

        if not dblist:
            return dict(url=url, dblist=dblist_load, selectedDb=db, message=message)

        try:
            res = rpc.session.execute_db('dump', password, dblist)
            dump = base64.decodestring(res)
        except Exception, e:
            message = "Could not create backup..."

        if res != -1:
            cherrypy.response.headers['Content-Type'] = "application/data"
            return dump
        else:
            message = "Could not create backup..."

        return dict(url=url, dblist=dblist_load, selectedDb=db, message=message)

    @expose(template="tinyerp.modules.gui.templates.dbadmin_restore")
    def restore(self, passwd=None, new_db=None, path=None):

        url = rpc.session.get_url()
        url = str(url[:-1])
        message=None

        if path is None:
            return dict(url=url, message=message)

        try:
            data_b64 = base64.encodestring(path.file.read())
            res = rpc.session.execute_db('restore', passwd, new_db, data_b64)
        except Exception, e:
            if e.faultString=='AccessDenied:None':
                message = str(_('Bad database administrator password !'))+ str(_("Could not restore database."))
            else:
                message = str(_("Couldn't restore database"))

        if res != -1:
            raise redirect("/dbadmin")
        else:
            message = str(_('Bad database administrator password !'))+ str(_("Could not restore database."))


        return dict(url=url, message=message)

    @expose(template="tinyerp.modules.gui.templates.dbadmin_password")
    def password(self, new_passwd=None, old_passwd=None, new_passwd2=None):

        url = rpc.session.get_url()
        url = str(url[:-1])
        message=None

        if not new_passwd:
            return dict(url=url, message=message)

        if new_passwd != new_passwd2:
            message = str(_("Confirmation password do not match new password, operation cancelled!")+ _("Validation Error."))
        else:
            try:
                res = rpc.session.execute_db('change_admin_password', old_passwd, new_passwd)
            except Exception,e:
                if e.faultString=='AccessDenied:None':
                    message = str(_("Could not change password database.")+_('Bas password provided !'))
                else:
                    message = str(_("Error, password not changed."))

        if res != -1:
            raise redirect("/dbadmin")
        else:
            message = str(_("Could not change password database.")+_('Bad password provided !'))

        return dict(url=url, message=message)
