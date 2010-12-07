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
# -   All names, links and logos of Tiny, OpenERP and Axelor must be
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
import random
import xml

import cherrypy
from openerp import utils, widgets, validators
from openerp.controllers import SecuredController
from openerp.utils import rpc, common, icons, cache, TinyDict

from form import Form
from openobject.tools import url, expose


class NewField(Form):

    _cp_path = "/openerp/viewed/new_field"

    def create_form(self, params, tg_errors=None):

        # generate model_id field
        params.hidden_fields = [widgets.form.Hidden(name='model_id', default=params.model_id)]
        form = super(NewField, self).create_form(params, tg_errors)

        field = form.screen.widget.get_widgets_by_name('model_id')[0]
        field.set_value(params.model_id or False)
        field.readonly = True

        vals = getattr(cherrypy.request, 'terp_validators', {})
        vals['model_id'] = validators.Int()

        return form

    @expose(template="/openerp/controllers/templates/viewed_new.mako")
    def create(self, params, tg_errors=None):

        params.editable = True
        params.model_id = False
        for_model = params.context.get('for_model')

        if for_model:
            params.model_id = rpc.RPCProxy('ir.model').search([('model', '=', for_model)])[0]

        params.context = params.context or {}
        params.context.update({'manual' : True})

        form = self.create_form(params, tg_errors)

        return dict(form=form, params=params)

    @expose()
    def edit(self, for_model, id=False):
        ctx = {'for_model' : for_model}
        return super(NewField, self).edit(model='ir.model.fields', id=id, context=ctx)

class NewModel(Form):

    _cp_path = "/openerp/viewed/new_model"

    @expose(template="/openerp/controllers/templates/viewed_new_model.mako")
    def create(self, params, tg_errors=None):

        params.editable = True
        params.context = params.context or {}
        params.context.update({'manual' : True})

        form = self.create_form(params, tg_errors)

        return dict(form=form, params=params)

    @expose()
    def edit(self, model=None, id=False, **kw):

        params = TinyDict()
        params.model = model
        params.id = id

        id = params.id
        if not id:
            res = rpc.RPCProxy('ir.model').search([('model', '=', params.model)])

            id = (res or False) and res[0]

        return super(NewModel, self).edit(model='ir.model', id=id)

class Preview(Form):

    _cp_path = "/openerp/viewed/preview"

    @expose(template="/openerp/controllers/templates/viewed_preview.mako")
    def create(self, params, tg_errors=None):
        form = self.create_form(params, tg_errors)
        return dict(form=form)

    @expose()
    def show(self, model, view_id, view_type):
        view_id = int(view_id)
        params, data = TinyDict.split({'_terp_model': model,
                                       '_terp_ids' : [],
                                       '_terp_view_ids' : [view_id],
                                       '_terp_view_mode' : [view_type]})
        return self.create(params)

def xml_locate(expr, ref):
    """Simple xpath locator.

    >>> xml_locate("/form[1]/field[2]", doc)
    >>> xml_locate("/form[1]", doc)

    @param expr: simple xpath with tag name and index
    @param ref: reference node

    @return: list of nodes
    """

    if '/' not in expr:
        name, index = expr.split('[')
        index = int(index.replace(']', ''))

        nodes = [n for n in ref.childNodes if n.localName == name]
        try:
            return nodes[index-1]
        except Exception, e:
            return []

    parts = expr.split('/')
    for part in parts:
        if part in ('', '.'):
            continue
        ref = xml_locate(part, ref)

    return [ref]

def xml_getElementsByTagAndName(tag, name, ref):
    """Convenient function to locate tags with Tag name and Name attribute.

    @param tag: tag name
    @param name: name attribute value of the tag
    @param ref: reference node

    @return: list of nodes
    """
    return [node for node in ref.getElementsByTagName(tag) if node.getAttribute('name') == name]

def _get_model(node, parent_model):

    parents = []
    pnode = node.parentNode

    while pnode:

        if pnode.localName == 'field':
            ch = utils.xml_locate('./form[1]', pnode) \
               + utils.xml_locate('./tree[1]', pnode) \
               + utils.xml_locate('./graph[1]', pnode) \
               + utils.xml_locate('./calendar[1]', pnode)

            if ch:
                parents.append(pnode.getAttribute('name'))

        pnode = pnode.parentNode

    parents.reverse()

    for parent in parents:
        field = rpc.RPCProxy(parent_model).fields_get([parent], rpc.session.context)

        if field:
            if field[parent].get('relation'):
                parent_model = field[parent]['relation']

    return parent_model

def _get_field_attrs(node, parent_model):

    if node.localName != 'field':
        return {}

    model = _get_model(node, parent_model)

    name = node.getAttribute('name')
    field = rpc.RPCProxy(model).fields_get([name])

    if field:
         field = field[name]

    return field

class ViewEd(SecuredController):

    _cp_path = "/openerp/viewed"

    @expose(template="/openerp/controllers/templates/viewed.mako")
    def default(self, view_id):

        try:
            view_id = eval(view_id)
        except:
            pass

        if isinstance(view_id, basestring) or not view_id:
            raise common.message(_("Invalid view id."))

        res = rpc.RPCProxy('ir.ui.view').read([view_id], ['model', 'type'])[0]

        model = res['model']
        view_type = res['type']

        headers = [{'string' : 'Name', 'name' : 'string', 'type' : 'char'},
                   {'string' : '', 'name': 'add', 'type' : 'image', 'width': 2},
                   {'string' : '', 'name': 'delete', 'type' : 'image', 'width': 2},
                   {'string' : '', 'name': 'edit', 'type' : 'image', 'width': 2},
                   {'string' : '', 'name': 'up', 'type' : 'image', 'width': 2},
                   {'string' : '', 'name': 'down', 'type' : 'image', 'width': 2}]

        tree = widgets.treegrid.TreeGrid('view_tree', model=model, headers=headers, url=url('/openerp/viewed/data?view_id='+str(view_id)))
        tree.showheaders = False
        tree.onselection = 'onSelect'
        tree.onbuttonclick = 'onButtonClick'
        tree.expandall = True

        return dict(view_id=view_id, view_type=view_type, model=model, tree=tree)

    def view_get(self, view_id=None):

        def _inherit_apply(src, inherit, inherited_id):
            def _find(node, node2):
                # Check if xpath query or normal inherit (with field matching)
                if node2.nodeType==node2.ELEMENT_NODE and node2.localName=='xpath':
                    res = utils.get_xpath(node2.getAttribute('expr'), node)
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

                if node2.localName == 'data':
                    continue
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
                    raise AttributeError, "Couldn't find tag '%s' in parent view" % tag
            return doc_src.toxml().replace('\t', '')

        views = rpc.RPCProxy('ir.ui.view')
        res = views.read([view_id])[0]

        def _inherit_apply_rec(result, inherit_id):
            # get all views which inherit from (ie modify) this view
            inherit_ids = views.search([('inherit_id', '=', inherit_id)], 0, 0, 'priority')
            inherit_res = views.read(inherit_ids, ['arch', 'id'])

            for res2 in inherit_res:
                result = _inherit_apply(result, res2['arch'], res2['id'])
                result = _inherit_apply_rec(result, res2['id'])

            return result

        doc_arch = _inherit_apply_rec(res['arch'], view_id)
        doc_arch = xml.dom.minidom.parseString(doc_arch.encode('utf-8'))

        new_doc = xml.dom.getDOMImplementation().createDocument(None, 'view', None)
        new_doc.documentElement.setAttribute('view_id', str(view_id))
        new_doc.documentElement.appendChild(doc_arch.documentElement)

        return {
            'model': res['model'],
            'view_id': view_id,
            'view_type': res['type'],
            'arch': new_doc.toxml().replace('\t', '')
        }

    def get_node_instance(self, node, model, view_id=False, view_type='form'):

        field_attrs = _get_field_attrs(node, parent_model=model)

        attrs = utils.node_attributes(node)

        view_id = attrs.get('view_id', view_id)
        view_type = attrs.get('view_type', view_type)

        attrs['view_id'] = view_id
        attrs['view_type'] = view_type

        attrs['__localName__'] = node.localName
        attrs['__id__'] = random.randrange(1, 10000)

        attrs.setdefault('name', node.localName)

        field_attrs.update(attrs)

        return _NODES.get(node.localName, Node)(field_attrs)

    def parse(self, root=None, model=None, view_id=False, view_type='form'):

        result = []

        for node in root.childNodes:

            if not node.nodeType==node.ELEMENT_NODE:
                continue

            attrs = utils.node_attributes(node)

            view_id = attrs.get('view_id', view_id)
            view_type = attrs.get('view_type', view_type)

            children = []

            if node.childNodes:
                children = self.parse(node, model=model, view_id=view_id, view_type=view_type)

            node_instance = self.get_node_instance(node, model=model, view_id=view_id, view_type=view_type)
            node_instance.children = children

            result.append(node_instance)

        return result

    @expose('json')
    def data(self, view_id, **kw):
        view_id = int(view_id)

        res = self.view_get(view_id)

        model = res['model']
        view_type = res['view_type']
        arch = res['arch']

        doc = xml.dom.minidom.parseString(arch.encode('utf-8'))
        result = self.parse(root=doc, model=model, view_id=view_id, view_type=view_type)

        records = [rec.get_record() for rec in result]

        return dict(records=records)

    @expose(template="/openerp/controllers/templates/viewed_edit.mako", methods=('POST',))
    def edit(self, view_id, xpath_expr):
        view_id = int(view_id)

        proxy = rpc.RPCProxy('ir.ui.view')
        res = proxy.read([view_id], ['model', 'arch'])[0]

        doc = xml.dom.minidom.parseString(res['arch'].encode('utf-8'))
        field = utils.xml_locate(xpath_expr, doc)[0]

        attrs = utils.node_attributes(field)
        editors = []

        properties = _PROPERTIES.get(field.localName, [])
        if field.localName == 'field':
            kind = 'char'
            try:
                model = _get_model(field, parent_model=res['model'])
                proxy = rpc.RPCProxy(model)
                attrs2 = proxy.fields_get([attrs['name']])[attrs['name']]

                attrs2.update(attrs)

                if attrs2.get('widget', False):
                    if attrs2['widget']=='one2many_list':
                        attrs2['widget']='one2many'
                    attrs2['type'] = attrs2['widget']

                kind = attrs2.get('type', kind)
            except:
                pass
            properties = _PROPERTIES_FIELDS.get(kind) or properties
        properties = properties[:]
        properties.extend(list(set(attrs.keys()) - set(properties)))

        for prop in properties:
            if field.localName == 'action' and prop == 'name':
                ed = ActionProperty(prop, attrs.get(prop))
            elif field.localName == 'button' and prop in _PROPERTY_WIDGETS_BUTTON:
                ed = _PROPERTY_WIDGETS_BUTTON[prop](prop, attrs.get(prop))
            else:
                ed = get_property_widget(prop, attrs.get(prop))

            ed.label = prop
            editors.append(ed)

        return dict(view_id=view_id, xpath_expr=xpath_expr, editors=editors)

    @expose(template="/openerp/controllers/templates/viewed_add.mako")
    def add(self, view_id, xpath_expr):
        view_id = int(view_id)

        res = rpc.RPCProxy('ir.ui.view').read([view_id], ['model', 'arch'])[0]

        doc = xml.dom.minidom.parseString(res['arch'].encode('utf-8'))
        model = res['model']

        field_node = utils.xml_locate(xpath_expr, doc)[0]
        model = _get_model(field_node, parent_model=model)

        # get the fields
        fields = rpc.RPCProxy(model).fields_get().keys()

        nodes = _CHILDREN.keys()
        nodes.remove('view')

        nodes.sort()
        fields.sort()

        positions = [('inside', 'Inside'), ('after', 'After'), ('before', 'Before')]
        if field_node.localName in [k for k,v in _CHILDREN.items() if not v] + ['field']:
            positions = [('after', 'After'), ('before', 'Before'), ('inside', 'Inside')]

        return dict(view_id=view_id, xpath_expr=xpath_expr, nodes=nodes, fields=fields, model=model, positions=positions)

    @expose('json', methods=('POST',))
    def create_view(self, view_id=False, xpath_expr=None, **kw):

        view_id = int(view_id)

        proxy = rpc.RPCProxy('ir.ui.view')
        res = proxy.read([view_id], ['model', 'type', 'arch'])[0]

        model = res['model']
        view_type = res['type']

        error = None
        record = None

        if view_id:

            doc = xml.dom.minidom.parseString(res['arch'].encode('utf-8'))
            node = utils.xml_locate(xpath_expr, doc)[0]
            new_node = doc.createElement('view')

            if node.localName == 'field':

                data = {'name' : res['model'] + '.' + str(random.randint(0, 100000)) + '.inherit',
                        'model' : res['model'],
                        'priority' : 16,
                        'type' : view_type,
                        'inherit_id' : view_id}

                arch = """<?xml version="1.0"?>
                <field name="%s" position="after">
                </field>""" % (node.getAttribute('name'))

                data['arch'] = arch

                try:
                    view_id = proxy.create(data)
                    record = self.get_node_instance(new_node, model, view_id, view_type).get_record()
                    node.setAttribute('position', 'after')
                    record['children'] = [self.get_node_instance(node, model, view_id, view_type).get_record()]

                except:
                    error = _("Unable to create inherited view.")
            else:
                error = _("Can't create inherited view here.")

        else:
            error = _("Not implemented yet!")

        try:
            cache.clear()
        except:
            pass

        return dict(record=record, error=error)

    @expose('json', methods=('POST',))
    def remove_view(self, view_id, **kw):

        view_id = int(view_id)

        if view_id:
            rpc.RPCProxy('ir.ui.view').unlink(view_id)

        try:
            cache.clear()
        except:
            pass

        return dict()

    @expose('json', methods=('POST',))
    def save(self, _terp_what, view_id, xpath_expr, **kw):

        view_id = int(view_id)

        proxy = rpc.RPCProxy('ir.ui.view')
        res = proxy.read([view_id], ['model', 'type', 'arch'])[0]

        model = res['model']
        view_type = res['type']

        doc = xml.dom.minidom.parseString(res['arch'].encode('utf-8'))
        node = utils.xml_locate(xpath_expr, doc)[0]

        new_node = None
        record = None

        if _terp_what == "properties":

            attrs = utils.node_attributes(node)
            for attr in attrs:
                node.removeAttribute(attr)

            for attr, val in kw.items():
                if val:
                    node.setAttribute(attr, val)

        elif _terp_what == "node" and node.parentNode:

            new_node = doc.createElement(kw['node'])

            if new_node.localName == "field":
                new_node.setAttribute('name', kw.get('name', new_node.localName))

            elif new_node.localName == "notebook":
                page = doc.createElement('page')
                page.setAttribute('string', 'Page 1')
                new_node.appendChild(page)

            pnode = node.parentNode
            position = kw['position']

            try:

                if position == 'after':
                    pnode.insertBefore(new_node, node.nextSibling)

                if position == 'before':
                    pnode.insertBefore(new_node, node)

                if position == 'inside':
                    node.appendChild(new_node)

            except Exception, e:
                return dict(error=ustr(e))

        elif _terp_what == "move":

            refNode = None
            try:
                refNode = utils.xml_locate(kw['xpath_ref'], doc)[0]
            except:
                pass

            pnode = node.parentNode
            newNode = pnode.removeChild(node)

            pnode.insertBefore(newNode, refNode)

        elif _terp_what == "remove":
            pnode = node.parentNode
            pnode.removeChild(node)

        if _terp_what != 'remove':
            node_instance = self.get_node_instance(new_node or node, model=model, view_id=view_id, view_type=view_type)
            node_instance.children = self.parse(new_node or node, model, view_id, view_type)
            record = node_instance.get_record()

        try:
            proxy.write([view_id], {'arch': doc.toxml(encoding="utf-8")})
        except Exception:
            return dict(error=_("Unable to update the view."))

        try:
            cache.clear()
        except:
            pass

        return dict(record=record)

    @expose(methods=('POST',))
    def update_dashboard(self, view_id, dst, src, ref=None):
        error = None

        view_id = int(view_id)

        views = rpc.RPCProxy('ir.ui.view')
        data = views.read([view_id])[0]

        doc = xml.dom.minidom.parseString(data['arch'].encode('utf-8'))
        pnode = utils.xml_locate(dst, doc)[0]
        src = xml_getElementsByTagAndName('*', src, doc)[0]

        if ref: ref = xml_getElementsByTagAndName('*', ref, doc)[0]
        pnode.insertBefore(src, ref)
        del data['id']

        try:
            views.write(view_id, {'arch': doc.toxml(encoding="utf-8")})
        except Exception, e:
            error = str(e)
        return dict(error=error)


class Node(object):

    def __init__(self, attrs, children=None):
        self.attrs = attrs or {}
        self.children = children

        self.view_id = self.attrs['view_id']
        self.id = self.attrs['__id__']

        self.name = self.attrs['name']
        self.localName = self.attrs['__localName__']
        self.string = self.get_text()

    def get_text(self):
        if 'string' in self.attrs:
            return '<%s string="%s">' % (self.name, self.attrs['string'])
        return "<%s>" % self.name

    def get_record(self):
        items = {'string' : self.string,
                 'name' : self.name,
                 'localName' : self.localName,
                 'view_id' : self.view_id,
                 'delete': icons.get_icon('gtk-remove')}

        if self.localName != 'view':
            items.update(
                add=icons.get_icon('gtk-add'),
                up=icons.get_icon('gtk-go-up'),
                down=icons.get_icon('gtk-go-down'))

        if self.localName not in ('view', 'newline'):
            items['edit'] = icons.get_icon('gtk-edit')

        record = { 'id' : self.id, 'items' : items}

        if self.children:
            record['children'] = [c.get_record() for c in self.children]

        return record

class ViewNode(Node):

    def get_text(self):
        return '<view view_id="%s">' % self.view_id

class FieldNode(Node):

    def get_text(self):

        if self.attrs.get('type') == 'one2many':
            return '<field name="%s">' % self.name

        return '<field name="%s">' % self.name

class ButtonNode(Node):

    def get_text(self):
        return '<button name="%s">' % self.name

class ActionNode(Node):

    def get_text(self):
        return '<action name="%s">' % self.name

_NODES = {
    'view' : ViewNode,
    'field': FieldNode,
    'button' : ButtonNode,
    'action' : ActionNode
}

_PROPERTIES = {
    'field' : ['name', 'string', 'required', 'readonly', 'select', 'domain', 'context', 'nolabel', 'completion',
               'colspan', 'widget', 'eval', 'ref', 'on_change', 'attrs', 'groups'],
    'form' : ['string', 'col', 'link'],
    'notebook' : ['colspan', 'position', 'groups'],
    'page' : ['string', 'states', 'attrs', 'groups'],
    'group' : ['string', 'col', 'colspan', 'states', 'attrs', 'groups'],
    'image' : ['filename', 'width', 'height', 'groups'],
    'separator' : ['string', 'colspan', 'groups'],
    'label': ['string', 'align', 'colspan', 'groups'],
    'button': ['name', 'string', 'icon', 'type', 'states', 'readonly', 'special', 'target', 'confirm', 'context', 'attrs', 'groups'],
    'newline' : [],
    'hpaned': ['position', 'groups'],
    'vpaned': ['position', 'groups'],
    'child1' : ['groups'],
    'child2' : ['groups'],
    'action' : ['name', 'string', 'colspan', 'groups'],
    'tree' : ['string', 'colors', 'editable', 'link', 'limit', 'min_rows'],
    'graph' : ['string', 'type'],
    'calendar' : ['string', 'date_start', 'date_stop', 'date_delay', 'day_length', 'color', 'mode'],
    'view' : [],
}

# TODO: valid attributes for each field type
_PROPERTIES_FIELDS = {
    'date': [],
    'time': [],
    'float_time': [],
    'datetime': [],
    'float': [],
    'integer': [],
    'selection': [],
    'char': [],
    'boolean': [],
    'button': [],
    'reference': [],
    'binary': [],
    #'picture': Picture,
    'text': [],
    'text_tag': [],
    'text_html': [],
    'text_wiki': [],
    'one2many': [],
    'one2many_form': [],
    'one2many_list': [],
    'many2many': [],
    'many2one': [],
    'email' : [],
    'url' : [],
    'image' : ['name', 'string', 'width', 'height', 'required', 'readonly',
               'domain', 'context', 'nolabel', 'colspan', 'widget', 'eval',
               'attrs', 'groups']
}

_CHILDREN = {
    'view': ['form', 'tree', 'graph', 'calendar', 'field'],
    'form': ['notebook', 'group', 'field', 'label', 'button', 'image', 'newline', 'separator'],
    'tree': ['field'],
    'graph': ['field'],
    'calendar': ['field'],
    'notebook': ['page'],
    'page': ['notebook', 'group', 'field', 'label', 'button', 'image', 'newline', 'separator'],
    'group': ['field', 'label', 'button', 'separator', 'newline'],
    'hpaned': ['child1', 'child2'],
    'vpaned': ['child1', 'child2'],
    'child1': ['action'],
    'child2': ['action'],
    'action': [],
    'field': ['form', 'tree', 'graph'],
    'label': [],
    'button' : [],
    'image': [],
    'newline': [],
    'separator': [],
}

class SelectProperty(widgets.SelectField):

    def __init__(self, name, default=None):

        options = [('', 'Not Searchable'),
                   ('1', 'Always Searchable'),
                   ('2', 'Advanced Search')]

        super(SelectProperty, self).__init__(name=name, options=options, default=default)

class PositionProperty(widgets.SelectField):

    def __init__(self, name, default=None):

        options = [('', ''),
                   ('after', 'After'),
                   ('before', 'Before'),
                   ('inside', 'Inside'),
                   ('replace', 'Replace')]

        super(PositionProperty, self).__init__(name=name, options=options, default=default)

class WidgetProperty(widgets.SelectField):

    def __init__(self, name, default=None):

        options = widgets.get_registered_widgets().keys()
        options.sort()
        options = [''] + options

        super(WidgetProperty, self).__init__(name=name, options=options, default=default)

class BooleanProperty(widgets.CheckBox):

    def __init__(self, name, default=None):
        super(BooleanProperty, self).__init__(name=name, default=default, attrs=dict(value=1))
        self.css_class = "checkbox"

class GroupsProperty(widgets.SelectField):

    multiple = True

    def __init__(self, name, default=None):

        default = default or ''
        default = default.split(',')

        group_ids = rpc.RPCProxy('res.groups').search([])
        groups = rpc.RPCProxy('ir.model.data').search([('res_id', 'in', group_ids ), ('model', '=', 'res.groups')])
        groups = rpc.RPCProxy('ir.model.data').read(groups, ['module', 'res_id', 'name'])

        groups_names = rpc.RPCProxy('res.groups').read(group_ids, ['name'])
        names = dict([(n['id'], n['name']) for n in groups_names])

        options = [('%s.%s' % (g['module'], g['name']), names[g['res_id']]) for g in groups]

        super(GroupsProperty, self).__init__(name=name, options=options, default=default)

class ActionProperty(widgets.form.M2O):

    def __init__(self, name, default=None):
        super(ActionProperty, self).__init__(name=name, relation='ir.actions.actions')
        self.set_value(default or False)

class IconProperty(widgets.SelectField):

    def __init__(self, name, default=None):
        options = [('', '')] + icons.icons
        super(IconProperty, self).__init__(name=name, options=options, default=default)

class ButtonTargetProperty(widgets.SelectField):

    def __init__(self, name, default=None):
        options = [('', ''), ('new', _('New Window'))]
        super(ButtonTargetProperty, self).__init__(name=name, options=options, default=default)

class ButtonTypeProperty(widgets.SelectField):

    def __init__(self, name, default=None):
        options = [('', ''), ('action', 'Action'), ('object', 'Object'), ('workflow', 'Workflow'), ('server_action', 'Server Action')]
        super(ButtonTypeProperty, self).__init__(name=name, options=options, default=default)

class ButtonSpecialProperty(widgets.SelectField):

    def __init__(self, name, default=None):
        options = [('', ''), ('save', _('Save Button')), ('cancel', _('Cancel Button')), ('open', _('Open Button'))]
        super(ButtonSpecialProperty, self).__init__(name=name, options=options, default=default)

class AlignProperty(widgets.SelectField):

    def __init__(self, name, default=None):
        options = [('', ''), ('0.0', _('Left')), ('0.5', _('Center')), ('1.0', _('Right'))]
        super(AlignProperty, self).__init__(name=name, options=options, default=default)

_PROPERTY_WIDGETS = {
    'select' : SelectProperty,
    'required' : BooleanProperty,
    'readonly' : BooleanProperty,
    'nolabel' : BooleanProperty,
    'completion' : BooleanProperty,
    'widget' : WidgetProperty,
    'groups' : GroupsProperty,
    'position': PositionProperty,
    'icon': IconProperty,
    'align': AlignProperty,
}

_PROPERTY_WIDGETS_BUTTON = {
    'special': ButtonSpecialProperty,
    'type': ButtonTypeProperty,
    'target': ButtonTargetProperty,
}

def get_property_widget(name, value=None):
    wid = _PROPERTY_WIDGETS.get(name, widgets.TextField)
    return wid(name=name, default=value)
