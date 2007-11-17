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

import os
import time
import types
import base64

import csv
import StringIO

from turbogears import expose
from turbogears import controllers

import cherrypy

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp.tinyres import TinyResource
from tinyerp.utils import TinyDict

import tinyerp.widgets as tw

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
                if type(d)==types.StringType:
                    row.append(d.replace('\n',' ').replace('\t',' '))
                else:
                    row.append(d)
            writer.writerow(row)

        fp.seek(0)
        data = fp.read()
        fp.close()

        return data
    except IOError, (errno, strerror):
        raise common.message(_("Operation failed !\nI/O error")+"(%s)" % (errno,))

class ImpEx(controllers.Controller, TinyResource):

    @expose(template="tinyerp.subcontrollers.templates.exp")
    def exp(self, **kw):
        params, data = TinyDict.split(kw)

        headers = [{'string' : 'Name', 'name' : 'name', 'type' : 'char'}]
        tree = tw.treegrid.TreeGrid('export_fields', model=params.model, headers=headers, url='/impex/get_fields', field_parent='relation')
        tree.show_headers = False

        return dict(model=params.model, ids=params.ids, search_domain=params.search_domain, source=params.source, tree=tree, show_header_footer=False)

    @expose('json')
    def get_fields(self, model, prefix='', name='', field_parent=None, **kw):

        is_importing = len(eval(kw.get('domain')))

        ids = kw.get('ids', '').split(',')
        ids = [i for i in ids if i]

        proxy = rpc.RPCProxy(model)
        fields = proxy.fields_get(False, rpc.session.context)

        # XXX: in GTK client, top fields comes from Screen
        if not ids:
            f1 = proxy.fields_view_get(False, 'tree', rpc.session.context)['fields']
            f2 = proxy.fields_view_get(False, 'form', rpc.session.context)['fields']

            fields = {}
            fields.update(f1)
            fields.update(f2)

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
                record['data'] = {'name' : nm}
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

                record['data'] = {'name' : nm}
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

                record['children'] = children
                record['params'] = {'model': ref, 'prefix': id, 'name': nm}

        records.reverse()
        return dict(records=records)

    @expose(content_type="application/octat-stream")
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

    @expose(template="tinyerp.subcontrollers.templates.imp")
    def imp(self, **kw):
        params, data = TinyDict.split(kw)

        headers = [{'string' : 'Name', 'name' : 'name', 'type' : 'char'}]
        tree = tw.treegrid.TreeGrid('import_fields', model=params.model, headers=headers, url='/impex/get_fields', field_parent='relation')
        tree.show_headers = False
        tree.domain = [()] # will be used in `get_fields` as flag

        return dict(model=params.model, source=params.source, tree=tree, fields=kw.get('fields', {}), show_header_footer=False)

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
            raise common.warning('Error opening .CSV file', 'Input Error.')

        fields = []
        word=''
        try:
            for line in data:
                for word in line:
                    word=word.decode(csvcode).encode('utf-8')
                    fields += [(_fields_invert[word], word)]
                break
        except:
            raise common.warning('Error processing your first line of the file.\nField %s is unknown !' % (word,), 'Import Error.')

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
        for line in data:
            datas.append(map(lambda x:x.decode(csvcode).encode('utf-8'), line))
        try:
            res = rpc.session.execute('object', 'execute', params.model, 'import_data', fields, datas)
        except Exception, e:
            raise common.warning(str(e), _('XML-RPC error !'))
        if res[0]>=0:
            raise common.message(_('Imported %d objects !') % (res[0],))
        else:
            d = ''
            for key,val in res[1].items():
                d+= ('\t%s: %s\n' % (str(key),str(val)))
            error = u'Error trying to import this record:\n%s\nError Message:\n%s\n\n%s' % (d,res[2],res[3])
            raise common.error('Importation Error !', unicode(error))

        return self.imp(**kw)
