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

import os
import time
import types
import base64
import xml.dom.minidom

import csv
import StringIO

from openerp.tools import expose
from openerp.tools import redirect

import cherrypy

from openerp import rpc
from openerp import tools
from openerp import common

from openerp.tinyres import TinyResource
from openerp.utils import TinyDict

import openerp.widgets as tw

def datas_read(ids, model, fields):
    return rpc.RPCProxy(model).export_data(ids, fields)

def export_csv(fields, result, write_title=False):
    try:
        fp = StringIO.StringIO()
        writer = csv.writer(fp)
        if write_title:
            writer.writerow(fields)
        for data in result:
            row = []
            for d in data:
                if isinstance(d, basestring):
                    d = d.replace('\n',' ').replace('\t',' ')
                    try:
                        d = d.encode('utf-8')
                    except:
                        pass
                row.append(d)

            writer.writerow(row)

        fp.seek(0)
        data = fp.read()
        fp.close()

        return data
    except IOError, (errno, strerror):
        raise common.message(_("Operation failed!\nI/O error")+"(%s)" % (errno,))

def _fields_get_all(model, views):

    def parse(root, fields):

        for node in root.childNodes:

            if node.nodeName in ('form', 'notebook', 'page', 'group', 'tree', 'hpaned', 'vpaned'):
                parse(node, fields)

            elif node.nodeName=='field':
                attrs = tools.node_attributes(node)
                name = attrs['name']

                fields[name].update(attrs)

        return fields

    proxy = rpc.RPCProxy(model)

    v1 = proxy.fields_view_get(views.get('tree', False), 'tree', rpc.session.context)
    v2 = proxy.fields_view_get(views.get('form', False), 'form', rpc.session.context)

    dom = xml.dom.minidom.parseString(v1['arch'].encode('utf-8'))
    root = dom.childNodes[0]

    f1 = parse(root, v1['fields'])

    dom = xml.dom.minidom.parseString(v2['arch'].encode('utf-8'))
    root = dom.childNodes[0]

    f2 = parse(root, v2['fields'])

    fields = {}
    fields.update(f1)
    fields.update(f2)

    return fields

class ImpEx(TinyResource):

    @expose(template="templates/exp.mako")
    def exp(self, **kw):
        params, data = TinyDict.split(kw)

        views = {}
        if params.view_mode and params.view_ids:
            for i, view in enumerate(params.view_mode):
                views[view] = params.view_ids[i]


        proxy = rpc.RPCProxy('ir.exports')
        new_list = []

        headers = [{'string' : 'Name', 'name' : 'name', 'type' : 'char'}]
        tree = tw.treegrid.TreeGrid('export_fields',
                                    model=params.model,
                                    headers=headers,
                                    url='/impex/get_fields',
                                    field_parent='relation',
                                    views=views)

        tree.show_headers = False

        view = proxy.fields_view_get(False, 'tree', rpc.session.context)
        new_list = tw.listgrid.List(name='_terp_list', model='ir.exports', view=view, ids=None,
                                       domain=[('resource', '=', params.model)],
                                       context=rpc.session.context, selectable=1, editable=False, pageable=False)


        return dict(new_list=new_list, model=params.model, ids=params.ids,
                    search_domain=params.search_domain, source=params.source,
                    tree=tree)

    @expose()
    def save_exp(self, **kw):
        params, data = TinyDict.split(kw)

        selected_list = data.get('fields')
        name = data.get('savelist_name')

        proxy = rpc.RPCProxy('ir.exports')

        if selected_list and name:
            if isinstance(selected_list, basestring):
                selected_list = [selected_list]
            proxy.create({'name' : name, 'resource' : params.model, 'export_fields' : [(0, 0, {'name' : f}) for f in selected_list]})

        raise redirect('/impex/exp', **kw)

    @expose()
    def delete_listname(self, **kw):

        params, data = TinyDict.split(kw)
        proxy = rpc.RPCProxy('ir.exports')

        proxy.unlink(params.id)

        raise redirect('/impex/exp', **kw)

    @expose('json')
    def get_fields(self, model, prefix='', name='', field_parent=None, **kw):

        is_importing = kw.get('is_importing', False)

        ids = kw.get('ids', '').split(',')
        ids = [i for i in ids if i]

        views = {}
        try:
            views = eval(kw['views'])
        except:
            pass

        fields = _fields_get_all(model, views)

        fields_order = fields.keys()
        fields_order.sort(lambda x,y: -cmp(fields[x].get('string', ''), fields[y].get('string', '')))

        records = []

        for i, field in enumerate(fields_order):

            value = fields[field]
            record = {}

            id = prefix + (prefix and '/' or '') + field
            nm = name + (name and '/' or '') + value['string']

            if is_importing and (value['type'] not in ('reference',)) and (not value.get('readonly', False) \
                        or not dict(value.get('states', {}).get('draft', [('readonly', True)])).get('readonly', True)):

                record['id'] = id
                record['items'] = {'name' : nm}
                record['action'] = 'javascript: void(0)'
                record['target'] = None
                record['icon'] = None
                record['children'] = []
                record['required'] = value.get('required', False)

                records += [record]

            elif not is_importing:
                if ids:
                    record['id'] = ids[i]
                else:
                    record['id'] = id

                record['items'] = {'name' : nm}
                record['action'] = 'javascript: void(0)'
                record['target'] = None
                record['icon'] = None
                record['children'] = []

                records += [record]

            if len(nm.split('/')) < 3 and value.get('relation', False):

                if is_importing and not ((value['type'] not in ('reference',)) and (not value.get('readonly', False)) and value['type']=='one2many'):
                    continue

                ref = value.pop('relation')

                proxy = rpc.RPCProxy(ref)
                cfields = proxy.fields_get(False, rpc.session.context)
                cfields_order = cfields.keys()
                cfields_order.sort(lambda x,y: -cmp(cfields[x].get('string', ''), cfields[y].get('string', '')))

                children = []
                for j, fld in enumerate(cfields_order):
                    cid = id + '/' + fld
                    cid = cid.replace(' ', '_')

                    children += [cid]

                record['children'] = children or None
                record['params'] = {'model': ref, 'prefix': id, 'name': nm}

        records.reverse()
        return dict(records=records)


    @expose()
    def get_namelist(self, **kw):

        params, data = TinyDict.split(kw)

        res = []
        ids = []
        id = params.id

        res = self.get_data(params.model)

        ir_export = rpc.RPCProxy('ir.exports')
        ir_export_line = rpc.RPCProxy('ir.exports.line')

        field = ir_export.read(id)
        fields = ir_export_line.read(field['export_fields'])

        name_list = []
        ids = [f['name'] for f in fields]

        for name in ids:
            name_list += [(name, res.get(name))]

        return dict(name_list=name_list)

    def get_data(self, model):

        name = ''
        prefix = ''
        ids = []

        fields_data = {}
        proxy = rpc.RPCProxy(model)
        fields = proxy.fields_get(False, rpc.session.context)

        # XXX: in GTK client, top fields comes from Screen
        if not ids:
            f1 = proxy.fields_view_get(False, 'tree', rpc.session.context)['fields']
            f2 = proxy.fields_view_get(False, 'form', rpc.session.context)['fields']

            fields = {}
            fields.update(f1)
            fields.update(f2)

        def rec(fields):

            _fields = {}

            def model_populate(fields, prefix_node='', prefix=None, prefix_value='', level=2):
                fields_order = fields.keys()
                fields_order.sort(lambda x,y: -cmp(fields[x].get('string', ''), fields[y].get('string', '')))

                for field in fields_order:
                    fields_data[prefix_node+field] = fields[field]
                    if prefix_node:
                        fields_data[prefix_node + field]['string'] = '%s%s' % (prefix_value, fields_data[prefix_node + field]['string'])
                    st_name = fields[field]['string'] or field
                    _fields[prefix_node+field] = st_name
                    if fields[field].get('relation', False) and level>0:
                        fields2 = rpc.session.execute('object', 'execute', fields[field]['relation'], 'fields_get', False, rpc.session.context)
                        model_populate(fields2, prefix_node+field+'/', None, st_name+'/', level-1)

            model_populate(fields)

            return _fields

        return rec(fields)

    @expose(content_type="application/octet-stream")
    def export_data(self, fname, fields, export_as="csv", add_names=False, **kw):

        params, data = TinyDict.split(kw)
        proxy = rpc.RPCProxy(params.model)

        if isinstance(fields, basestring):
            fields = [fields]

        ctx = {}
        ctx.update(rpc.session.context.copy())

        domain = params.seach_domain or []

        ids = params.ids or proxy.search(domain, 0, 0, 0, ctx)
        result = datas_read(ids, params.model, fields)

        if export_as == 'excel':
            #add_names = True
            pass
        return export_csv(params.fields2, result, add_names)

    @expose(template="templates/imp.mako")
    def imp(self, **kw):
        params, data = TinyDict.split(kw)

        views = {}
        if params.view_mode and params.view_ids:
            for i, view in enumerate(params.view_mode):
                views[view] = params.view_ids[i]

        headers = [{'string' : 'Name', 'name' : 'name', 'type' : 'char'}]
        tree = tw.treegrid.TreeGrid('import_fields',
                                    model=params.model,
                                    headers=headers,
                                    url='/impex/get_fields',
                                    field_parent='relation',
                                    views=views,
                                    is_importing=1)

        tree.show_headers = False

        return dict(model=params.model, source=params.source, tree=tree, fields=kw.get('fields', {}))

    @expose()
    def detect_data(self, csvfile, csvsep, csvdel, csvcode, csvskip, **kw):
        params, data = TinyDict.split(kw)

        _fields = {}
        _fields_invert = {}

        def model_populate(fields, prefix_node='', prefix=None, prefix_value='', level=2):
            def str_comp(x,y):
                if x<y: return 1
                elif x>y: return -1
                else: return 0

            fields_order = fields.keys()
            fields_order.sort(lambda x,y: str_comp(fields[x].get('string', ''), fields[y].get('string', '')))
            for field in fields_order:
                if (fields[field]['type'] not in ('reference',)) and (not fields[field].get('readonly', False)):
                    st_name = prefix_value+fields[field]['string'] or field
                    _fields[prefix_node+field] = st_name
                    _fields_invert[st_name] = prefix_node+field
                    if fields[field]['type']=='one2many' and level>0:
                        fields2 = rpc.session.execute('object', 'execute', fields[field]['relation'], 'fields_get', False, rpc.session.context)
                        model_populate(fields2, prefix_node+field+'/', None, st_name+'/', level-1)

        proxy = rpc.RPCProxy(params.model)
        fields = proxy.fields_get(False, rpc.session.context)
        model_populate(fields)

        try:
            data = csv.reader(csvfile.file, quotechar=str(csvdel), delimiter=str(csvsep))
        except:
            raise common.warning(_('Error opening .CSV file'), _('Input Error.'))

        fields = []
        word=''
        try:
            for line in data:
                for word in line:
                    word = ustr(word.decode(csvcode))
                    fields += [(_fields_invert[word], word)]
                break
        except:
            raise common.warning(_('Error processing your first line of the file.\nField %s is unknown!') % (word,), _('Import Error.'))

        kw['fields'] = fields
        return self.imp(**kw)

    @expose()
    def import_data(self, csvfile, csvsep, csvdel, csvcode, csvskip, fields=[], **kw):

        params, data = TinyDict.split(kw)

        content = csvfile.file.read()
        input=StringIO.StringIO(content)
        data = list(csv.reader(input, quotechar=str(csvdel), delimiter=str(csvsep)))[int(csvskip):]
        datas = []
        #if csv_data['combo']:

        if not isinstance(fields, list):
            fields = [fields]

        for line in data:
            datas.append(map(lambda x:x.decode(csvcode).encode('utf-8'), line))
        try:
            res = rpc.session.execute('object', 'execute', params.model, 'import_data', fields, datas)
        except Exception, e:
            raise common.warning(ustr(e), _('XML-RPC error!'))
        if res[0]>=0:
            raise common.message(_('Imported %d objects!') % (res[0],))
        else:
            d = ''
            for key,val in res[1].items():
                d+= ('\t%s: %s\n' % (ustr(key),ustr(val)))
            error = _('Unable to import this record:\n%s\nError Message:\n%s\n\n%s') % (d,res[2],res[3])
            raise common.message(unicode(error))

        return self.imp(**kw)


# vim: ts=4 sts=4 sw=4 si et

