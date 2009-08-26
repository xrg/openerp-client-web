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

import time

import cherrypy

from openerp import tools
from openerp import rpc
from openerp.utils import TinyDict

from interface import TinyInputWidget
from screen import Screen

class O2M(TinyInputWidget):
    """One2Many widget
    """
    template = "templates/one2many.mako"
    params = ['id', 'parent_id', 'new_attrs', 'pager_info', 'switch_to', 'default_get_ctx']
    member_widgets = ['screen']

    form = None

    def __init__(self, **attrs):
        #FIXME: validation error in `Pricelist Version`
        attrs['required'] = False

        super(O2M, self).__init__(**attrs)

        self.new_attrs = { 'text': _("New"), 'help': _('Create new record.')}
        self.default_get_ctx = attrs.get('default_get', {}) or attrs.get('context', {})

#        self.colspan = 4
#        self.nolabel = True

        # get top params dictionary
        params = cherrypy.request.terp_params

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

        if not current:
            current = TinyDict()

        if current.view_mode: view_mode = current.view_mode
        if current.view_type: view_type = current.view_type

        self.switch_to = view_mode[-1]
        if view_type == view_mode[-1]: self.switch_to = view_mode[0]
        
        ids = attrs.get('value') or []
        if not isinstance(ids, list):
            ids = [ids]
            
        id = (ids or None) and ids[0]
        
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

        if self.default_get_ctx:
            ctx = cherrypy.request.terp_record
            ctx['current_date'] = time.strftime('%Y-%m-%d')
            ctx['time'] = time
            ctx['context'] = current.context
            ctx['active_id'] = self.parent_id or False

            # XXX: parent record for O2M
            #if self.parent:
            #    ctx['parent'] = EvalEnvironment(self.parent)

            try:
                ctx = tools.expr_eval("dict(%s)" % self.default_get_ctx, ctx)
                current.context.update(ctx)
            except:
                pass

        current.offset = current.offset or 0
        current.limit = current.limit or 20
        current.count = len(ids or [])

        if current.view_type == 'tree' and self.readonly:
            self.editable = False

        self.screen = Screen(current, prefix=self.name, views_preloaded=view,
                             editable=self.editable, readonly=self.readonly,
                             selectable=0, nolinks=self.link)
        self.id = id
        self.ids = ids

        if view_type == 'tree':
            #self.screen.widget.pageable=False
            self.id = None

        pager_info = None
        if view_type == 'form':
            c = (self.screen.ids or 0) and len(self.screen.ids)
            i = 0

            if c and self.screen.id in self.screen.ids:
                i = self.screen.ids.index(self.screen.id) + 1

            self.pager_info = '[%s/%s]' % (i, c)

    def get_value(self):

        if not self.ids:
            return []
        
        values = getattr(self.screen.widget, 'values', [])
        
        return [(1, val.get('id', False), val) for val in values]

# vim: ts=4 sts=4 sw=4 si et

