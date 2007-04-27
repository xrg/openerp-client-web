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
import xml.dom.minidom

import turbogears as tg
import cherrypy

from tinyerp import rpc
from tinyerp import tools

import treegrid

class ViewTree(tg.widgets.Form):
    template = """
    <form xmlns:py="http://purl.org/kid/ns#" method="post" id="${name}" name="${name}" action="${action}">
        <span py:for="field in hidden_fields" py:replace="field.display(value_for(field), **params_for(field))"/>
        <span py:if="tree" py:replace="tree.display(value_for(tree), **params_for(tree))"/>
    </form>
    """

    member_widgets = ['tree']

    def __init__(self, view, model, res_id=False, domain=[], context={}, action=None):

        super(ViewTree, self).__init__(name='tree_view', action=action)

        self.model = view['model']
        self.domain2 = domain
        self.context = context

        self.domain = []

        if 'field_parent' in view:
            self.domain = domain

        self.view = view

        proxy = rpc.RPCProxy(self.model)
        ids = proxy.search(self.domain2)

        ctx = context;
        ctx.update(rpc.session.context)

        fields = proxy.fields_get(False, ctx)
        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))

        root = dom.childNodes[0]
        attrs = tools.node_attributes(root)
        self.string = attrs.get('string', 'Unknown')

        self.headers = []

        self.parse(root, fields)

        self.tree = treegrid.TreeGrid(name="treegrid", model=self.model, headers=self.headers, url="/tree/data", selectable=True, domain=self.domain)

    def parse(self, root, fields=None):

        for node in root.childNodes:

            if not node.nodeType==node.ELEMENT_NODE:
                continue

            attrs = tools.node_attributes(node)

            name = attrs['name']
            field = fields.get(name)
            field.update(attrs)

            self.headers += [[name, field]]
