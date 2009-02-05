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
import turbogears as tg

from openerp.widgets_search.search import Search

from screen import Screen
from sidebar import Sidebar

class ViewForm(tg.widgets.Form):

    template = "openerp.widgets.templates.viewform"

    params = ['limit', 'offset', 'count', 'search_domain', 'search_data']
    member_widgets = ['screen', 'search', 'sidebar']    
    javascript = [tg.widgets.JSLink("openerp", "javascript/form.js", location=tg.widgets.js_location.bodytop),
                  tg.widgets.JSLink("openerp", "javascript/form_state.js", location=tg.widgets.js_location.bodytop),
                  tg.widgets.JSLink("openerp", "javascript/m2o.js", location=tg.widgets.js_location.bodytop),
                  tg.widgets.JSLink("openerp", "javascript/m2m.js", location=tg.widgets.js_location.bodytop),
                  tg.widgets.JSLink("openerp", "javascript/o2m.js", location=tg.widgets.js_location.bodytop),
                  tg.widgets.JSLink("openerp", "javascript/textarea.js", location=tg.widgets.js_location.bodytop),
                  tg.widgets.JSLink("openerp", "javascript/binary.js", location=tg.widgets.js_location.bodytop),
                  tg.widgets.JSLink("openerp", "javascript/charts.js", location=tg.widgets.js_location.bodytop),
                  tg.widgets.JSLink("openerp", "javascript/swfobject.js", location=tg.widgets.js_location.bodytop)]

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
            
        self.screen = Screen(prefix='', hastoolbar=True, editable=editable, readonly=readonly, 
                             selectable=params.selectable or 2)

        self.sidebar = Sidebar(self.screen.model, self.screen.toolbar, self.screen.id, 
                               self.screen.view_type, self.screen.view_type != 'form', 
                               self.screen.context)

        self.is_dashboard = getattr(cherrypy.request, '_terp_dashboard', False)
        
        self.search = None
        
        if params.view_type in ('tree', 'graph'):
            self.search = Search(model=params.model, domain=params.domain, 
                                 context=params.context, values=params.search_data or {})
            
        if params.view_type == 'tree':
            self.screen.id = False
            
        if params.context and '_view_name' in params.context:
            self.screen.string = params.context.get('_view_name')

        # get the actual pager data
        self.limit = self.screen.limit
        self.offset = self.screen.offset        
        self.count = self.screen.count
        
        self.search_domain = params.search_domain
        self.search_data = params.search_data
        
        self.fields = cherrypy.request.terp_fields
        
# vim: ts=4 sts=4 sw=4 si et


