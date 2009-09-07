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

from openerp import tools
from openerp import rpc
from openerp import cache

from interface import TinyInputWidget

import form
import graph
import listgrid

import tinycalendar

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

        % if widget:
            ${display_member(widget)}
        % endif
    """

    params = ['model', 'state', 'id', 'ids', 'view_id', 'view_ids', 'view_mode', 'view_type', 'domain', 'context', 'limit', 'offset', 'count']
    member_widgets = ['widget']

    def __init__(self, params=None, prefix='', name='', views_preloaded={}, hastoolbar=False, editable=False, readonly=False, selectable=0, nolinks=1):

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

        self.is_wizard = params.is_wizard

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
            self.count = rpc.RPCProxy(self.model).search_count(self.domain, self.context)

        self.prefix             = prefix
        self.views_preloaded    = views_preloaded or (params.views or {})

        self.hastoolbar         = hastoolbar
        self.toolbar            = None

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
            view = cache.fields_view_get(self.model, view_id, view_type, ctx, self.hastoolbar)

        self.add_view(view, view_type)

    def add_view(self, view, view_type='form'):

        self.view_id = view.get('view_id', self.view_id)

        if view_type == 'form':
            self.widget = form.Form(prefix=self.prefix,
                                    model=self.model,
                                    view=view,
                                    ids=(self.id or []) and [self.id],
                                    domain=self.domain,
                                    context=self.context,
                                    editable=self.editable,
                                    readonly=self.readonly,
                                    nodefault=self.nodefault, nolinks=self.link)

            if not self.is_wizard and self.ids is None:
                proxy = rpc.RPCProxy(self.model)
                self.ids = proxy.search(self.domain, self.offset or False, self.limit or False, 0, self.context)
                self.count = proxy.search_count(self.domain, self.context)

        elif view_type == 'tree':
            self.widget = listgrid.List(self.name or '_terp_list',
                                        model=self.model,
                                        view=view,
                                        ids=self.ids,
                                        domain=self.domain,
                                        context=self.context,
                                        editable=self.editable,
                                        selectable=self.selectable,
                                        offset=self.offset, limit=self.limit, count=self.count, nolinks=self.link)

            self.ids = self.widget.ids
            self.limit = self.widget.limit
            self.count = self.widget.count

        elif view_type == 'graph':
            self.widget = graph.Graph(model=self.model,
                                      view=view,
                                      view_id=view.get('view_id', False),
                                      ids=self.ids, domain=self.domain,
                                      context=self.context)
            self.ids = self.widget.ids

        elif view_type == 'calendar':
            self.widget = tinycalendar.get_calendar(view=view,
                                                    model=self.model,
                                                    ids=self.ids,
                                                    domain=self.domain,
                                                    context=self.context,
                                                    options=self.kalendar)

        elif view_type == 'gantt':
            self.widget = tinycalendar.GanttCalendar(model=self.model,
                                                     view=view,
                                                     ids=self.ids,
                                                     domain=self.domain,
                                                     context=self.context,
                                                     options=self.kalendar)

        self.string = (self.widget or '') and self.widget.string

        toolbar = {}
        for item, value in view.get('toolbar', {}).items():
            if value: toolbar[item] = value

        self.toolbar = toolbar or None
        self.hastoolbar = (toolbar or False) and True

# vim: ts=4 sts=4 sw=4 si et

