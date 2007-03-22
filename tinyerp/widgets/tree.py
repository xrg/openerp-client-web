###############################################################################
#
# Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
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
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################################################

"""
This modules implements custom widget controles like:
    - Tree

@todo: multicolumn TreeView (or TreeTable)
"""

import pkg_resources

from turbogears import expose

from turbogears.widgets import CSSLink
from turbogears.widgets import JSLink
from turbogears.widgets import Widget
from turbogears.widgets import FormField, InputWidget
from turbogears.widgets import register_static_directory
from turbogears.widgets import CalendarDateTimePicker
from turbogears.widgets import CalendarDatePicker

from tinyerp import rpc

tinyerp_static_dir = pkg_resources.resource_filename("tinyerp",  "static")
register_static_directory("tinyerp", tinyerp_static_dir)

class Tree(Widget):
    """Tree Widget

    @todo: refine the tree, especialy for how to get children
    """

    template = "tinyerp.widgets.templates.tree"

    css=[CSSLink("tinyerp", "css/xtree.css")]
    javascript = [JSLink("tinyerp", "javascript/xtree.js"), JSLink("tinyerp", "javascript/xloadtree.js")]

    params = ['id', 'title', 'model', 'url', 'action', 'target']
    params_doc = {
                  'id': 'Widget id',
                  'title': 'Root Title of the tree',
                  'model': 'TinyERP model from where data should be fetched',
				  'url' : 'Source URL that will be called to fetch tree data in JSON or XML format',
                  'action': 'action url, called when tree item is clicked',
                  'target': 'target window'
                  }


    @staticmethod
    @expose('json')
    def items(tg_obj, model, id, action='', target=''):
        """This static method should be used to define controller methods.

        @param tg_obj: the controller object, just ignore this
        @param model: TinyERP model from where data should be fetched
        @param id: parent node id
        @param action: action url, called when tree item is clicked
        @param target: target window

        @return: JSON object of all the child nodes
        """

        proxy = rpc.RPCProxy(model)
        id = int(id)

        menu_ids = []

        if id == -1:
            menu_ids = proxy.search([('parent_id','=',False)])
        else:
            menu_ids = proxy.read([id], ['child_id'])[0]['child_id']

        res = proxy.read(menu_ids, ['name', 'child_id', 'icon'])

        nodes = []
        for r in res:
            node = {'text': r['name']}
            if r['child_id']:
                node['src'] = "/menu_items/%s/%d?action=%s&target=%s"%(model, r['id'], action, target)

            if action:
                node['action'] = "%s/%s/%d" %(action, model, r['id'])

            if target:
                node['target'] = target

            #icon = r['icon']
            #if icon.startswith('STOCK_'):
            #    icon = "/static/images/stock/%s.png" % (icon.lower())
            #else:
            #    icon = "/static/images/%s.png" % (icon.lower())

            #node['icon'] = icon
            #node['openIcon'] = icon

            nodes += [node]

        return dict(tree=nodes);
