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
import cherrypy
from openerp.controllers import SecuredController
from openerp.utils import rpc

from openobject.tools import expose, redirect


class Shortcuts(SecuredController):

    _cp_path = "/openerp/shortcuts"

    def my(self):

        if not rpc.session.is_logged():
            return []

        sc = cherrypy.session.get('terp_shortcuts', False)
        if not sc:
            proxy = rpc.RPCProxy('ir.ui.view_sc')
            sc = proxy.get_sc(rpc.session.uid, 'ir.ui.menu', rpc.session.context) or []

            cherrypy.session['terp_shortcuts'] = sc

        for x in sc:
            if isinstance(x['res_id'], (list, tuple)):
                x['res_id'] = x['res_id'][0]

        return sc
        
    @expose()
    def default(self):
        import actions
        domain = [('user_id', '=', rpc.session.uid), ('resource', '=', 'ir.ui.menu')]
        return actions.execute_window(False, 'ir.ui.view_sc', res_id=None, domain=domain, view_type='form', mode='tree,form')
    
    @expose()
    def add(self, id):
        id = int(id)
        proxy = rpc.RPCProxy('ir.ui.view_sc')

        sc = cherrypy.session.get('terp_shortcuts', False)
        
        if sc:
            for s in sc:
                if isinstance(s['res_id'], tuple):
                    if s['res_id'][0] == id:
                        raise redirect('/openerp/tree/open', id=id, model='ir.ui.menu')
                elif s['res_id'] == id:
                    raise redirect('/openerp/tree/open', id=id, model='ir.ui.menu')
        
        name = rpc.RPCProxy('ir.ui.menu').name_get([id], rpc.session.context)[0][1]
        proxy.create({'user_id': rpc.session.uid, 'res_id': id, 'resource': 'ir.ui.menu', 'name': name})

        sc = proxy.get_sc(rpc.session.uid, 'ir.ui.menu', rpc.session.context)
        cherrypy.session['terp_shortcuts'] = sc
        
        raise redirect('/openerp/tree/open', id=id, model='ir.ui.menu')

# vim: ts=4 sts=4 sw=4 si et
