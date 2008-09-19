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

from turbojson import jsonify

import turbogears

from turbogears import widgets
from interface import TinyField

class TreeGrid(TinyField):

    template = "openerp.widgets.templates.treegrid"
    params = ['headers', 'showheaders', 'expandall', 'onselection', 'onbuttonclick', 'onheaderclick', 'url', 'url_params']

    css = [widgets.CSSLink("openerp", "css/treegrid.css")]
    javascript = [widgets.JSLink("openerp", "javascript/treegrid.js")]

    def __init__(self, name, model, headers, url, field_parent=None, ids=[], domain=[], context={}, **kw):
        attrs = dict(name=name, model=model, url=url)
        super(TreeGrid, self).__init__(attrs)
        
        self.ids = ids
        self.model = model
        
        self.headers = jsonify.encode(headers)
        
        fields = [field['name'] for field in headers]
        icon_name = headers[0].get('icon')
        
        self.url = url
        self.url_params = dict(model=model, 
                                ids=ids,
                                fields=ustr(fields), 
                                domain=ustr(domain), 
                                context=ustr(context), 
                                field_parent=field_parent,
                                icon_name=icon_name)
        
        self.url_params.update(kw)
        
        def _jsonify(obj):
            
            for k, v in obj.items():
                if isinstance(v, dict):
                    obj[k] = _jsonify(v)
            
            return jsonify.encode(obj)
                
        self.url_params = _jsonify(self.url_params)
        
        self.domain = domain
        self.context = context
        
        self.showheaders = kw.get('showheaders', 1)
        self.onselection = kw.get('onselection')
        self.onbuttonclick = kw.get('onbuttonclick')
        self.onheaderclick = kw.get('onheaderclick')
        self.expandall = kw.get('expandall', 0)
        
# vim: ts=4 sts=4 sw=4 si et

