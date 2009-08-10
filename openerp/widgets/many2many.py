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

from interface import TinyInputWidget

from form import Form
from listgrid import List

from openerp import rpc
from openerp import cache
from openerp import tools

from screen import Screen
from openerp.utils import TinyDict

from openerp import validators

class M2M(TinyInputWidget):

    template = "templates/many2many.mako"
    params = ['relation', 'domain', 'context']
    member_widgets = ['screen']

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

        self.domain  = attrs.get('domain',{})

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

        current = params.chain_get(self.name)

        if not current:
            current = TinyDict()

        current.offset = current.offset or 0
        current.limit = current.limit or 20
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
            ctx = cherrypy.request.terp_record
            ctx['current_date'] = time.strftime('%Y-%m-%d')
            ctx['time'] = time
            ctx['context'] = current.context
            ctx['active_id'] = current.id or False

            # XXX: parent record for O2M
            #if self.parent:
            #    ctx['parent'] = EvalEnvironment(self.parent)

            try:
                ctx = tools.expr_eval(self.context, ctx)
                current.context.update(ctx)
            except:
                pass

        if current.view_type == 'tree' and self.readonly:
            self.editable = False

        if self.editable is False:
            selectable = 0
        else:
            selectable = 2
            
        try: # try to get original input values if creating validation form
            current.ids = eval(cherrypy.request.terp_data.get(self.name))
        except:
            pass

        self.screen = Screen(current, prefix=self.name, views_preloaded=view,
                             editable=False, readonly=self.editable,
                             selectable=selectable, nolinks=self.link)

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

# vim: ts=4 sts=4 sw=4 si et

