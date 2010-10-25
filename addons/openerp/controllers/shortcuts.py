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
from openerp.controllers import SecuredController
from openerp.utils import rpc

from openobject.tools import expose, redirect


class Shortcuts(SecuredController):

    _cp_path = "/openerp/shortcuts"

    def refresh_session(self):
        ''' refresh_session() -> [{id, name, res_id}]

        Fetches the list of ir.ui.menu shortcuts from the server, stores them
        in session and returns the list.

        Returns only the id of the resource, not the retrieved (id, name_get())
        '''
        shortcuts = rpc.RPCProxy('ir.ui.view_sc')\
            .get_sc(rpc.session.uid, 'ir.ui.menu', rpc.session.context) or []
        for shortcut in shortcuts:
            # if res_id is (id, name), only keep id
            if isinstance(shortcut['res_id'], (list, tuple)):
                shortcut['res_id'] = shortcut['res_id'][0]
        cherrypy.session['terp_shortcuts'] = shortcuts
        return shortcuts

    def list(self):
        return cherrypy.session.get('terp_shortcuts', [])

    def by_res_id(self):
        ''' dict_by_res_id() -> {int: {}}
        Returns a dictionary of {shortcut id, shortcut name} indexed by res_id
        '''
        return dict([
            (shortcut['res_id'], {'id': shortcut['id'], 'name': shortcut['name']})
            for shortcut in self.list()])

    def my(self):
        if not rpc.session.is_logged():
            return []
        # return the shortcuts we have in session, or if none
        # (empty list or no list at all) go fetch them from the server
        return self.list() or self.refresh_session()

    @expose()
    def default(self):
        import actions
        domain = [('user_id', '=', rpc.session.uid), ('resource', '=', 'ir.ui.menu')]
        return actions.execute_window(False, 'ir.ui.view_sc', res_id=None, domain=domain, view_type='form', mode='tree,form')

    @expose('json')
    def by_resource(self):
        return self.by_res_id()

    @expose(methods=('POST',))
    def add(self, id):
        id = int(id)

        if not self.by_res_id().get(id):
            name = rpc.RPCProxy('ir.ui.menu').name_get([id], rpc.session.context)[0][1]
            rpc.RPCProxy('ir.ui.view_sc').create({'user_id': rpc.session.uid, 'res_id': id, 'resource': 'ir.ui.menu', 'name': name})
            self.refresh_session()

        raise redirect('/openerp/tree/open', id=id, model='ir.ui.menu')
    
    @expose(methods=('POST',))
    def delete(self, id):
        id = int(id)

        shortcut = self.by_res_id().get(id)
        if shortcut:
            rpc.RPCProxy('ir.ui.view_sc').unlink(shortcut['id'])
            self.refresh_session()

        raise redirect('/openerp/tree/open', id=id, model='ir.ui.menu')

# vim: ts=4 sts=4 sw=4 si et
