###############################################################################
#
#  Copyright (C) 2007-TODAY OpenERP SA. All Rights Reserved.
#
#  $Id$
#
#  Developed by OpenERP (http://openerp.com) and Axelor (http://axelor.com).
#
#  The OpenERP web client is distributed under the "OpenERP Public License".
#  It's based on Mozilla Public License Version (MPL) 1.1 with following 
#  restrictions:
#
#  -   All names, links and logos of OpenERP must be kept as in original
#      distribution without any changes in all software screens, especially
#      in start-up page and the software header, even if the application
#      source code has been changed or updated or code has been added.
#
#  You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################
import StringIO
import csv
import xml.dom.minidom
import cherrypy

from openerp.controllers import SecuredController
from openerp.utils import rpc, common, TinyDict, node_attributes
from openerp.widgets import treegrid

from openobject import tools
from openobject.tools import expose, redirect, ast




def datas_read(ids, model, flds, context=None):
    ctx = dict((context or {}), **rpc.session.context)
    return rpc.RPCProxy(model).export_data(ids, flds, ctx)

def export_csv(fields, result):
    try:
        fp = StringIO.StringIO()
        writer = csv.writer(fp, quoting=csv.QUOTE_ALL)

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
                if d is False: d = None
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

    def get_view_fields(view):
        return parse(
            xml.dom.minidom.parseString(view['arch'].encode('utf-8')).documentElement,
            view['fields'])

    proxy = rpc.RPCProxy(model)

    tree_view = proxy.fields_view_get(views.get('tree', False), 'tree', context)
    form_view = proxy.fields_view_get(views.get('form', False), 'form', context)

    fields = {}
    fields.update(get_view_fields(tree_view))
    fields.update(get_view_fields(form_view))

    return fields


class ImpEx(SecuredController):

    _cp_path = "/openerp/impex"

    @expose(template="/openerp/controllers/templates/exp.mako")
    def exp(self, import_compat="1", **kw):

        params, data = TinyDict.split(kw)
        ctx = dict((params.context or {}), **rpc.session.context)

        views = {}
        if params.view_mode and params.view_ids:
            for i, view in enumerate(params.view_mode):
                views[view] = params.view_ids[i]


        exports = rpc.RPCProxy('ir.exports')

        headers = [{'string' : 'Name', 'name' : 'name', 'type' : 'char'}]
        tree = treegrid.TreeGrid('export_fields',
                                 model=params.model,
                                 headers=headers,
                                 url=tools.url('/openerp/impex/get_fields'),
                                 field_parent='relation',
                                 context=ctx,
                                 views=views,
                                 import_compat=int(import_compat))

        tree.show_headers = False

        existing_exports = exports.read(
            exports.search([('resource', '=', params.model)], context=ctx),
            [], ctx)

        return dict(existing_exports=existing_exports, model=params.model, ids=params.ids, ctx=ctx,
                    search_domain=params.search_domain, source=params.source,
                    tree=tree, import_compat=import_compat)

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

        parent_field = kw.get('ids').split(',')[0].split('/')
        if len(parent_field) == 1:
            parent_field = parent_field[0]
        else:
            parent_field = parent_field[-2]

        is_importing = kw.get('is_importing', False)
        import_compat= bool(int(kw.get('import_compat', True)))

        try:
            ctx = ast.literal_eval(kw['context'])
        except:
            ctx = {}

        ctx.update(**rpc.session.context)

        try:
            views = ast.literal_eval(kw['views'])
        except:
            views = {}

        fields = _fields_get_all(model, views, ctx)
        m2ofields = cherrypy.session.get('fld')
        if m2ofields:
            for i in m2ofields:
                if i == parent_field:
                    fields = {}
        else:
            m2ofields = []

        fields.update({'id': {'string': 'ID'}, '.id': {'string': 'Database ID'}})

        fields_order = fields.keys()
        fields_order.sort(lambda x,y: -cmp(fields[x].get('string', ''), fields[y].get('string', '')))
        records = []


        for i, field in enumerate(fields_order):
            value = fields[field]
            record = {}

            if import_compat and value.get('readonly', False):
                ok = False
                for sl in value.get('states', {}).values():
                    for s in sl:
                        ok = ok or (s==('readonly',False))
                if not ok: continue
                
            id = prefix + (prefix and '/' or '') + field
            nm = name + (name and '/' or '') + value['string']

            if is_importing and (value.get('type') not in ('reference',)) and (not value.get('readonly') \
                        or not dict(value.get('states', {}).get('draft', [('readonly', True)])).get('readonly', True)):

                record.update(id=id, items={'name': nm},
                              action='javascript: void(0)', target=None,
                              icon=None, children=[],
                              required=value.get('required', False))

                records.append(record)

            elif not is_importing:

                record.update(id=id, items={'name': nm},
                              action='javascript: void(0)', target=None,
                              icon=None, children=[])
                records.append(record)


            if len(nm.split('/')) < 3 and value.get('relation', False):

                if import_compat or is_importing:
                    ref = value.pop('relation')
                    proxy = rpc.RPCProxy(ref)
                    cfields = proxy.fields_get(False, rpc.session.context)
                    if (value['type'] == 'many2many') and not is_importing:
                        record['children'] = None
                        record['params'] = {'model': ref, 'prefix': id, 'name': nm}

                    elif (value['type'] == 'many2one') or (value['type'] == 'many2many' and is_importing):
                        m2ofields.append(field)
                        cfields_order = cfields.keys()
                        cfields_order.sort(lambda x,y: -cmp(cfields[x].get('string', ''), cfields[y].get('string', '')))
                        children = []
                        for j, fld in enumerate(cfields_order):
                            cid = id + '/' + fld
                            cid = cid.replace(' ', '_')
                            children.append(cid)
                        record['children'] = children or None
                        record['params'] = {'model': ref, 'prefix': id, 'name': nm}
                        cherrypy.session['fld'] = m2ofields

                    else:
                        cfields_order = cfields.keys()
                        cfields_order.sort(lambda x,y: -cmp(cfields[x].get('string', ''), cfields[y].get('string', '')))
                        children = []
                        for j, fld in enumerate(cfields_order):
                            cid = id + '/' + fld
                            cid = cid.replace(' ', '_')
                            children.append(cid)
                        record['children'] = children or None
                        record['params'] = {'model': ref, 'prefix': id, 'name': nm}

                else:
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
                    cherrypy.session['fld'] = []

        records.reverse()
        return dict(records=records)


    @expose('json')
    def namelist(self, **kw):

        params, data = TinyDict.split(kw)

        ctx = dict((params.context or {}), **rpc.session.context)

        id = params.id

        res = self.get_data(params.model, ctx)
        ir_export = rpc.RPCProxy('ir.exports')
        ir_export_line = rpc.RPCProxy('ir.exports.line')

        field = ir_export.read(id)
        fields = ir_export_line.read(field['export_fields'])

        name_list = [
                (f['name'], res.get(f['name']))
                for f in fields]

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

            fields = dict(f1)
            fields.update(f2)

        def rec(fields):
            _fields = {'id': 'ID' , '.id': 'Database ID' }

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
    def export_data(self, fname, fields, import_compat=False, **kw):

        params, data_index = TinyDict.split(kw)
        proxy = rpc.RPCProxy(params.model)

        flds = []
        for item in fields:
            fld = item.replace('/.id','.id')
            flds.append(fld)

        if isinstance(fields, basestring):
            fields = fields.replace('/.id','.id')
            flds = [fields]


        ctx = dict((params.context or {}), **rpc.session.context)
        ctx['import_comp'] = bool(int(import_compat))

        domain = params.seach_domain or []

        ids = params.ids or proxy.search(domain, 0, 0, 0, ctx)
        result = datas_read(ids, params.model, flds, context=ctx)

        if result.get('warning'):
            common.warning(unicode(result.get('warning', False)), _('Export Error'))
            return False
        result = result.get('datas',[])

        if import_compat:
            params.fields2 = flds

        return export_csv(params.fields2, result)

    @expose(template="/openerp/controllers/templates/imp.mako")
    def imp(self, error=None, records=None, success=None, **kw):
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
        return dict(error=error, records=records, success=success,
                    model=params.model, source=params.source,
                    tree=tree, fields=kw.get('fields', {}))

    @expose()
    def detect_data(self, csvfile, csvsep, csvdel, csvcode, csvskip, **kw):
        params, data = TinyDict.split(kw)

        _fields = {}
        _fields_invert = {}
        error = None

        fields = dict(rpc.RPCProxy(params.model).fields_get(False, rpc.session.context))
        fields.update({'id': {'string': 'ID'}, '.id': {'string': 'Database ID'}})

        def model_populate(fields, prefix_node='', prefix=None, prefix_value='', level=2):
            def str_comp(x,y):
                if x<y: return 1
                elif x>y: return -1
                else: return 0

            fields_order = fields.keys()
            fields_order.sort(lambda x,y: str_comp(fields[x].get('string', ''), fields[y].get('string', '')))
            for field in fields_order:
                if (fields[field].get('type','') not in ('reference',))\
                            and (not fields[field].get('readonly')\
                            or not dict(fields[field].get('states', {}).get(
                            'draft', [('readonly', True)])).get('readonly',True)):

                    st_name = prefix_value+fields[field]['string'] or field
                    _fields[prefix_node+field] = st_name
                    _fields_invert[st_name] = prefix_node+field

                    if fields[field].get('type','')=='one2many' and level>0:
                        fields2 = rpc.session.execute('object', 'execute', fields[field]['relation'], 'fields_get', False, rpc.session.context)
                        model_populate(fields2, prefix_node+field+'/', None, st_name+'/', level-1)

                    if fields[field].get('relation',False) and level>0:
                        model_populate({'/id': {'type': 'char', 'string': 'ID'}, '.id': {'type': 'char', 'string': 'Database ID'}},
                                       prefix_node+field, None, st_name+'/', level-1)
        fields.update({'id':{'string':'ID'},'.id':{'string':_('Database ID')}})
        model_populate(fields)


        try:
            data = csv.reader(csvfile.file, quotechar=str(csvdel), delimiter=str(csvsep))
        except:
            raise common.warning(_('Error opening .CSV file'), _('Input Error.'))


        records = []
        fields = []
        word=''
        limit = 3

        try:
            for i, row in enumerate(data):
                records.append(row)
                if i == limit:
                    break

            for line in records:
                for word in line:
                    word = ustr(word.decode(csvcode))
                    if word in _fields:
                        fields.append((word, _fields[word]))
                    elif word in _fields_invert.keys():
                        fields.append((_fields_invert[word], word))
                    else:
                        error = {'message':_("You cannot import the field '%s', because we cannot auto-detect it" % (word,))}
                break
        except:
            error = {'message':_('Error processing the first line of the file. Field "%s" is unknown') % (word,), 'title':_('Import Error.')}

        kw['fields'] = fields
        if error:
            csvfile.file.seek(0)
            return self.imp(error=dict(error, preview=csvfile.file.read(200)), **kw)
        return self.imp(records=records, **kw)

    @expose()
    def import_data(self, csvfile, csvsep, csvdel, csvcode, csvskip, fields=[], **kw):

        params, data = TinyDict.split(kw)
        res = None
        
        content = csvfile.file.read()
        input=StringIO.StringIO(content)
        limit = 0
        data = []

        if not (csvdel and len(csvdel) == 1):
            return self.imp(error={'message': _("The CSV delimiter must be a single character")}, **kw)

        try:
            for j, line in enumerate(csv.reader(input, quotechar=str(csvdel), delimiter=str(csvsep))):
                # If the line contains no data, we should skip it.
                if not line:
                    continue
                if j == limit:
                    fields = line
                else:
                    data.append(line)
        except csv.Error, e:
            return self.imp(
                error={
                    'message': ustr(e),
                    'title': _('File Format Error')
                },
                **kw)

        datas = []
        ctx = dict(rpc.session.context)

        if not isinstance(fields, list):
            fields = [fields]

        for line in data:
            try:
                datas.append(map(lambda x:x.decode(csvcode).encode('utf-8'), line))
            except:
                datas.append(map(lambda x:x.decode('latin').encode('utf-8'), line))
        
        # If the file contains nothing,
        if not datas:
            error = {'message': _('The file is empty !'), 'title': _('Importation !')}
            return self.imp(error=error, **kw)
        
        #Inverting the header into column names
        try:
            res = rpc.session.execute('object', 'execute', params.model, 'import_data', fields, datas, 'init', '', False, ctx)
        except Exception, e:
            error = {'message':ustr(e), 'title':_('XML-RPC error')}
            return self.imp(error=error, **kw)


        if res[0]>=0:
            return self.imp(success={'message':_('Imported %d objects') % (res[0],)}, **kw)

        d = ''
        for key,val in res[1].items():
            d+= ('%s: %s' % (ustr(key),ustr(val)))
        msg = _('Error trying to import this record:%s. ErrorMessage:%s %s') % (d,res[2],res[3])
        error = {'message':ustr(msg), 'title':_('ImportationError')}

        return self.imp(error=error, **kw)
