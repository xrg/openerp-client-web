###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the 
# Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
# Boston, MA  02111-1307, USA.
#
###############################################################################

import cherrypy
import turbogears as tg

from tinyerp.widgets_search.search import Search

from screen import Screen
from sidebar import Sidebar

class ViewForm(tg.widgets.Form):

    template = "tinyerp.widgets.templates.viewform"

    params = ['limit', 'offset', 'count', 'search_domain', 'search_data']
    member_widgets = ['screen', 'search']    
    javascript = [tg.widgets.JSLink("tinyerp", "javascript/form.js", location=tg.widgets.js_location.bodytop),
                  tg.widgets.JSLink("tinyerp", "javascript/form_state.js", location=tg.widgets.js_location.bodytop),
                  tg.widgets.JSLink("tinyerp", "javascript/m2o.js", location=tg.widgets.js_location.bodytop),
                  tg.widgets.JSLink("tinyerp", "javascript/charts.js", location=tg.widgets.js_location.bodytop),
                  tg.widgets.JSLink("tinyerp", "javascript/swfobject.js", location=tg.widgets.js_location.bodytop)]

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
            
        self.screen = Screen(prefix='', hastoolbar=True, editable=editable, readonly=readonly, selectable=2)
        self.sidebar = Sidebar(self.screen.model, self.screen.toolbar, self.screen.view_type != 'form', self.screen.context)
        
        self.search = None
        
        if params.view_type in ('tree', 'graph'):
            self.search = Search(model=params.model, domain=params.domain, context=params.context, values=params.search_data or {})
            
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

