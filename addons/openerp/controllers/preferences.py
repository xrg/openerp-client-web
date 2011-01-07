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
import cherrypy
import openerp.utils.common
import openerp.utils.rpc
from openobject.tools import expose, redirect

from openerp.utils import rpc, TinyDict, cache

import database
from form import Form

class PrefsPassword(database.FormPassword):
    action = "/openerp/pref/password"
    string = _('Change your password')

class Preferences(Form):

    _cp_path = "/openerp/pref"

    @expose(template="/openerp/controllers/templates/preferences/index.mako")
    def create(self, saved=False):

        tg_errors = None
        proxy = rpc.RPCProxy('res.users')
        action_id = proxy.action_get({})

        action = rpc.RPCProxy('ir.actions.act_window').read([action_id], False, rpc.session.context)[0]

        view_ids=[]
        if action.get('views', []):
            view_ids=[x[0] for x in action['views']]
        elif action.get('view_id', False):
            view_ids=[action['view_id'][0]]

        params = TinyDict()
        params.id = rpc.session.uid
        params.ids = [params.id]
        params.model = 'res.users'
        params.view_type = 'form'
        params.view_mode = ['form']
        params.view_ids = view_ids

        params.string = _('Preferences')

        params.editable = True
        form = self.create_form(params, tg_errors)

        return dict(form=form, params=params, editable=True, saved=saved)

    @expose(methods=('POST',))
    def ok(self, **kw):
        params, data = TinyDict.split(kw)
        proxy = rpc.RPCProxy('res.users')
        proxy.write([rpc.session.uid], data)
        rpc.session.context_reload()
        raise redirect('/openerp/pref/create', saved=True)

    @expose(template='/openerp/controllers/templates/preferences/password.mako')
    def password(self, old_password='', new_password='', confirm_password=''):
        context = {'form': PrefsPassword(), 'errors': []}
        if cherrypy.request.method != 'POST':
            return context

        if not (old_password.strip() and new_password.strip() and confirm_password.strip()):
            context['errors'].append(_('All passwords have to be filled.'))
        if new_password != confirm_password:
            context['errors'].append(_('The new password and its confirmation must be identical.'))
        if context['errors']: return context

        try:
            if openerp.utils.rpc.RPCProxy('res.users').change_password(
                    old_password, new_password, rpc.session.context):
                rpc.session.password = new_password
                return dict(context, changed=True)
            context['errors'].append(
                _('Could not change your password.'))
        except openerp.utils.common.AccessDenied:
            context['errors'].append(_('Original password incorrect, your password was not changed.'))
        return context

    @expose()
    def clear_cache(self):
        cache.clear()
        raise redirect('/')
