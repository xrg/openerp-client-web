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

import xml
import random

from xml import xpath

# xpath module replaces __builtins__['_'], which breaks TG i18n
import turbogears
turbogears.i18n.tg_gettext.install()

from turbogears import expose
from turbogears import controllers
from turbogears import validators as tg_validators
from turbogears import widgets as tg_widgets

import cherrypy

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp.tinyres import TinyResource

import tinyerp.widgets as tw

from form import Form

class NewField(Form):
    
    path = '/viewed/new_field'    # mapping from root
    
    def create_form(self, params, tg_errors=None):
        form = super(NewField, self).create_form(params, tg_errors)
        
        field = form.screen.widget.get_widgets_by_name('model_id')[0]
        field.set_value(params.model_id or False)
        
        # generate model_id field
        form.hidden_fields = [tg_widgets.HiddenField(name='model_id', default=params.model_id)]
        vals = getattr(cherrypy.request, 'terp_validators', {})
        vals['model_id'] = tw.validators.Int()
                
        return form

    @expose(template="tinyerp.subcontrollers.templates.viewed_new")
    def create(self, params, tg_errors=None):
        
        params.model_id = False
        for_model = params.context.get('model')
        
        if for_model:
            params.model_id = rpc.RPCProxy('ir.model').search([('model', '=', for_model)])[0]
        
        if not params.id:
            params.context = {'manual' : True}

        form = self.create_form(params, tg_errors)
        
        return dict(form=form, params=params, show_header_footer=False)
   
class ViewEd(controllers.Controller, TinyResource):
    
    new_field = NewField()
    
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
        
        headers = [{'string' : 'Name', 'name' : 'string', 'type' : 'char'}]
        tree = tw.treegrid.TreeGrid('view_tree', model=model, headers=headers, url='/viewed/data?view_id='+str(view_id))
        tree.showheaders = False
        tree.onselection = 'onSelect'
        tree.expandall = True

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

            doc_src = xml.dom.minidom.parseString(src.encode('utf-8'))
            doc_dest = xml.dom.minidom.parseString(inherit.encode('utf-8'))
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
        doc_arch = xml.dom.minidom.parseString(doc_arch.encode('utf-8'))
        
        new_doc = xml.dom.getDOMImplementation().createDocument(None, 'view', None)
        new_doc.documentElement.setAttribute('view_id', str(view_id))
        new_doc.documentElement.appendChild(doc_arch.documentElement)

        return res['model'], new_doc.toxml().replace('\t', '')
    
    def get_node_instance(self, node=None, view_id=False):
        
        attrs = tools.node_attributes(node)
        view_id = attrs.get('view_id', view_id)
        
        attrs['view_id'] = view_id
        attrs['__local_name__'] = node.localName
    
        attrs['__random_id__'] = random.randrange(1, 10000)
        attrs.setdefault('name', node.localName)
        
        return _NODES.get(node.localName, Node)(attrs)

    def parse(self, root=None, view_id=False):

        result = []
    
        for node in root.childNodes:
            
            if not node.nodeType==node.ELEMENT_NODE:
                continue

            attrs = tools.node_attributes(node)
            view_id = attrs.get('view_id', view_id)
            
            attrs['view_id'] = view_id
            attrs['__local_name__'] = node.localName
        
            attrs['__random_id__'] = random.randrange(1, 10000)
            attrs.setdefault('name', node.localName)
            
            children = []
            
            if node.childNodes:
                children = self.parse(node, view_id)
                
            node_instance = self.get_node_instance(node, view_id)
            node_instance.children = children
            
            result += [node_instance]

        return result
    
    @expose('json')
    def data(self, view_id, **kw):
        view_id = int(view_id)
        
        model, view = self.view_get(view_id)
        
        doc = xml.dom.minidom.parseString(view.encode('utf-8'))
        result = self.parse(root=doc, view_id=view_id)
        
        records = [rec.get_record() for rec in result]
        
        return dict(records=records)
    
    @expose(template="tinyerp.subcontrollers.templates.viewed_edit")
    def edit(self, view_id, xpath_expr):
        
        view_id = int(view_id)
        
        proxy = rpc.RPCProxy('ir.ui.view')
        res = proxy.read(view_id, ['model', 'arch'])
        
        doc = xml.dom.minidom.parseString(res['arch'].encode('utf-8'))        
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
        
        doc = xml.dom.minidom.parseString(res['arch'].encode('utf-8'))        
        field_node = xpath.Evaluate(xpath_expr, doc)[0]
        
        model = res['model']
        
        # get the correct model
        
        parents = []
        parent_node = field_node.parentNode
        
        while parent_node:
            if parent_node.localName == 'field':
                parents += [parent_node.getAttribute('name')]
            parent_node = parent_node.parentNode
        
        parents.reverse()
        
        for parent in parents:
            proxy = rpc.RPCProxy(model)
            field = proxy.fields_get([parent])[parent]
            
            model = field['relation']
        
        # get the fields
        proxy = rpc.RPCProxy(model)
        fields = proxy.fields_get().keys()

        nodes = _PROPERTIES.keys()
        nodes.sort()

        return dict(view_id=view_id, xpath_expr=xpath_expr, nodes=nodes, fields=fields)
    
    @expose('json')
    def create_view(self, view_id=False, xpath_expr=None, model=None, **kw):
        
        view_id = int(view_id)
        proxy = rpc.RPCProxy('ir.ui.view')
        
        error = None
        record = None
        
        if view_id:
            
            res = proxy.read(view_id, ['model', 'arch'])
            doc = xml.dom.minidom.parseString(res['arch'].encode('utf-8'))
            node = xpath.Evaluate(xpath_expr, doc)[0]
            new_node = doc.createElement('view')
            
            if node.localName == 'field':

                data = {'name' : res['model'] + '.' + str(random.randint(0, 100000)) + '.inherit',
                        'model' : res['model'],
                        'priority' : 16,
                        'type' : 'form',
                        'inherit_id' : view_id}
            
                arch = """<?xml version="1.0"?>
                <field name="%s" position="after">
                </field>""" % (node.getAttribute('name'))
                
                data['arch'] = arch
            
                try:
                    view_id = rpc.RPCProxy('ir.ui.view').create(data)
                    
                    node.setAttribute('position', 'after')
                    
                    record = self.get_node_instance(new_node, view_id).get_record()
                    record['children'] = [self.get_node_instance(node, view_id).get_record()]
                    
                except:
                    error = _("Unable to create inherited view.")
            else:
                error = _("Unable to create inherited view.")
                
        else:
            error = _("Not implemented yet!")
            
        return dict(record=record, error=error)
    
    @expose('json')
    def remove_view(self, view_id, **kw):
        
        view_id = int(view_id)
        
        if view_id:
            proxy = rpc.RPCProxy('ir.ui.view')
            proxy.unlink(view_id)
            
        return dict()
    
    @expose('json')
    def save(self, _terp_what, view_id, xpath_expr, **kw):
        
        view_id = int(view_id)
        
        proxy = rpc.RPCProxy('ir.ui.view')
        res = proxy.read(view_id, ['model', 'arch'])
        
        doc = xml.dom.minidom.parseString(res['arch'].encode('utf-8'))
        node = xpath.Evaluate(xpath_expr, doc)[0]
        
        new_node = None
        
        error = None
        record = None
            
        if _terp_what == "properties":
            
            attrs = tools.node_attributes(node)        
            for attr in attrs:
                node.removeAttribute(attr)
        
            for attr, val in kw.items():
                if val:
                    node.setAttribute(attr, val)
        
        if _terp_what == "node" and node.parentNode:
            
            new_node = doc.createElement(kw['node'])
            
            if new_node.localName == "field":
                new_node.setAttribute('name', kw.get('name', new_node.localName))
            
            pnode = node.parentNode
            pos = kw['position']
            
            try:
                if pos == "after":
                    pnode.insertBefore(new_node, node.nextSibling)
                    
                elif pos == "before":
                    pnode.insertBefore(new_node, node)
                    
                elif pos == "inside" and new_node.localName != "field":
                    node.appendChild(new_node)
                
                else:
                    error = _("Invalid position.")
            except Exception, e:
                error = ustr(e)

        if _terp_what == "remove":
            pnode = node.parentNode
            pnode.removeChild(node)
        else:
            node_instance = self.get_node_instance(new_node or node, view_id)
            node_instance.children = self.parse(new_node or node, view_id)
            record = node_instance.get_record()
        
        data = dict(arch=doc.toxml(encoding="utf-8"))
        try:
            res = proxy.write(view_id, data)
        except:
            error = _("Unable to update the view.")
        
        return dict(record=record, error=error)
    
class Node(object):
    
    def __init__(self, attrs, children=None):
        self.attrs = attrs or {}
        self.children = children
        
        self.view_id = self.attrs['view_id']
        self.id = self.attrs['__random_id__']
        
        self.name = self.attrs['name']
        self.localName = self.attrs['__local_name__']
        self.string = self.get_text()
        
    def get_text(self):
        return "<%s>" % self.name
    
    def get_record(self):
        record = {
            'id' : self.id,
            'items' : {'string' : self.string,
                       'name' : self.name,
                       'localName' : self.localName,
                       'view_id' : self.view_id}}
        
        if self.children:
            record['children'] = [c.get_record() for c in self.children]

        return record

class ViewNode(Node):
    
    def get_text(self):
        return '<view view_id="%s">' % self.view_id
    
class FieldNode(Node):
    
    def get_text(self):
        return '[%s]' % self.name
    
class ButtonNode(Node):
    
    def get_text(self):
        return '<button>'
    
class ActionNode(Node):
    
    def get_text(self):
        return '<action>'

_NODES = {
    'view' : ViewNode,
    'field': FieldNode,
    'button' : ButtonNode,
    'action' : ActionNode
}

_PROPERTIES = {
    'field' : ['name', 'string', 'readonly', 'select', 'completion', 'domain', 'context', 'nolabel', 'colspan', 'widget', 'eval', 'ref', 'groups'],
    'form' : ['string', 'col', 'link'],
    'notebook' : ['colspan', 'position', 'groups'],
    'page' : ['string', 'groups'],
    'group' : ['string', 'col', 'colspan', 'groups'],
    'image' : ['filename', 'width', 'height', 'groups'],
    'separator' : ['string', 'colspan', 'groups'],
    'label': ['string', 'align', 'colspan', 'groups'],
    'button': ['name', 'string', 'type', 'states', 'readonly', 'groups'],
    'newline' : [],
    'hpaned': ['position', 'groups'],
    'vpaned': ['position', 'groups'],
    'child1' : ['groups'],
    'child2' : ['groups'],
    'action' : ['string', 'groups'],
    'tree' : ['string', 'colors', 'editable', 'link'],
    'graph' : ['string', 'type'],
    'calendar' : ['string', 'date_start', 'date_stop', 'date_delay', 'day_length', 'color'],
    'view' : [],
    'properties' : ['groups'],
}

class SelectProperty(tg_widgets.SingleSelectField):
    
    def __init__(self, name, default=None):
        
        options = [('', 'Not Searchable'),
                   ('1', 'Always Searchable'),
                   ('2', 'Advanced Search')]
        
        super(SelectProperty, self).__init__(name=name, options=options, default=default)
        
class WidgetProperty(tg_widgets.SingleSelectField):
    
    def __init__(self, name, default=None):
        
        options = [''] + tw.form.widgets_type.keys()
                
        super(WidgetProperty, self).__init__(name=name, options=options, default=default)        
        
class BooleanProperty(tg_widgets.CheckBox):
    
    def __init__(self, name, default=None):
        super(BooleanProperty, self).__init__(name=name, attrs=dict(value=1, checked=default))
        self.field_class = "checkbox"
        
class GroupsProperty(tg_widgets.MultipleSelectField):
    
    def __init__(self, name, default=None):
                
        default = default or ''
        default = default.split(',')
        
        group_ids = rpc.RPCProxy('res.groups').search([])
        groups = rpc.RPCProxy('ir.model.data').search([('res_id', 'in', group_ids ), ('model', '=', 'res.groups')])
        groups = rpc.RPCProxy('ir.model.data').read(groups, ['module', 'name'])
        
        options = ['%s.%s' % (g['module'], g['name']) for g in groups]
        
        super(GroupsProperty, self).__init__(name=name, options=options, default=default)

_PROPERTY_WIDGETS = {
    'select' : SelectProperty,                                                                  
    'readonly' : BooleanProperty,
    'nolabel' : BooleanProperty,
    'completion' : BooleanProperty,
    'widget' : WidgetProperty,
    'groups' : GroupsProperty,                                                 
}

def get_property_widget(name, value=None):
    wid = _PROPERTY_WIDGETS.get(name, tg_widgets.TextField)
    return wid(name=name, default=value)
