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

from tinyerp import icons
from tinyerp import tools
from tinyerp import rpc

from interface import TinyCompoundWidget

class Graph(TinyCompoundWidget):

    template = """<table width="100%">
        <tr>
            <td align="center">
                <img class="graph" src="/static/images/stock/gtk-no.png"/>
            </td>
        </tr>
    </table>
    """

    def __init__(self, model, view, ids=[], domain=[], context={}):
        self.model = model
        self.fields = view['fields']
        self.ids = ids
        self.domain = domain
        self.context = context

        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
        self.parse(root, self.fields)

        datas = []
        if self.ids:
            proxy = rpc.RPCProxy(self.model)
            ctx = rpc.session.context.copy()
            ctx.update(context)
            datas = proxy.read(self.ids, self.fields.keys(), ctx)

    def parse(self, root, fields):
        attrs = tools.node_attributes(root)
        self.string = attrs.get('string', 'Unknown')

        axis = []
        axis_data = {}
        for node in root.childNodes:
            node_attrs = tools.node_attributes(node)
            if node.localName == 'field':
                axis.append(str(node_attrs['name']))
                axis_data[str(node_attrs['name'])] = node_attrs

        self.axis = axis
        self.axis_data = axis_data
        self.graph_attrs = attrs

