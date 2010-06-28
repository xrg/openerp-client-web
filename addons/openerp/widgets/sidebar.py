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

from openerp.utils import rpc
from openerp.utils import TinyDict

from openobject.widgets import JSSource
from openerp.widgets import TinyWidget

from screen import Screen


class Sidebar(TinyWidget):

    template = "templates/sidebar.mako"
    params = ['reports', 'actions', 'relates', 'attachments', 'sub_menu', 'view_type', 'model']

    def __init__(self, model, submenu=None, toolbar=None, id=None, view_type="form", multi=True, context={}, **kw):

        super(Sidebar, self).__init__(model=model, id=id)
        self.multi = multi
        self.context = context or {}
        self.view_type = view_type
        act = 'client_action_multi'
        toolbar = toolbar or {}
        submenu = submenu
        self.reports = toolbar.get('print', [])
        self.actions = toolbar.get('action', [])
        self.relates = toolbar.get('relate', [])

        self.attachments = []
        self.sub_menu = None

        proxy = rpc.RPCProxy('ir.values')

        if self.view_type == 'form':
            act = 'tree_but_action'

        actions = proxy.get('action', act, [(self.model, False)], False, self.context)
        actions = [a[-1] for a in actions]

        ids = [a['id'] for a in self.actions]
        for act in actions:
            if act['id'] not in ids:
                act['context'] = self.context
                self.actions.append(act)

        reports = proxy.get('action', 'client_print_multi', [(self.model, False)], False, self.context)
        reports = [a[-1] for a in reports]

        ids = [a['id'] for a in self.reports]
        for rep in reports:
            if rep['id'] not in ids:
                rep['context'] = self.context
                self.reports.append(rep)

        if self.view_type == 'form' and id:

            proxy = rpc.RPCProxy('ir.attachment')
            ids = proxy.search([('res_model', '=', model), ('res_id', '=', id)], 0, 0, 0, self.context)

            if ids:
                attach = []
                datas = proxy.read(ids, ['datas_fname', 'name'])
                self.attachments = [(d['id'], d['name']) for d in datas]

            self.sub_menu = submenu

# vim: ts=4 sts=4 sw=4 si et
