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

from openerp.utils import rpc, expr_eval, TinyDict
from openerp.widgets import screen, TinyInputWidget, register_widget


__all__ = ["Action"]


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

        self.act_id= self.name
        
        proxy = rpc.RPCProxy("ir.actions.actions")
        res = proxy.read([self.act_id], ['type'], rpc.session.context)
        if not res:
            raise _('Action not found!')

        _type=res[0]['type']
        self.action = rpc.session.execute('object', 'execute', _type, 'read', [self.act_id], False, rpc.session.context)[0]

        if 'view_mode' in attrs:
            self.action['view_mode'] = attrs['view_mode']

        if self.action['type']=='ir.actions.act_window':

            if not self.action.get('domain', False):
                self.action['domain']='[]'

            ctx = dict(rpc.session.context,
                       active_id=False,
                       active_ids=[])

            self.context = expr_eval(self.action.get('context', '{}'), ctx)
            self.domain = expr_eval(self.action['domain'], ctx)
            views = dict(map(lambda x: (x[1], x[0]), self.action['views']))
            view_mode = self.action.get('view_mode', 'tree,form').split(',')
            view_ids = map(lambda x: views.get(x, False), view_mode)
            
            if views.keys() != view_mode:
                view_mode = map(lambda x: x[1], self.action['views'])
                view_ids = map(lambda x: x[0], self.action['views'])
            
            if self.action['view_type'] == 'form':

                params = TinyDict()
                params.updateAttrs(
                    model=self.action['res_model'],
                    id=False,
                    ids=None,
                    view_ids=view_ids,
                    view_mode=view_mode,
                    context=self.context,
                    domain=self.domain,
                    offset = 0,
                    limit = 20
                )

                # get pager vars if set
                if hasattr(cherrypy.request, 'terp_params'):
                    current = cherrypy.request.terp_params
                    current = current.chain_get(self.name or '') or current

                    params.updateAttrs(
                        offset=current.offset,
                        limit=current.limit
                    )

                self.screen = screen.Screen(params, prefix=self.name, editable=True, selectable=3)

            elif self.action['view_type']=='tree':
                pass #TODO

register_widget(Action, ["action"])

# vim: ts=4 sts=4 sw=4 si et
