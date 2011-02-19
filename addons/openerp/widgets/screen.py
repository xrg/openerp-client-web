###############################################################################
#
#  Copyright (C) 2007-TODAY OpenERP SA. All Rights Reserved.
#
#  $Id$
#
#  Developed by OpenERP (http://openerp.com) and Axelor (http://axelor.com).
#
#  The OpenERP web client is distributed under the "OpenERP Public License".
#  It's based on Mozilla Public License Version (MPL) 1.1 with following 
#  restrictions:
#
#  -   All names, links and logos of OpenERP must be kept as in original
#      distribution without any changes in all software screens, especially
#      in start-up page and the software header, even if the application
#      source code has been changed or updated or code has been added.
#
#  You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################

import cherrypy

from openerp.utils import rpc
from openerp.utils import cache

from openerp.widgets import TinyInputWidget


class Screen(TinyInputWidget):

    template = "/openerp/widgets/templates/screen.mako"

    params = ['model', 'state', 'id', 'ids', 'view_id', 'view_ids', 'view_mode', 'view_type', 'domain',
              'context', 'limit', 'offset', 'count', 'group_by_ctx', 'action_id']

    member_widgets = ['widget']

    def __init__(self, params=None, prefix='', name='', views_preloaded={}, hastoolbar=False, hassubmenu=False, editable=False, readonly=False, selectable=0, nolinks=1, **kw):

        # get params dictionary
        params = params or cherrypy.request.terp_params
        prefix = prefix or (params.prefix or '')
        super(Screen, self).__init__(prefix=prefix, name=name)

        self.model         = params.model
        self.state         = params.state or None
        self.id            = params.id or False
        self.ids           = params.ids
        self.view_ids      = params.view_ids or []
        self.view_mode     = params.view_mode or []
        self.view_type     = params.view_type
        self.view_id       = False
        self.action_id     = params.action_id
        self.group_by_ctx  = params.group_by_ctx or []        
        self.is_wizard = params.is_wizard
        self.default_value = params.default_data or []
        
        self.m2m = kw.get('_m2m', 0)
        self.o2m = kw.get('_o2m', 0)
        self.is_dashboard = False
        if self.model == 'board.board' and self.view_type == 'form':
            self.is_dashboard = True
            
        while len(self.view_ids) < len(self.view_mode):
            self.view_ids += [False]

        if not self.view_type and params.view_mode:
            self.view_type = params.view_mode[0]

        if self.view_ids and self.view_type in self.view_mode:
            idx = self.view_mode.index(self.view_type)
            self.view_id = self.view_ids[idx]
 
        self.search_domain = params.search_domain or []
        self.domain        = params.domain or []
        self.context       = params.context or {}
        self.nodefault     = params.nodefault or False

        self.offset        = params.offset
        self.limit         = params.limit
        self.count         = params.count

        if (self.ids or self.id) and self.count == 0:
            if self.ids and len(self.ids) < self.limit:
                self.count = len(self.ids)
            else:
                self.count = rpc.RPCProxy(self.model).search_count(self.domain, self.context)
                
        self.prefix             = prefix
        self.views_preloaded    = views_preloaded or (params.views or {})

        self.hastoolbar         = hastoolbar
        self.toolbar            = None

        self.hassubmenu         = hassubmenu
        self.submenu            = None

        self.selectable         = selectable
        self.editable           = editable
        self.readonly           = readonly
        self.link               = nolinks

        # get calendar options
        self.kalendar           = params.kalendar
        if self.view_mode:
            self.add_view_id(self.view_id, self.view_type)

    def add_view_id(self, view_id, view_type):
        self.view_id = view_id

        if view_type in self.views_preloaded:
            view = self.views_preloaded[view_type]
        else:
            ctx = rpc.session.context.copy()
            ctx.update(self.context)
            if ctx.get('view_id'):
                view_id = ctx['view_id']
                if 'view_id' in cherrypy.request.terp_params['_terp_context']:
                    cherrypy.request.terp_params['_terp_context'].pop('view_id')
            view = cache.fields_view_get(self.model, view_id or False, view_type, ctx, self.hastoolbar, self.hassubmenu)

        self.add_view(view, view_type)

    def add_view(self, view, view_type='form'):

        self.view_id = view.get('view_id', self.view_id)
        self.view = view  
        
        from _views import get_view_widget
        self.widget = get_view_widget(view_type, self)

        self.string = (self.widget or '') and self.widget.string

        toolbar = {}
        for item, value in view.get('toolbar', {}).items():
            if value: toolbar[item] = value

        submenu = view.get('submenu', {})

        self.toolbar = toolbar or None
        self.submenu = eval(ustr(submenu)) or None

        self.hastoolbar = bool(toolbar)
        self.hassubmenu = bool(submenu)

# vim: ts=4 sts=4 sw=4 si et
