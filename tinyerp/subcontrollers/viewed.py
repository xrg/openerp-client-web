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

import random
from xml import dom, xpath

from turbogears import expose
from turbogears import controllers
from turbogears import validators

import cherrypy

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp.tinyres import TinyResource

import tinyerp.widgets as tw

class ViewEd(controllers.Controller, TinyResource):
    
    @expose(template="tinyerp.subcontrollers.templates.viewed")
    def default(self, view_id):
        
        view_id = int(view_id)
        
        proxy = rpc.RPCProxy('ir.ui.view')
        res = proxy.read(view_id, ['model'])
        
        model = res['model']
        
        headers = [{'string' : 'Name', 'name' : 'name', 'type' : 'char'}]
        tree = tw.treegrid.TreeGrid('view', model=model, headers=headers, url='/viewed/data?view_id='+str(view_id))
        tree.show_headers = False

        return dict(model=model, tree=tree, show_header_footer=False)
    
    def view_get(self, view_id=None):
        
        def _inherit_apply(src, inherit, inherited_id):
            def _find(node, node2):
                # Check if xpath query or normal inherit (with field matching)
                if node2.nodeType==node2.ELEMENT_NODE and node2.localName=='xpath':
                    res = xpath.Evaluate(node2.getAttribute('expr'), node)
                    return res and res[0]
                else:
                    if node.nodeType==node.ELEMENT_NODE and node.localName==node2.localName:
                        res = True
                        for attr in node2.attributes.keys():
                            if attr=='position':
                                continue
                            if node.hasAttribute(attr):
                                if node.getAttribute(attr)==node2.getAttribute(attr):
                                    continue
                            res = False
                        if res:
                            return node
                    for child in node.childNodes:
                        res = _find(child, node2)
                        if res: return res
                return None

            doc_src = dom.minidom.parseString(src)
            doc_dest = dom.minidom.parseString(inherit)
            for node2 in doc_dest.childNodes:
                if not node2.nodeType==node2.ELEMENT_NODE:
                    continue
                node = _find(doc_src, node2)
                if node:
                    vnode = doc_dest.createElement('view')
                    vnode.setAttribute('view_id', str(inherited_id))
                    vnode.appendChild(node2)
                    node.appendChild(vnode)
                else:
                    attrs = ''.join([
                        ' %s="%s"' % (attr, node2.getAttribute(attr)) 
                        for attr in node2.attributes.keys() 
                        if attr != 'position'
                    ])
                    tag = "<%s%s>" % (node2.localName, attrs)
                    raise AttributeError, "Couldn't find tag '%s' in parent view !" % tag
            return doc_src.toxml(encoding="utf-8").replace('\t', '')
        
        proxy = rpc.RPCProxy('ir.ui.view')
        res = proxy.read(view_id)

        def _inherit_apply_rec(result, inherit_id):
            # get all views which inherit from (ie modify) this view
            inherit_ids = proxy.search([('inherit_id', '=', inherit_id)], 0, 0, 'priority')
            inherit_res = proxy.read(inherit_ids, ['arch', 'id'])
            
            for res2 in inherit_res:
                result = _inherit_apply(result, res2['arch'], res2['id'])
                result = _inherit_apply_rec(result, res2['id'])
            
            return result
        
        doc_arch = _inherit_apply_rec(res['arch'], view_id)
        doc_arch = dom.minidom.parseString(doc_arch)
        
        new_doc = dom.getDOMImplementation().createDocument(None, 'view', None)
        new_doc.documentElement.setAttribute('view_id', str(view_id))
        new_doc.documentElement.appendChild(doc_arch.documentElement)
        
        return res['model'], new_doc.toxml(encoding="utf-8").replace('\t', '')
    
    def parse(self, root=None, view_id=False):

        result = []
    
        for node in root.childNodes:
            
            if not node.nodeType==node.ELEMENT_NODE:
                continue
                        
            attrs = tools.node_attributes(node)
            attrs['view_id'] = attrs.get('view_id', view_id)
        
            attrs['__random_id__'] = random.randrange(1, 1000)
            attrs.setdefault('name', node.localName)
            
            children = []
            
            if node.childNodes:
                children = self.parse(node)
            
            result += [_NODES.get(node.localName, Node)(attrs, children)]
            
        return result
    
    @expose('json')
    def data(self, view_id, **kw):
        view_id = int(view_id)
        
        model, view = self.view_get(view_id)
        
        doc = dom.minidom.parseString(view.encode('utf-8'))
        result = self.parse(root=doc)
        
        records = [rec.get_record() for rec in result]
        
        return dict(records=records)
    
class Node(object):
    
    def __init__(self, attrs, children=None):
        self.attrs = attrs or {}
        self.children = children
        
        self.id = self.attrs['__random_id__']
        self.name = self.get_name()
        
    def get_name(self):
        return "<%s>" % self.attrs['name']
    
    def get_record(self):
        record = {
            'id' : self.id,
            'data' : {'name' : self.name}}
        
        if self.children:
            record['children'] = [c.id for c in self.children]
            record['child_records'] = [c.get_record() for c in self.children]

        return record

class ViewNode(Node):
    
    def get_name(self):
        return '<view view_id="%s">' % self.attrs.get('view_id', False)
    
class FieldNode(Node):
    
    def get_name(self):
        return '[%s]' % self.attrs['name']

_NODES = {
    'view' : ViewNode,
    'field': FieldNode
}
