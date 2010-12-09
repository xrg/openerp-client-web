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

from openerp.utils import rpc
from openerp.utils import TinyDict
from openerp.utils import expr_eval

from openerp.widgets.screen import Screen

from openerp.widgets import TinyInputWidget
from openerp.widgets import register_widget

from openerp import validators


__all__ = ["M2M"]


class M2M(TinyInputWidget):

    template = "/openerp/widgets/form/templates/many2many.mako"
    params = ['relation', 'domain', 'context']
    member_widgets = ['screen']

    valign = "top"

    relation = None
    domain = []
    context = {}

    def __init__(self, **attrs):
        super(M2M, self).__init__(**attrs)

        ids = None
        params = getattr(cherrypy.request, 'terp_params', None)
        if not params:
            params = TinyDict()
            params.model = attrs.get('relation', 'model')
            params.ids = attrs.get('value', [])
            params.name = attrs.get('name', '')

        current = params.chain_get(self.name)
        if current and params.source == self.name:
            ids = current.ids

        self.model = attrs.get('relation', 'model')
        self.link = attrs.get('link', None)
        self.onchange = None # override onchange in js code

        self.relation = attrs.get('relation', '')
        self.domain = attrs.get('domain', [])
        self.context = attrs.get('context', {}) or {}        

        view = attrs.get('views', {})
        mode = str(attrs.get('mode', 'tree,form')).split(',')

        self.view = view

        view_mode = mode
        view_type = mode[0]

        self.switch_to = view_mode[-1]
        if view_type == view_mode[-1]: self.switch_to = view_mode[0]

        if ids is None:
            ids = attrs.get('value', [])

        id = (ids or None) and ids[0]
        
        pprefix = ''
        if '/' in self.name:
            pprefix = self.name[:self.name.rindex('/')]
        
        if self.name == params.source and params.sort_key and ids:
            self.domain.append(('id', 'in', ids))
            ids = rpc.RPCProxy(self.model).search(self.domain, 0, 0, params.sort_key+ ' '+params.sort_order, self.context)
            id = ids[0]
        current = params.chain_get(self.name)

        if not current:
            current = TinyDict()

        current.offset = current.offset or 0
        current.limit = current.limit or 50
        current.count = len(ids or [])

        if current.view_mode: view_mode = current.view_mode
        if current.view_type: view_type = current.view_type

        if current and params.source == self.name:
            id = current.id

        id = id or None

        current.model = self.model
        current.id = id

        if isinstance(ids, tuple):
            ids = list(ids)

        current.ids = ids or []
        current.view_mode = view_mode
        current.view_type = view_type
        current.domain = current.domain or []
        current.context = current.context or {}

        if isinstance(self.context, basestring):
            # XXX: parent record for O2M
            #if self.parent:
            #    ctx['parent'] = EvalEnvironment(self.parent)

            try:
                ctx = expr_eval(
                        self.context,
                        dict(cherrypy.request.terp_record,
                             context=current.context,
                             active_id=current.id or False))
                current.context.update(ctx)
            except:
                pass

        if current.view_type == 'tree' and self.readonly:
            self.editable = False

        if self.editable is False:
            selectable = 0
        else:
            selectable = 2

        # try to get original input values if creating validation form
        if not params.filter_action:
            try:
                current.ids = eval(cherrypy.request.terp_data.get(self.name))
            except:
                pass

        self.screen = Screen(current, prefix=self.name, views_preloaded=view,
                             editable=self.editable, readonly=self.editable,
                             selectable=selectable, nolinks=self.link, **{'_m2m': 1})

        self.screen.widget.checkbox_name = False
        self.screen.widget.m2m = True

        self.validator = validators.many2many()

    def set_value(self, value):

        ids = value
        if isinstance(ids, basestring):
            if not ids.startswith('['):
                ids = '[' + ids + ']'
            ids = eval(ids)

        self.ids = ids
        self.screen.ids = ids

    def get_value(self):
        return [(6, 0, self.ids or [])]

register_widget(M2M, ["many2many"])


# vim: ts=4 sts=4 sw=4 si et
