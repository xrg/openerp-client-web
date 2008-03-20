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
from turbogears import widgets as tg_widgets

import cherrypy

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp.tinyres import TinyResource

import tinyerp.widgets as tw

def _get_xpath(node):

    pn = node.parentNode
    xp = '/' + node.localName

    if pn and pn.localName and pn.localName != 'view':
        xp = _get_xpath(pn) + xp

    nodes = xpath.Evaluate(node.localName, node.parentNode)
    xp += '[%s]' % (nodes.index(node) + 1)

    return xp

class ViewEd(controllers.Controller, TinyResource):
    
    @expose(template="tinyerp.subcontrollers.templates.viewed")
    def default(self, view_id):

        try:
            view_id = eval(view_id)
        except:
            pass
        
        if isinstance(view_id, basestring) or not view_id:
            raise common.error(_("Error!"), _("Invalid view id."))
        
        proxy = rpc.RPCProxy('ir.ui.view')
        res = proxy.read(view_id, ['model'])
        
        model = res['model']
        
        headers = [{'string' : 'Name', 'name' : 'name', 'type' : 'char'}]
        tree = tw.treegrid.TreeGrid('view_tree', model=model, headers=headers, url='/viewed/data?view_id='+str(view_id))
        tree.show_headers = False
        tree.onselection = 'onSelect'

        return dict(view_id=view_id, model=model, tree=tree, show_header_footer=False)
    
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

            doc_src = dom.minidom.parseString(src.encode('utf-8'))
            doc_dest = dom.minidom.parseString(inherit.encode('utf-8'))
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
            return doc_src.toxml().replace('\t', '')
        
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
        doc_arch = dom.minidom.parseString(doc_arch.encode('utf-8'))
        
        new_doc = dom.getDOMImplementation().createDocument(None, 'view', None)
        new_doc.documentElement.setAttribute('view_id', str(view_id))
        new_doc.documentElement.appendChild(doc_arch.documentElement)

        return res['model'], new_doc.toxml().replace('\t', '')
    
    def parse(self, root=None, view_id=False):

        result = []
    
        for node in root.childNodes:
            
            if not node.nodeType==node.ELEMENT_NODE:
                continue

            attrs = tools.node_attributes(node)
            view_id = attrs.get('view_id', view_id)
            
            attrs['view_id'] = view_id
        
            attrs['__random_id__'] = random.randrange(1, 10000)
            attrs.setdefault('name', node.localName)
            
            # xpath relative to <view>
            attrs['__xpath__'] = _get_xpath(node)
            
            children = []
            
            if node.childNodes:
                children = self.parse(node, view_id)
            
            result += [_NODES.get(node.localName, Node)(attrs, children)]
            
        return result
    
    @expose('json')
    def data(self, view_id, **kw):
        view_id = int(view_id)
        
        model, view = self.view_get(view_id)
        
        doc = dom.minidom.parseString(view.encode('utf-8'))
        result = self.parse(root=doc, view_id=view_id)
        
        records = [rec.get_record() for rec in result]
        
        return dict(records=records)
    
    @expose(template="tinyerp.subcontrollers.templates.viewed_edit")
    def edit(self, view_id, xpath_expr):
        
        view_id = int(view_id)
        
        proxy = rpc.RPCProxy('ir.ui.view')
        res = proxy.read(view_id, ['model', 'arch'])
        
        doc = dom.minidom.parseString(res['arch'].encode('utf-8'))        
        field = xpath.Evaluate(xpath_expr, doc)[0]
        
        attrs = tools.node_attributes(field)
        
        editors = []
        
        properties = _PROPERTIES.get(field.localName, [])
        properties = properties[:]
        properties += list(set(attrs.keys()) - set(properties))
        
        for prop in properties:
            ed = get_property_widget(prop, attrs.get(prop))
            ed.label = prop
            
            editors += [ed]
            
        return dict(view_id=view_id, xpath_expr=xpath_expr, editors=editors)
    
    @expose(template="tinyerp.subcontrollers.templates.viewed_add")
    def add(self, view_id, xpath_expr):
        view_id = int(view_id)
        
        proxy = rpc.RPCProxy('ir.ui.view')
        res = proxy.read(view_id, ['model', 'arch'])
        
        proxy = rpc.RPCProxy(res['model'])
        fields = proxy.fields_get().keys()
        
        nodes = _PROPERTIES.keys()
        nodes.sort()

        return dict(view_id=view_id, xpath_expr=xpath_expr, nodes=nodes, fields=fields)
    
    @expose('json')
    def save(self, _terp_what, view_id, xpath_expr, **kw):
        
        view_id = int(view_id)
        
        proxy = rpc.RPCProxy('ir.ui.view')
        res = proxy.read(view_id, ['model', 'arch'])
        
        doc = dom.minidom.parseString(res['arch'].encode('utf-8'))        
        field = xpath.Evaluate(xpath_expr, doc)[0]
        
        error = None
        
        if _terp_what == "properties":
            
            attrs = tools.node_attributes(field)        
            for attr in attrs:
                field.removeAttribute(attr)
            
            attrs.update(kw)
        
            for attr, val in attrs.items():
                if val:
                    field.setAttribute(attr, val)
                    
        if _terp_what == "node" and field.parentNode and field.parentNode.localName:
            
            node = doc.createElement(kw['node'])
            
            if node.localName == "field":
                node.setAttribute('name', kw.get('name', node.localName))

            pos = kw['position']
            
            pnode = field.parentNode
            
            if pos == "after":
                pnode.insertBefore(node, field.nextSibling)
                
            elif pos == "before":
                pnode.insertBefore(node, field)
                
            elif pos == "inside":
                field.appendChild(node)

        if _terp_what == "remove":
            
            pnode = field.parentNode
            pnode.removeChild(field)
        
        data = dict(arch=doc.toxml(encoding="utf-8"))
        try:
            res = proxy.write(view_id, data)
        except:
            error = _("Unable to update the view.")
        
        return dict(error=error)
    
class Node(object):
    
    def __init__(self, attrs, children=None):
        self.attrs = attrs or {}
        self.children = children
        
        self.view_id = self.attrs['view_id']
        self.id = self.attrs['__random_id__']
        self.xpath = self.attrs['__xpath__']
        
        self.name = self.get_name()
        
    def get_name(self):
        return "<%s>" % self.attrs['name']
    
    def get_record(self):
        record = {
            'id' : self.id,
            'data' : {'name' : self.name,
                      'view_id' : self.view_id,
                      'xpath' : self.xpath,
                      'editable' : 1}}
        
        if self.children:
            record['children'] = [c.id for c in self.children]
            record['child_records'] = [c.get_record() for c in self.children]

        return record

class ViewNode(Node):
    
    def get_name(self):
        return '<view view_id="%s">' % self.view_id
    
    def get_record(self):
        res = super(ViewNode, self).get_record()
        res['data']['editable'] = 0
        
        return res
    
class FieldNode(Node):
    
    def get_name(self):
        return '[%s]' % self.attrs['name']
    
class ButtonNode(Node):
    
    def get_name(self):
        return '<button>'

_NODES = {
    'view' : ViewNode,
    'field': FieldNode,
    'button' : ButtonNode
}

_PROPERTIES = {
    'field' : ['name', 'string', 'readonly', 'select', 'completion', 'domain', 'context', 'nolabel', 'colspan', 'widget', 'eval', 'ref'],
    'form' : ['string', 'col', 'link'],
    'notebook' : ['colspan', 'position'],
    'page' : ['string'],
    'group' : ['string', 'col', 'colspan'],
    'image' : ['filename', 'width', 'height'],
    'separator' : ['string', 'colspan'],
    'label': ['string', 'align', 'colspan'],
    'button': ['name', 'string', 'type', 'states', 'readonly'],
    'newline' : [],
    'hpaned': ['position'],
    'vpaned': ['position'],
    'child1' : [],
    'child2' : [],
    'action' : ['string'],
    'tree' : ['string', 'colors', 'editable', 'link'],
    'graph' : ['string', 'type'],
    'calendar' : ['string', 'date_start', 'date_stop', 'date_delay', 'day_length', 'color'],
    'view' : [],
}

def get_property_widget(name, value=None):
    return tg_widgets.TextField(name=name, default=value)
