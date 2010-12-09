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

from search import Search
from screen import Screen
from sidebar import Sidebar
from listgroup import ListGroup
from logs import Logs

from openobject.widgets import Form, JSLink, locations

class ViewForm(Form):

    template = "/openerp/widgets/templates/viewform.mako"

    params = ['limit', 'offset', 'count', 'search_domain', 'search_data', 'filter_domain', 'notebook_tab', 'context_menu']
    member_widgets = ['screen', 'search', 'sidebar', 'logs']

    def __init__(self, params, **kw):

        super(ViewForm, self).__init__(**kw)

        # save reference of params dictionary in requeste
        cherrypy.request.terp_params = params
        cherrypy.request.terp_fields = []
        self.notebook_tab = params.notebook_tab or 0
        self.context_menu = params.get('context_menu')
        editable = params.editable
        readonly = params.readonly

        if editable is None:
            editable = True

        if readonly is None:
            readonly = False
       
        self.is_dashboard = getattr(cherrypy.request, '_terp_dashboard', False)

        self.search = None
        search_param = params.search_domain or []
        params_domain = params.domain or []
        for element in params_domain:
            if element not in search_param:
                if not isinstance(element,tuple):
                    search_param.append(element)
                else:
                    key, op, value = element
                    search_param.append((key, op, value))

        cherrypy.request.custom_search_domain = []
        cherrypy.request.custom_filter_domain = []

        if params.view_type in ('tree', 'graph'):
            self.search = Search(source=params.source, model=params.model, domain=search_param, context=params.context, values=params.search_data or {},
                                 filter_domain=params.filter_domain or [], search_view=params.search_view, group_by_ctx=params.group_by_ctx or [],
                                 **{'clear': params.get('_terp_clear')})

            cherrypy.request.custom_search_domain = self.search.listof_domain or []
            cherrypy.request.custom_filter_domain = self.search.custom_filter_domain or []
            params.search_domain = self.search.listof_domain
            params.filter_domain = self.search.custom_filter_domain            
            params.group_by_ctx = self.search.groupby
            
        self.screen = Screen(prefix='', hastoolbar=True, hassubmenu=True, editable=editable, readonly=readonly,
                             selectable=params.selectable or 2)
        
        if self.screen.widget and self.screen.view_type in ['form', 'tree']:
            self.logs = Logs()
            
        if self.screen.widget and hasattr(self.screen.widget, 'sidebar'):
            self.sidebar = self.screen.widget.sidebar
        else:
            view_mode = self.screen.view_mode
            if  'form' in view_mode and view_mode.index('form') > 0:
                self.sidebar = Sidebar(self.screen.model, self.screen.submenu, self.screen.toolbar, self.screen.id,
                               self.screen.view_type, context=self.screen.context)

        if params.view_type == 'tree':
            self.screen.id = False
            
        if 'form' not in self.screen.view_mode and not isinstance(self.screen.widget, ListGroup):
            self.screen.widget.link = 0
            self.screen.editable = False
            self.screen.widget.editable = False

        # get the correct view title
        if params.context:
            self.screen.string = params.context.get('_terp_view_name', self.screen.string)
        self.screen.string = self.screen.string

        # get the actual pager data
        self.limit = self.screen.limit
        self.offset = self.screen.offset
        self.count = self.screen.count

        self.search_domain = params.search_domain
        self.search_data = params.search_data
        self.filter_domain = params.filter_domain or []
        
        if params.hidden_fields:
            self.hidden_fields = params.hidden_fields

        #self.fields = cherrypy.request.terp_fields
    def update_params(self, params):
        super(ViewForm, self).update_params(params)
        if self.search:            
            params['attrs']['onsubmit']='submit_search_form()'
        


# vim: ts=4 sts=4 sw=4 si et
