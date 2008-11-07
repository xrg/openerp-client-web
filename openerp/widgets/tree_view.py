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
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import xml.dom.minidom

import turbogears as tg
import cherrypy

from openerp import rpc
from openerp import tools
from openerp import cache

from sidebar import Sidebar

import treegrid

class ViewTree(tg.widgets.Form):
    template = "openerp.widgets.templates.viewtree"
    params = ['model', 'id', 'ids', 'domain', 'context', 'view_id', 'toolbar']
    member_widgets = ['tree', 'sidebar']

    def __init__(self, view, model, res_id=False, domain=[], context={}, action=None):
        super(ViewTree, self).__init__(name='view_tree', action=action)

        self.model = view['model']
        self.domain2 = domain or []
        self.context = context or {}

        self.domain = []

        self.field_parent = view.get("field_parent") or None

        if self.field_parent:
            self.domain = domain

        self.view = view
        self.view_id = view['view_id']

        proxy = rpc.RPCProxy(self.model)

        ctx = self.context.copy();
        ctx.update(rpc.session.context)

        fields = cache.fields_get(self.model, False, ctx)
        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))

        root = dom.childNodes[0]
        attrs = tools.node_attributes(root)
        self.string = attrs.get('string', 'Unknown')
        self.toolbar = attrs.get('toolbar', False)

        ids = []
        id = res_id

        if self.toolbar:
            ids = proxy.search(self.domain2, 0, 0, 0, ctx)
            self.toolbar = proxy.read(ids, ['name', 'icon'], ctx)

            if not id and ids: 
                id = ids[0]

            if id: 
                ids = proxy.read([id], [self.field_parent])[0][self.field_parent]
        elif not ids:
            ids = proxy.search(domain, 0, 0, 0, ctx)

        self.headers = []
        self.parse(root, fields)

        self.tree = treegrid.TreeGrid(name="tree", 
                                      model=self.model, 
                                      headers=self.headers, 
                                      url="/tree/data", 
                                      ids=ids, 
                                      domain=self.domain, 
                                      context=self.context, 
                                      field_parent=self.field_parent)
        self.id = id
        self.ids = ids

        #register callbacks
        self.tree.onselection = "onSelection"
        self.tree.onheaderclick = "onHeaderClick"
        
        toolbar = {}
        for item, value in view.get('toolbar', {}).items():
            if value: toolbar[item] = value
            
        self.sidebar = Sidebar(self.model, toolbar, True, True, context=self.context)

    def parse(self, root, fields=None):

        for node in root.childNodes:

            if not node.nodeType==node.ELEMENT_NODE:
                continue

            attrs = tools.node_attributes(node)

            field = fields.get(attrs['name'])
            field.update(attrs)

            self.headers += [field]
            
# vim: ts=4 sts=4 sw=4 si et

