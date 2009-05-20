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

from openerp import icons
from openerp import tools
from openerp import rpc

import screen
from interface import TinyInputWidget
from openerp.utils import TinyDict

class Action(TinyInputWidget):
    template = """
    % if screen:
        ${display_member(screen)}
    % endif
    """

    params = ['string']
    member_widgets = ['screen']

    def __init__(self, **attrs):

        super(Action, self).__init__(**attrs)
        self.nolabel = True

        self.act_id=attrs['name']
        res = rpc.session.execute('object', 'execute', 'ir.actions.actions', 'read', [self.act_id], ['type'], rpc.session.context)
        if not res:
            raise _('Action not found!')

        type=res[0]['type']
        self.action = rpc.session.execute('object', 'execute', type, 'read', [self.act_id], False, rpc.session.context)[0]

        if 'view_mode' in attrs:
            self.action['view_mode'] = attrs['view_mode']

        if self.action['type']=='ir.actions.act_window':

            if not self.action.get('domain', False):
                self.action['domain']='[]'
            
            ctx = rpc.session.context.copy()
            ctx.update({'active_id': False, 'active_ids': []})
            
            self.context = tools.expr_eval(self.action.get('context', '{}'), ctx)
            self.domain = tools.expr_eval(self.action['domain'], ctx)

            views = dict(map(lambda x: (x[1], x[0]), self.action['views']))
            view_mode = self.action.get('view_mode', 'tree,form').split(',')
            view_ids = map(lambda x: views.get(x, False), view_mode)

            if self.action['view_type']=='form':

                params = TinyDict()
                params.model = self.action['res_model']
                params.id = False
                params.ids = None
                params.view_ids = view_ids
                params.view_mode = view_mode
                params.context = self.context
                params.domain = self.domain

                params.offset = params.offset or 0
                params.limit = params.limit or 20

                # get pager vars if set
                if hasattr(cherrypy.request, 'terp_params'):
                    current = cherrypy.request.terp_params
                    current = current.chain_get(self.name or '') or current

                    params.offset = current.offset
                    params.limit = current.limit

                self.screen = screen.Screen(params, prefix=self.name, editable=True, selectable=3)

            elif self.action['view_type']=='tree':
                pass #TODO

# vim: ts=4 sts=4 sw=4 si et

