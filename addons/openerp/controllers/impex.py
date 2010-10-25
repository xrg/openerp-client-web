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
import StringIO
import csv
import re
import xml.dom.minidom

from openerp.controllers import SecuredController
from openerp.utils import rpc, common, TinyDict, node_attributes
from openerp.widgets import treegrid, listgrid

from openobject import tools
from openobject.tools import expose, redirect, ast


def datas_read(ids, model, fields, context=None):
    ctx = dict((context or {}), **rpc.session.context)
    return rpc.RPCProxy(model).export_data(ids, fields, ctx)

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
        raise common.message(_("Operation failed\nI/O error")+"(%s)" % (errno,))

def _fields_get_all(model, views, context=None):
    
    context = context or {}

    def parse(root, fields):

        for node in root.childNodes:

            if node.nodeName in ('form', 'notebook', 'page', 'group', 'tree', 'hpaned', 'vpaned'):
                parse(node, fields)

            elif node.nodeName=='field':
                attrs = node_attributes(node)
                name = attrs['name']

                fields[name].update(attrs)

        return fields

    proxy = rpc.RPCProxy(model)

    v1 = proxy.fields_view_get(views.get('tree', False), 'tree', context)
    v2 = proxy.fields_view_get(views.get('form', False), 'form', context)

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

class ImpEx(SecuredController):

    _cp_path = "/openerp/impex"

    @expose(template="/openerp/controllers/templates/exp.mako")
    def exp(self, **kw):
        params, data = TinyDict.split(kw)
        
        ctx = dict((params.context or {}), **rpc.session.context)

        views = {}
        if params.view_mode and params.view_ids:
            for i, view in enumerate(params.view_mode):
                views[view] = params.view_ids[i]


        proxy = rpc.RPCProxy('ir.exports')
        new_list = []

        headers = [{'string' : 'Name', 'name' : 'name', 'type' : 'char'}]
        tree = treegrid.TreeGrid('export_fields',
                                 model=params.model,
                                 headers=headers,
                                 url=tools.url('/openerp/impex/get_fields'),
                                 field_parent='relation',
                                 context=ctx,
                                 views=views)

        tree.show_headers = False

        view = proxy.fields_view_get(False, 'tree', ctx)
        new_list = listgrid.List(name='_terp_list', model='ir.exports', view=view, ids=None,
                                 domain=[('resource', '=', params.model)],
                                 context=ctx, selectable=1, editable=False, pageable=False)


        return dict(new_list=new_list, model=params.model, ids=params.ids, ctx=ctx,
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

        raise redirect('/openerp/impex/exp', **kw)

    @expose()
    def delete_listname(self, **kw):

        params, data = TinyDict.split(kw)
        proxy = rpc.RPCProxy('ir.exports')

        proxy.unlink(params.id)

        raise redirect('/openerp/impex/exp', **kw)

    @expose('json')
    def get_fields(self, model, prefix='', name='', field_parent=None, **kw):

        is_importing = kw.get('is_importing', False)        
        
        try:
            ctx = ast.literal_eval(kw['context'])
        except:
            ctx = {}
            
        ctx.update(**rpc.session.context)

        ids = kw.get('ids', '').split(',')
        ids = [i for i in ids if i]
        
        try:
            views = ast.literal_eval(kw['views'])
        except:
            views = {}
            

        fields = _fields_get_all(model, views, ctx)
        fields.update({'id': {'string': 'ID'}, 'db_id': {'string': 'Database ID'}})

        fields_order = fields.keys()
        fields_order.sort(lambda x,y: -cmp(fields[x].get('string', ''), fields[y].get('string', '')))

        records = []

        for i, field in enumerate(fields_order):

            value = fields[field]
            record = {}

            id = prefix + (prefix and '/' or '') + field
            nm = name + (name and '/' or '') + value['string']

            if is_importing and (value.get('type') not in ('reference',)) and (not value.get('readonly', False) \
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
#                if ids:
#                    record['id'] = ids[i]
#                else:
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

                    children.append(cid)

                record['children'] = children or None
                record['params'] = {'model': ref, 'prefix': id, 'name': nm}

        records.reverse()
        return dict(records=records)


    @expose('json')
    def get_namelist(self, **kw):

        params, data = TinyDict.split(kw)
        
        ctx = dict((params.context or {}), **rpc.session.context)
        
        res = []
        ids = []
        id = params.id

        res = self.get_data(params.model, ctx)

        ir_export = rpc.RPCProxy('ir.exports')
        ir_export_line = rpc.RPCProxy('ir.exports.line')

        field = ir_export.read(id)
        fields = ir_export_line.read(field['export_fields'])

        name_list = []
        ids = [f['name'] for f in fields]

        for name in ids:
            name_list += [(name, res.get(name))]

        return dict(name_list=name_list)

    def get_data(self, model, context=None):

        ids = []
        context = context or {}

        fields_data = {}
        proxy = rpc.RPCProxy(model)
        fields = proxy.fields_get(False, rpc.session.context)

        # XXX: in GTK client, top fields comes from Screen
        if not ids:
            f1 = proxy.fields_view_get(False, 'tree', context)['fields']
            f2 = proxy.fields_view_get(False, 'form', context)['fields']

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
            fields.update({'id': {'string': 'ID'}, 'db_id': {'string': 'Database ID'}})
            model_populate(fields)

            return _fields

        return rec(fields)

    @expose(content_type="application/octet-stream")
    def export_data(self, fname, fields, export_as="csv", add_names=False, import_compat=False, **kw):

        params, data = TinyDict.split(kw)
        proxy = rpc.RPCProxy(params.model)

        if isinstance(fields, basestring):
            fields = [fields]

        ctx = dict((params.context or {}), **rpc.session.context)
        ctx['import_comp'] = import_compat

        domain = params.seach_domain or []

        ids = params.ids or proxy.search(domain, 0, 0, 0, ctx)
        result = datas_read(ids, params.model, fields, context=ctx)

        if result.get('warning', False):
            common.warning(unicode(result.get('warning', False)), _('Export Error'))
            return False
        result = result.get('datas',[])

        if import_compat:
            params.fields2 = fields

        if export_as == 'xls':
            try:
                import xlwt
            except Exception, e:
                  raise common.warning(_('Please Install xlwt Library.\nTo create spreadsheet files compatible with MS Excel.'), _('Import Error.'))

            ezxf = xlwt.easyxf

            fp = StringIO.StringIO()

            wb = xlwt.Workbook()
            worksheet = wb.add_sheet('Sheet 1')

            for col in range(len(params.fields2)):
                worksheet.write(0, col, ustr(params.fields2[col]))
                col+1

            heading_xf = ezxf('align: wrap yes')

            for data in range(len(result)):
                for d in range(len(result[data])):
                    try:
                        result[data][d] = ustr(result[data][d])
                    except:
                        pass
                    result[data][d] = re.sub("\r", " ", result[data][d])
                    worksheet.write(data+1, d, result[data][d], heading_xf)
                    worksheet.col(d).width = 8000
                    d+1

            wb.save(fp)

            fp.seek(0)
            data = fp.read()
            return data
        else:
            return export_csv(params.fields2, result, add_names)

    @expose(template="/openerp/controllers/templates/imp.mako")
    def imp(self, **kw):
        params, data = TinyDict.split(kw)
        
        ctx = dict((params.context or {}), **rpc.session.context)
        
        views = {}
        if params.view_mode and params.view_ids:
            for i, view in enumerate(params.view_mode):
                views[view] = params.view_ids[i]

        headers = [{'string' : 'Name', 'name' : 'name', 'type' : 'char'}]
        tree = treegrid.TreeGrid('import_fields',
                                    model=params.model,
                                    headers=headers,
                                    url=tools.url('/openerp/impex/get_fields'),
                                    field_parent='relation',
                                    views=views,
                                    context=ctx,
                                    is_importing=1)

        tree.show_headers = False

        return dict(model=params.model, source=params.source, tree=tree, fields=kw.get('fields', {}))

    @expose()
    def detect_data(self, csvfile, csvsep, csvdel, csvcode, csvskip, **kw):
        params, data = TinyDict.split(kw)

        _fields = {}
        _fields_invert = {}
        
        fields = rpc.RPCProxy(params.model).fields_get(False, rpc.session.context)
        
        def model_populate(fields, prefix_node='', prefix=None, prefix_value='', level=2):
            def str_comp(x,y):
                if x<y: return 1
                elif x>y: return -1
                else: return 0

            fields_order = fields.keys()
            fields_order.sort(lambda x,y: str_comp(fields[x].get('string', ''), fields[y].get('string', '')))
            for field in fields_order:
                if (fields[field].get('type','') not in ('reference',))\
                            and (not fields[field].get('readonly', False)\
                            or not dict(fields[field].get('states', {}).get(
                            'draft', [('readonly', True)])).get('readonly',True)):
                    
                    st_name = prefix_value+fields[field]['string'] or field
                    _fields[prefix_node+field] = st_name
                    _fields_invert[st_name] = prefix_node+field
                    if fields[field].get('type','')=='one2many' and level>0:
                        fields2 = rpc.session.execute('object', 'execute', fields[field]['relation'], 'fields_get', False, rpc.session.context)
                        fields2.update({'id': {'type': 'char', 'string': 'ID'}, 'db_id':{'type': 'char', 'string': 'Database ID'}})
                        model_populate(fields2, prefix_node+field+'/', None, st_name+'/', level-1)
                    if fields[field].get('type','') in ('many2one', 'many2many' ) and level>0:
                        model_populate({'id': {'type': 'char', 'string': 'ID'}, 'db_id': {'type': 'char', 'string': 'Database ID'}},
                                       prefix_node+field+':', None, st_name+'/', level-1)

        fields.update({'id': {'type': 'char', 'string': 'ID'}, 'db_id': {'type': 'char', 'string': 'Database ID'}})
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
                    if word in _fields:
                        fields += [(word, _fields[word])]
                    elif word in _fields_invert.keys():
                        fields += [(_fields_invert[word], word)]
                    else:
                        raise common.warning(_("You cannot import this field %s, because we cannot auto-detect it" % (word,)))
                break
        except:
            raise common.warning(_('Error processing your first line of the file.\nField %s is unknown') % (word,), _('Import Error.'))

        kw['fields'] = fields
        return self.imp(**kw)

    @expose()
    def import_data(self, csvfile, csvsep, csvdel, csvcode, csvskip, fields=[], **kw):

        params, data = TinyDict.split(kw)

        content = csvfile.file.read()
        input=StringIO.StringIO(content)
        data = list(csv.reader(input, quotechar=str(csvdel), delimiter=str(csvsep)))[int(csvskip):]
        datas = []
        ctx = dict(**rpc.session.context)
        
        if not isinstance(fields, list):
            fields = [fields]

        for line in data:
            try:
                datas.append(map(lambda x:x.decode(csvcode).encode('utf-8'), line))
            except:
                datas.append(map(lambda x:x.decode('latin').encode('utf-8'), line))
        try:
            res = rpc.session.execute('object', 'execute', params.model, 'import_data', fields, datas, 'init', '', False, ctx)
        except Exception, e:
            raise common.warning(ustr(e), _('XML-RPC error'))
        if res[0]>=0:
            raise common.message(_('Imported %d objects') % (res[0],))
        else:
            d = ''
            for key,val in res[1].items():
                d+= ('\t%s: %s\n' % (ustr(key),ustr(val)))
            error = _('Error trying to import this record:\n%s\nError Message:\n%s\n\n%s') % (d,res[2],res[3])
            raise common.warning(unicode(error), _('Importation Error'))

        return self.imp(**kw)


# vim: ts=4 sts=4 sw=4 si et

