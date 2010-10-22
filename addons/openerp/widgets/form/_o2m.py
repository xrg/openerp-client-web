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
import time

import cherrypy
from openerp.utils import TinyDict, expr_eval, rpc
from openerp.widgets import TinyInputWidget, register_widget
from openerp.widgets.screen import Screen

__all__ = ["O2M"]


class O2M(TinyInputWidget):
    """One2Many widget
    """
    template = "/openerp/widgets/form/templates/one2many.mako"
    params = ['id', 'parent_id', 'new_attrs', 'pager_info', 'switch_to', 'default_get_ctx', 'source', 'view_type']
    member_widgets = ['screen']

    form = None
    valign = "top"

    def __init__(self, **attrs):
        #FIXME: validation error in `Pricelist Version`
        attrs['required'] = False

        super(O2M, self).__init__(**attrs)

        self.new_attrs = { 'text': _("New"), 'help': _('Create new record.')}
        self.default_get_ctx = attrs.get('default_get', {}) or attrs.get('context', {})


        # get top params dictionary
        params = cherrypy.request.terp_params
        self.source = params.source
        pprefix = ''
        if '/' in self.name:
            pprefix = self.name[:self.name.rindex('/')]

        pparams = params.chain_get(pprefix)
        if (pparams and not pparams.id) or (not pparams and not params.id):
            self.new_attrs = { 'text': _("Save/New"), 'help': _('Save parent record.')}

        self.parent_id = params.id
        if pparams:
            self.parent_id = pparams.id

        # get params for this field
        current = params.chain_get(self.name)

        self.model = attrs['relation']
        self.link = attrs.get('link', '')
        self.onchange = None # override onchange in js code

        view = attrs.get('views', {})
        mode = str(attrs.get('mode', 'tree,form')).split(',')

        self.view = view

        view_mode = mode
        view_type = mode[0]
        self.view_type = view_type
        
        if not current:
            current = TinyDict()

        if current.view_mode: view_mode = current.view_mode
        if current.view_type: view_type = current.view_type

        self.switch_to = view_mode[-1]
        if view_type == view_mode[-1]: self.switch_to = view_mode[0]
        
        ids = attrs.get('value') or []
        
        if not isinstance(ids, list):
            ids = [ids]

        if ids:
            if isinstance(ids[0], dict):
                ids = []
            elif isinstance(ids[0], tuple):
                ids = [current[1] for current in ids]
        
        id = (ids or None) and ids[0]
        
        if self.name == self.source or self.name == params.source:
            if params.sort_key and ids:
                domain = current.domain or []
                domain.append(('id', 'in', ids))
                ids = rpc.RPCProxy(self.model).search(domain, current.offset, current.limit, params.sort_key + ' '+params.sort_order, current.context)
                id = ids[0]
        if current and params.source and self.name in params.source.split('/'):
            id = current.id

        id = id or None
                
        current.model = self.model
        current.id = id
        current.ids = ids
        current.view_mode = view_mode
        current.view_type = view_type
        current.domain = current.domain or []
        current.context = current.context or {}

        group_by_ctx = ''

        if self.default_get_ctx:
            ctx = dict(cherrypy.request.terp_record,
                       context=current.context,
                       active_id=self.parent_id or False)

            # XXX: parent record for O2M
            #if self.parent:
            #    ctx['parent'] = EvalEnvironment(self.parent)

            try:
                ctx = expr_eval("dict(%s)" % self.default_get_ctx, ctx)
                current.context.update(ctx)
            except:
                pass

            if ctx and ctx.get('group_by'):
                group_by_ctx = ctx.get('group_by')

        current.offset = current.offset or 0
        current.limit = current.limit or 20
        current.count = len(ids or [])

        # Group By for one2many list.
        if group_by_ctx:
            current.group_by_ctx = group_by_ctx
            current.domain = [('id', 'in', ids)]

        if current.view_type == 'tree' and self.readonly:
            self.editable = False
        
        self.screen = Screen(current, prefix=self.name, views_preloaded=view,
                             editable=self.editable, readonly=self.readonly,
                             selectable=0, nolinks=self.link, _o2m=1)
        
        self.id = id
        self.ids = ids

        if view_type == 'tree':
            self.id = None

        elif view_type == 'form':
            records_count = len(self.screen.ids or [])

            current_record = 0
            if records_count and self.screen.id in self.screen.ids:
                current_record = self.screen.ids.index(self.screen.id) + 1
                self.pager_info = _('%d of %d') % (current_record, records_count)
            else:
                self.pager_info = _('- of %d') % (records_count)

    def get_value(self):

        if not self.ids:
            return []

        values = getattr(self.screen.widget, 'values', [])

        return [(1, val.get('id', False), val) for val in values]

register_widget(O2M, ["one2many", "one2many_form", "one2many_list"])
