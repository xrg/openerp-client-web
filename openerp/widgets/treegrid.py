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

