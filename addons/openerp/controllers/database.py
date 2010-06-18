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
# -   All names, links and logos of Tiny, Open ERP and Axelor must be
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
import base64
import re
import time

import cherrypy
from openerp import widgets, validators
from openerp.utils import rpc, common

from openobject.controllers import BaseController
from openobject.tools import url, expose, redirect, validate, error_handler


def get_lang_list():
    langs = [('en_US', 'English (US)')]
    try:
        return langs + (rpc.session.execute_db('list_lang') or [])
    except Exception, e:
        pass
    return langs

def get_db_list():
    try:
        return rpc.session.execute_db('list') or []
    except:
        return []

class DBForm(widgets.Form):
    strip_name = True

    def post_init(self, *args, **kw):
        if self.validator is validators.DefaultValidator:
            self.validator = validators.Schema()
        for f in self.fields:
            self.validator.add_field(f.name, f.validator)

    def update_params(self, d):
        super(DBForm, self).update_params(d)
        d.attrs['action'] = url(self.action)

class FormCreate(DBForm):
    name = "create"
    string = _('Create database')
    action = '/openerp/database/do_create'
    submit_text = _('OK')
    strip_name = True
    form_attrs = {'onsubmit': 'return on_create()'}
    fields = [widgets.PasswordField(name='password', label=_('Super admin password:'), validator=validators.NotEmpty()),
              widgets.TextField(name='dbname', label=_('New database name:'), validator=validators.NotEmpty()),
              widgets.CheckBox(name='demo_data', label=_('Load Demonstration data:'), default=True, validator=validators.Bool(if_empty=False)),
              widgets.SelectField(name='language', options=get_lang_list, validator=validators.String(), label=_('Default Language:')),
              widgets.PasswordField(name='admin_password', label=_('Administrator password:'), validator=validators.NotEmpty()),
              widgets.PasswordField(name='confirm_password', label=_('Confirm password:'), validator=validators.NotEmpty())
              ]
    validator = validators.Schema(chained_validators=[validators.FieldsMatch("admin_password","confirm_password")])

class FormDrop(DBForm):
    name = "drop"
    string = _('Drop database')
    action = '/openerp/database/do_drop'
    submit_text = _('OK')
    form_attrs = {'onsubmit': 'return window.confirm(_("Do you really want to drop the selected database?"))'}
    fields = [widgets.SelectField(name='dbname', options=get_db_list, label=_('Database:'), validator=validators.String(not_empty=True)),
              widgets.PasswordField(name='password', label=_('Password:'), validator=validators.NotEmpty())]

class FormBackup(DBForm):
    name = "backup"
    string = _('Backup database')
    action = '/openerp/database/do_backup'
    submit_text = _('OK')
    fields = [widgets.SelectField(name='dbname', options=get_db_list, label=_('Database:'), validator=validators.String(not_empty=True)),
              widgets.PasswordField(name='password', label=_('Password:'), validator=validators.NotEmpty())]

class FormRestore(DBForm):
    name = "restore"
    string = _('Restore database')
    action = '/openerp/database/do_restore'
    submit_text = _('OK')
    fields = [widgets.FileField(name="filename", label=_('File:')),
              widgets.PasswordField(name='password', label=_('Password:'), validator=validators.NotEmpty()),
              widgets.TextField(name='dbname', label=_('New database name:'), validator=validators.NotEmpty())]

class FormPassword(DBForm):
    name = "password"
    string = _('Change Administrator Password')
    action = '/openerp/database/do_password'
    submit_text = _('OK')
    fields = [widgets.PasswordField(name='old_password', label=_('Old Password:'), validator=validators.NotEmpty()),
              widgets.PasswordField(name='new_password', label=_('New Password:'), validator=validators.NotEmpty()),
              widgets.PasswordField(name='confirm_password', label=_('Confirm Password:'), validator=validators.NotEmpty())]

    validator = validators.Schema(chained_validators=[validators.FieldsMatch("new_password","confirm_password")])


_FORMS = {
    'create': FormCreate(),
    'drop': FormDrop(),
    'backup': FormBackup(),
    'restore': FormRestore(),
    'password': FormPassword()
}

class Database(BaseController):

    _cp_path = "/openerp/database"

    @expose()
    def index(self, *args, **kw):
        raise redirect('/openerp/database/create')

    @expose(template="templates/database.mako")
    def create(self, tg_errors=None, **kw):
        form = _FORMS['create']
        return dict(form=form)

    @expose()
    @validate(form=_FORMS['create'])
    @error_handler(create)
    def do_create(self, password, dbname, admin_password, confirm_password, demo_data=False, language=None, **kw):

        if not re.match('^[a-zA-Z][a-zA-Z0-9_]+$', dbname):
            raise common.warning(_('The database name must contain only normal characters or "_".\nYou must avoid all accents, space or special characters.'), _('Bad database name!'))

        ok = False
        try:
            res = rpc.session.execute_db('create', password, dbname, demo_data, language, admin_password)
            while True:
                try:
                    progress, users = rpc.session.execute_db('get_progress', password, res)
                    if progress == 1.0:
                        for x in users:
                            if x['login'] == 'admin':
                                rpc.session.login(dbname, 'admin', x['password'])
                                ok = True
                        break
                    else:
                        time.sleep(1)
                except:
                    raise Exception('DbFailed')
        except Exception, e:
            if e.args == ('DbExist',):
                raise common.warning(_("Could not create database."), _('Database already exists!'))
            elif e.args == ('DbFailed'):
                raise common.warning(_("The server crashed during installation.\nWe suggest you to drop this database."),
                                     _("Error during database creation!"))
            elif getattr(e, 'faultCode', False) == 'AccessDenied':
                raise common.warning(_('Bad database administrator password!'), _("Could not create database."))
            else:
                raise common.warning(_("Could not create database."))

        if ok:
            raise redirect('/openerp/menu', {'db': True})
        raise redirect('/openerp/login', db=dbname)

    @expose(template="templates/database.mako")
    def drop(self, tg_errors=None, **kw):
        form = _FORMS['drop']
        return dict(form=form)

    @expose()
    @validate(form=_FORMS['drop'])
    @error_handler(drop)
    def do_drop(self, dbname, password, **kw):
        try:
            rpc.session.execute_db('drop', password, dbname)
        except Exception, e:
            if getattr(e, 'faultCode', False) == 'AccessDenied':
                raise common.warning(_('Bad database administrator password!'), _("Could not drop database."))
            else:
                raise common.warning(_("Couldn't drop database"))

        raise redirect("/openerp/database/drop")

    @expose(template="templates/database.mako")
    def backup(self, tg_errors=None, **kw):
        form = _FORMS['backup']
        return dict(form=form)

    @expose()
    @validate(form=_FORMS['backup'])
    @error_handler(backup)
    def do_backup(self, dbname, password, **kw):
        try:
            res = rpc.session.execute_db('dump', password, dbname)
            if res:
                cherrypy.response.headers['Content-Type'] = "application/data"
                cherrypy.response.headers['Content-Disposition'] = 'filename="' + dbname + '.dump"';
                return base64.decodestring(res)
        except Exception, e:
            raise common.warning(_("Could not create backup."))

        raise redirect('/openerp/login')

    @expose(template="templates/database.mako")
    def restore(self, tg_errors=None, **kw):
        form = _FORMS['restore']
        return dict(form=form)

    @expose()
    @validate(form=_FORMS['restore'])
    @error_handler(restore)
    def do_restore(self, filename, password, dbname, **kw):
        try:
            data = base64.encodestring(filename.file.read())
            res = rpc.session.execute_db('restore', password, dbname, data)
        except Exception, e:
            if getattr(e, 'faultCode', False) == 'AccessDenied':
                raise common.warning(_('Bad database administrator password!'), _("Could not restore database."))
            else:
                raise common.warning(_("Couldn't restore database"))

        raise redirect('/openerp/login', db=dbname)

    @expose(template="templates/database.mako")
    def password(self, tg_errors=None, **kw):
        form = _FORMS['password']
        return dict(form=form)

    @validate(form=_FORMS['password'])
    @error_handler(password)
    @expose()
    def do_password(self, old_password, new_password, confirm_password, **kw):
        try:
            res = rpc.session.execute_db('change_admin_password', old_password, new_password)
        except Exception,e:
            if getattr(e, 'faultCode', False) == 'AccessDenied':
                raise common.warning(_("Could not change super admin password."), _('Bad password provided!'))
            else:
                raise common.warning(_("Error, password not changed."))

        raise redirect('/openerp/login')

# vim: ts=4 sts=4 sw=4 si et

