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

from search import Search
from screen import Screen
from sidebar import Sidebar

from openobject.widgets import Form, CSSLink, JSLink, locations

class ViewForm(Form):

    template = "templates/viewform.mako"

    params = ['limit', 'offset', 'count', 'search_domain', 'search_data', 'filter_domain']
    member_widgets = ['screen', 'search', 'sidebar']

    css = [CSSLink("openerp", "css/autocomplete.css")]
    javascript = [JSLink("openerp", "javascript/form.js", location=locations.bodytop),
                  JSLink("openerp", "javascript/form_state.js", location=locations.bodytop),
                  JSLink("openerp", "javascript/m2o.js", location=locations.bodytop),
                  JSLink("openerp", "javascript/m2m.js", location=locations.bodytop),
                  JSLink("openerp", "javascript/o2m.js", location=locations.bodytop),
                  JSLink("openerp", "javascript/openerp/openerp.ui.textarea.js", location=locations.bodytop),
                  JSLink("openerp", "javascript/binary.js", location=locations.bodytop)]

    def __init__(self, params, **kw):

        super(ViewForm, self).__init__(**kw)

        # save reference of params dictionary in requeste
        cherrypy.request.terp_params = params
        cherrypy.request.terp_fields = []

        editable = params.editable
        readonly = params.readonly

        if editable is None:
            editable = True

        if readonly is None:
            readonly = False
       
        self.is_dashboard = getattr(cherrypy.request, '_terp_dashboard', False)

        self.search = None
        search_param = params.search_domain or []
        if search_param:
            for element in params.domain:
                if element not in search_param:
                    if not isinstance(element,tuple):
                        search_param.append(element)
                    else:
                        key, op, value = element
                        search_param.append((key, op, value))
                        
        cherrypy.request.custom_search_domain = []
        cherrypy.request.custom_filter_domain = []
        
        if params.view_type in ('tree', 'graph'):
            self.search = Search(model=params.model, domain=search_param, context=params.context, values=params.search_data or {},
                                 filter_domain=params.filter_domain or [], search_view=params.search_view, group_by_ctx=params.group_by_ctx or [])
            
            cherrypy.request.custom_search_domain = self.search.listof_domain or []
            cherrypy.request.custom_filter_domain = self.search.custom_filter_domain or []
            params.search_domain = self.search.listof_domain
            params.filter_domain = self.search.custom_filter_domain            
            params.group_by_ctx = self.search.groupby
            
        self.screen = Screen(prefix='', hastoolbar=True, hassubmenu=True, editable=editable, readonly=readonly,
                             selectable=params.selectable or 2)
        
        if self.screen.toolbar:
            self.sidebar = Sidebar(self.screen.model, self.screen.submenu, self.screen.toolbar, self.screen.id,
                                   self.screen.view_type, context=self.screen.context)

        if params.view_type == 'tree':
            self.screen.id = False

        # get the correct view title
        self.screen.string = getattr(cherrypy.request, '_terp_view_name', self.screen.string) or self.screen.string

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


# vim: ts=4 sts=4 sw=4 si et
