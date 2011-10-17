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
import simplejson
from openerp.utils import rpc, expr_eval, TinyDict, TinyForm, TinyFormError

import actions
from form import Form
from error_page import _ep
import openobject.i18n.format
from openobject.tools import expose, ast

class Search(Form):

    _cp_path = "/openerp/search"

    @expose(template="/openerp/controllers/templates/search.mako")
    def create(self, params, tg_errors=None):

        params.view_mode = ['tree', 'form']
        params.view_type = 'tree'

        params.offset = params.offset or 0
        params.limit = params.limit or 50
        params.count = params.count or 0
        params.filter_domain = params.filter_domain or []
        params.editable = 0

        form = self.create_form(params, tg_errors)

        # don't show links in list view, except the do_select link
        form.screen.widget.show_links = 0
        if params.get('return_to'):
            proxy = rpc.RPCProxy(params.model)
            records = proxy.read(params.ids, ['name'], rpc.session.context)
            params['grp_records'] = records
        return dict(form=form, params=params, form_name = form.screen.widget.name)

    @expose()
    def new(self, model, source=None, kind=0, text=None, domain=None, context=None, **kw):
        """Create new search view...

        @param model: the model
        @param source: the source, in case of m2m, m2o search
        @param kind: 0=normal, 1=m2o, 2=m2m
        @param text: do `name_search` if text is provided
        @param domain: the domain
        @param context: the context
        """

        params = TinyDict()

        params.model = model
        params.domain = domain or []
        params.context = context or {}

        params.source = source
        params.selectable = kind
        params.limit = params.limit or 50

        ctx = dict(rpc.session.context,
                   **(params.context or {}))
        params.ids = []
        proxy = rpc.RPCProxy(model)
        params.search_text = False

        if text:
            params.search_text = True
            ids = proxy.name_search(text, params.domain or [], 'ilike', ctx, False)

            if ids:
                params.ids = [id[0] for id in ids]

                # For m2o, when name_search is called, then its result will be added to existing domain
                params.domain.append(('id','in', params.ids))

                params.count = len(ids)
            else:
                params.context['default_name'] = ustr(text)
        elif 'default_name'in params.context:
            del params.context['default_name']

        if kw.get('return_to'):
            params['return_to'] = ast.literal_eval(kw['return_to'])
            
        return self.create(params)

    @expose('json')
    def eval_domain_and_context(self, **kw):
        params, data = TinyDict.split(kw)

        domain = kw.get('_terp_domain', [])
        context = params.context or {}
        parent_context = dict(params.parent_context or {},
                              **rpc.session.context)
        parent_context = self.context_get(params.parent_context) or {}
        if 'group_by' in parent_context:
            if isinstance(params.group_by, str):
                parent_context['group_by'] = params.group_by.split(',')
            else:
                parent_context['group_by'] = params.group_by
        try:
            ctx = TinyForm(**kw).to_python()
            pctx = ctx
        except TinyFormError, e:
            return dict(error_field=e.field, error=ustr(e))
        except Exception, e:
            return dict(error=_ep.render())

        prefix = params.prefix
        if prefix:
            ctx = ctx.chain_get(prefix)

        if prefix and '/' in prefix:
            prefix = prefix.rsplit('/', 1)[0]
            pctx = pctx.chain_get(prefix)

        #update active_id in context for links
        parent_context.update(
            active_id=params.active_id or False,
            active_ids=params.active_ids or [])

        ctx.update(
            parent=pctx,
            context=parent_context,
            active_id=params.active_id or False,
            active_ids=params.active_ids or []
        )

        if params.active_id and not params.active_ids:
            ctx['active_ids'] = [params.active_id]

        if domain and isinstance(domain, basestring):
            domain = expr_eval(domain, ctx)

        if domain and len(domain) >= 2 and domain[-2] in ['&', '|']: # For custom domain ('AND', OR') from search view.
            dom1 = domain[-1:]
            dom2 = domain[:-2]
            domain = dom2 + dom1

        if context and isinstance(context, basestring):
            if not context.startswith('{'):
                context = "dict(%s)"%context
                ctx['dict'] = dict # required

            context = expr_eval(context, ctx)

#           Fixed many2one pop up in listgrid when value is None.
            for key, val in context.items():
                if val is None:
                    context[key] = False

        for key, val in context.items():
            if key in ctx:
                context[key] = ctx[key]

        if isinstance(context, dict):
            context = expr_eval(context, ctx)
        parent_context.update(context)

        if isinstance(params.group_by, basestring):
            params.group_by = params.group_by.split(',')
        elif not isinstance(params.group_by, list):
            params.group_by = []

        # Fixed header string problem for m2m,m2o field when parent context takes '_terp_view_name'
        parent_context.pop('_terp_view_name', None)
        # parent's search_view has no business being in m2o or m2m
        parent_context.pop('search_view', None)

        return dict(domain=ustr(domain), context=ustr(parent_context), group_by = ustr(params.group_by))

    @expose('json')
    def get(self, **kw):

        params, data = TinyDict.split(kw)

        error = None
        error_field = None

        model = params.model

        record = kw.get('record')
        record = eval(record)
        proxy = rpc.RPCProxy(model)
        data = {}
        res = proxy.fields_get(False, rpc.session.context)

        all_values = {}
        errors = []
        for k, v in record.items():
            values = {}
            for key, val in v.items():
                for field in val:
                    fld = {
                        'value': val[field],
                        'type': res[field].get('type')
                    }
                    if fld['type'] == 'many2many':
                        fld['type'] = 'char'
                    datas = {field: fld}

                    try:
                        TinyForm(**datas).to_python()
                    except TinyFormError, e:
                        errors.append({e.field: ustr(e)})
                    except Exception, e:
                        errors.append({field: ustr(e)})

                    datas['rec'] = field
                    
                    datas['rec_val'] = fld['value']

                datas['type'] = fld['type']
                values[key] = datas

            all_values[k] = values

        return dict(frm=all_values, errors=errors)

    @expose('json')
    def eval_domain_filter(self, **kw):

        all_domains = kw.get('all_domains')
        custom_domains = kw.get('custom_domain')

        all_domains = eval(all_domains)

        domains = all_domains.get('domains')
        selection_domain = all_domains.get('selection_domain')
        search_context = all_domains.get('search_context')

        group_by_ctx = kw.get('group_by_ctx', [])
        if isinstance(group_by_ctx, str):
            group_by_ctx = group_by_ctx.split(',')

        if domains:
            domains = eval(domains)

        c = search_context.get('context', {})
        v = search_context.get('value')
        if v and isinstance(v, basestring) and '__' in v:
            value, operator = v.split('__')
            v = int(value)
        ctx = expr_eval(c, {'self':v})

        context = rpc.session.context
        if ctx:
            ctx.update(context)

        domain = []
        check_domain = all_domains.get('check_domain')

        if check_domain and isinstance(check_domain, basestring):
            domain = expr_eval(check_domain, context) or []

        search_data = {}
        model = kw.get('model')
        proxy = rpc.RPCProxy(model)
        res = proxy.fields_get(False, context)
        all_error = []
        fld = {}
        
        if domains:
            for field, value in domains.iteritems():
                
                if '/' in field:
                    fieldname, bound = field.split('/')
                else:
                    fieldname = field
                    bound = ''

                data = {}
                fld['type'] = res[fieldname].get('type')
                if fld['type'] == 'many2many':
                    fld['type'] = 'char'
                fld['value'] = value
                data[field] = fld

                try:
                    frm = TinyForm(**data).to_python()
                except TinyFormError, e:
                    error_field = e.field
                    error = ustr(e)
                    all_error.append(dict(error=error, error_field=error_field))
                    continue

                if bound in ('from', 'to'):
                    if bound == 'from': test = '>='
                    else: test = '<='

                    convert_format = openobject.i18n.format.convert_date_format_in_domain([(fieldname, test, value)], res, context)
                    domain.append(convert_format[0])
                    search_data.setdefault(fieldname, {})[bound] = convert_format[0][2]

                elif isinstance(value, bool) and value:
                    search_data[field] = 1

                elif isinstance(value, int) and not isinstance(value, bool):
                    domain.append((field, '=', value))
                    search_data[field] = value

                elif 'selection_' in value:
                    domain.append((field, '=', value.split('selection_')[1]))
                    search_data[field] = value.split('selection_')[1]

                elif fld['type'] == 'selection':
                    domain.append((field, '=', value))
                    search_data[field] = value

                else:
                    if not 'm2o_' in value:
                        operator = 'ilike'
                        if '__' in value:
                            value, operator = value.split('__')
                            value = int(value)
                        domain.append((field, operator, value))
                        search_data[field] = value
                    else:
                        search_data[field] = value.split('m2o_')[1]
            if all_error:
                return dict(all_error=all_error)

        if not custom_domains:
            custom_domains = []
        else:
            try:
                # from JS custom filters, data is sent as JSON
                custom_domains = simplejson.loads(custom_domains)
            except simplejson.decoder.JSONDecodeError:
                # from switchView, data is sent as Python literals
                # (with unicode strings and keys)
                custom_domains = ast.literal_eval(custom_domains)
        
        # conversion of the pseudo domain from the javascript to a valid domain
        ncustom_domain = []
        for i in xrange(max(len(custom_domains) - 1, 0)):
            ncustom_domain.append("|")
        for and_list in custom_domains:
            for i in xrange(max(len(and_list) - 1, 0)):
                ncustom_domain.append("&")
            ncustom_domain += [tuple(x) for x in and_list]

        if selection_domain and selection_domain not in ['blk', 'sf', 'mf']:
            selection_domain = expr_eval(selection_domain)
            if selection_domain:
                domain.extend(selection_domain)

        for i,flt in enumerate(ncustom_domain):
            if len(flt) > 1:

                left_field = flt[0]
                operator = flt[1]
                right_val = flt[2]

                if res[left_field]['type'] == 'selection' and right_val:

                    if operator in ['ilike','=','in']:
                        operator = 'in'
                    else:
                        operator = 'not in'

                    keys = []
                    if isinstance(right_val, list):
                        for sel_val in res[left_field]['selection']:
                            for rgt_val in right_val:
                                if sel_val[1].lower().find(rgt_val.lower()) != -1 and sel_val[0] not in keys:
                                    keys.append(sel_val[0])
                    else:
                        for sel_val in res[left_field]['selection']:
                            if sel_val[1].lower().find(right_val.lower()) != -1:
                                keys.append(sel_val[0])

                    if keys:
                        ncustom_domain[i] = (left_field, operator, keys)

        if not domain:
            domain = None
        if not isinstance(group_by_ctx, list):
            group_by_ctx = [group_by_ctx]
        if group_by_ctx:
            search_data['group_by_ctx'] = group_by_ctx
        ncustom_domain = openobject.i18n.format.convert_date_format_in_domain(ncustom_domain, res, context)
        return dict(domain=ustr(domain), context=ustr(ctx), search_data=ustr(search_data), filter_domain=ustr(ncustom_domain))

    @expose()
    def manage_filter(self, **kw):
        act={'name':'Manage Filters',
                 'res_model':'ir.filters',
                 'type':'ir.actions.act_window',
                 'view_type':'form',
                 'view_mode':'tree,form',
                 'domain':'[(\'model_id\',\'=\',\''+kw.get('model')+'\'),(\'user_id\',\'=\','+str(rpc.session.uid)+')]'}

        return actions.execute(act, context=rpc.session.context)

    @expose(template="/openerp/controllers/templates/save_filter.mako")
    def save_filter(self, **kw):
        model = kw.get('model')
        domain = kw.get('domain')
        if isinstance(domain,basestring):
            domain = eval(domain) or []

        custom_filter = kw.get('custom_filter')
        if isinstance(custom_filter,basestring):
            custom_filter = eval(custom_filter)

        if custom_filter:
            domain.extend(i for i in custom_filter if i not in domain)

        flag = kw.get('flag')
        group_by = kw.get('group_by',None)
        selected_filter = kw.get('selected_filter')
        if not isinstance(group_by, list) and group_by:
            group_by = group_by.split(',')

        if group_by:
            group_by_ctx = map(lambda x: x.split('group_')[-1], group_by)
        else:
            group_by_ctx = []
        return dict(model=model, domain=domain, flag=flag, group_by=group_by_ctx, filtername=selected_filter)

    @expose('json')
    def do_filter_sc(self, **kw):
        name = kw.get('name')
        model = kw.get('model')
        domain = kw.get('domain')
        group_by = kw.get('group_by', '[]')
        if group_by:
            context = {'group_by': group_by}
        else:
            context = {}
        if name:
            datas = {
                'name':name,
                'model_id':model,
                'domain':domain,
                'context':str(context),
                'user_id':rpc.session.uid
            }
            result = rpc.session.execute('object', 'execute', 'ir.filters', 'create_or_replace', datas, rpc.session.context)
            return {'filter': (domain, name, group_by), 'new_id':result}
        return {}

    @expose('json')
    def ok(self, **kw):
        params, data = TinyDict.split(kw)

        ids = [int(id) for id in data.get('search_list', [])]
        return dict(ids=ids)

    @expose('json')
    def get_name(self, model, id):
        return dict(name=rpc.name_get(model, id, rpc.session.context))

    @expose('json')
    def get_matched(self, model, text, limit=10, **kw):
        params, data = TinyDict.split(kw)

        ctx = dict(rpc.session.context,
                   **(params.context or {}))

        try:
            return {
                'values': rpc.RPCProxy(model).name_search(text, (params.domain or []), 'ilike', ctx, int(limit)),
                'error': None
            }
        except Exception, e:
            return {'error': ustr(e), 'values': False}

    def context_get(self, parent_context):
        # Need to remove default keys,group_by,search_default of the parent context
        context_own = dict(parent_context)
        for ctx in parent_context.items():
            if ctx[0].startswith('default_') or ctx[0] in ('set_editable','set_visible')\
             or ctx[0] == 'group_by' or ctx[0].startswith('search_default_'):
                del context_own[ctx[0]]

        return context_own
