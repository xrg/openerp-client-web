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

import simplejson

from interface import TinyWidget
from resource import CSSLink, JSLink


class TreeGrid(TinyWidget):

    template = "templates/treegrid.mako"
    params = ['headers', 'showheaders', 'expandall', 'onselection', 'onbuttonclick', 'onheaderclick', 'url', 'url_params']

    css = [CSSLink("openerp", "css/treegrid.css")]
    javascript = [JSLink("openerp", "javascript/treegrid.js")]
    
    ids = None
    domain = None
    context = None
    field_parent = None
    
    #def __init__(self, name, model, headers, url, field_parent=None, ids=[], domain=[], context={}, **kw):
    def __init__(self, **attrs):
        
        name = attrs['name']
        model = attrs['model']
        headers = attrs['headers']
        url = attrs['url']
        
        super(TreeGrid, self).__init__(**attrs)
        
        self.ids = self.ids or []
        self.domain = self.domain or []
        self.context = self.context or {}
        
        self.headers = simplejson.dumps(headers)
        
        fields = [field['name'] for field in headers]
        icon_name = headers[0].get('icon')
        
        url_params = attrs.copy()
        
        url_params.pop('name', None)
        url_params.pop('headers', None)
        url_params.pop('url', None)
        
        url_params['domain'] = ustr(self.domain)
        url_params['context'] = ustr(self.context)
        url_params['fields'] = ustr(fields)
        url_params['icon_name'] = icon_name
                
        def _jsonify(obj):
            
            for k, v in obj.items():
                if isinstance(v, dict):
                    obj[k] = _jsonify(v)
            
            return simplejson.dumps(obj)
        
        self.url_params = _jsonify(url_params)
                
        self.showheaders = attrs.get('showheaders', 1)
        self.onselection = attrs.get('onselection')
        self.onbuttonclick = attrs.get('onbuttonclick')
        self.onheaderclick = attrs.get('onheaderclick')
        self.expandall = attrs.get('expandall', 0)
        
# vim: ts=4 sts=4 sw=4 si et

