###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
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

from turbogears import widgets
from interface import TinyField

class TreeGrid(TinyField):

    template = "tinyerp.widgets.templates.treegrid"
    params = ['ids', 'url', 'model', 'headers', 'field_parent', 'onopen', 
              'onselection', 'domain', 'context', 'show_headers', 'url_params']

    selectable = False
    show_headers = True

    onopen = None
    onselection = None

    css = [widgets.CSSLink("tinyerp", "css/treegrid.css")]
    javascript = [widgets.JSLink("tinyerp", "javascript/treegrid.js")]

    def __init__(self, name, model, headers, url, field_parent=None, ids=[], domain=[], context={}, **kw):
        attrs = dict(name=name, model=model, url=url)

        super(TreeGrid, self).__init__(attrs)
        
        self.ids = ids
        self.model = model
        self.url = url

        self.domain = domain
        self.context = context
        
        self.headers = jsonify.encode(headers)
        self.field_parent = field_parent
        
        self.url_params = dict(model=str(model), domain=str(domain), context=str(context), field_parent=str(field_parent))
        for k, v in kw.items():
            self.url_params[k] = str(v)
            