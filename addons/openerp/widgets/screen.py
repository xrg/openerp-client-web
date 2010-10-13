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
from openerp.utils import cache

from openerp.widgets import TinyInputWidget


class Screen(TinyInputWidget):

    template = """
        <input type="hidden" id="${name}_terp_model" name="${name}_terp_model" value="${model}"/>
        <input type="hidden" id="${name}_terp_state" name="${name}_terp_state" value="${state}"/>
        <input type="hidden" id="${name}_terp_id" name="${name}_terp_id" value="${id}"/>
        <input type="hidden" id="${name}_terp_ids" name="${name}_terp_ids" value="${ids}"/>

        <input type="hidden" id="${name}_terp_view_ids" name="${name}_terp_view_ids" value="${view_ids}"/>
        <input type="hidden" id="${name}_terp_view_mode" name="${name}_terp_view_mode" value="${view_mode}"/>
        <input type="hidden" id="${name}_terp_view_type" name="${name}_terp_view_type" value="${view_type}"/>
        <input type="hidden" id="${name}_terp_view_id" name="${name}_terp_view_id" value="${view_id}"/>
        <input type="hidden" id="${name}_terp_domain" name="${name}_terp_domain" value="${domain}"/>
        <input type="hidden" id="${name}_terp_context" name="${name}_terp_context" value="${ctx}"/>
        <input type="hidden" id="${name}_terp_editable" name="${name}_terp_editable" value="${editable}"/>

        <input type="hidden" id="${name}_terp_limit" name="${name}_terp_limit" value="${limit}"/>
        <input type="hidden" id="${name}_terp_offset" name="${name}_terp_offset" value="${offset}"/>
        <input type="hidden" id="${name}_terp_count" name="${name}_terp_count" value="${count}"/>
        <input type="hidden" id="${name}_terp_group_by_ctx" name="${name}_terp_group_by_ctx" value="${group_by_ctx}"/>
        <input type="hidden" id="${name}_terp_filters_context" name="${name}_terp_filters_context" value=""/>

        % if widget:
            ${display_member(widget)}
        % endif
    """

    params = ['model', 'state', 'id', 'ids', 'view_id', 'view_ids', 'view_mode', 'view_type', 'domain',
              'context', 'limit', 'offset', 'count', 'group_by_ctx']

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
        self.group_by_ctx  = params.group_by_ctx or []        
        self.is_wizard = params.is_wizard
        
        self.m2m = kw.get('_m2m', 0)
        self.o2m = kw.get('_o2m', 0)
        
        while len(self.view_ids) < len(self.view_mode):
            self.view_ids += [False]

        if not self.view_type and params.view_mode:
            self.view_type = params.view_mode[0]

        if self.view_ids and self.view_type in self.view_mode:
            idx = self.view_mode.index(self.view_type)
            self.view_id = self.view_ids[idx]

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
            view = cache.fields_view_get(self.model, view_id, view_type, ctx, self.hastoolbar, self.hassubmenu)

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

        self.hastoolbar = (toolbar or False) and True
        self.hassubmenu = (submenu or False) and True

# vim: ts=4 sts=4 sw=4 si et
