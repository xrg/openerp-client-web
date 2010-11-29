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
from openerp.utils import rpc, expr_eval, TinyDict, TinyForm, TinyFormError

import actions
from form import Form
from error_page import _ep
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
    def new(self, model, source=None, kind=0, text=None, domain=[], context={}, **kw):
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
        params.domain = domain
        params.context = context

        params.source = source
        params.selectable = kind
        params.limit = params.limit or 50

        ctx = rpc.session.context.copy()
        ctx.update(params.context or {})
        params.ids = []
        proxy = rpc.RPCProxy(model)
        ids = proxy.name_search(text or '', params.domain or [], 'ilike', ctx)
        params.search_text = False
        if ids:
            params.ids = [id[0] for id in ids]
            if len(ids) < params.limit or text:
                count = len(ids)
            else:
                count = proxy.search_count(params.domain, ctx)
            params.count = count
        if text:
            params.search_text = True
            # When id does not exists for m2o
            if not ids:
                params.context['default_name'] = text
        if kw and kw.get('return_to'):
            params['return_to'] = ast.literal_eval(kw['return_to'])

        return self.create(params)

    @expose('json')
    def eval_domain_and_context(self, **kw):
        params, data = TinyDict.split(kw)

        domain = kw.get('_terp_domain', [])
        context = params.context or {}

        parent_context = dict(params.parent_context or {},
                              **rpc.session.context)
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
        parent_context.update({'active_id':  params.active_id or False,
                              'active_ids':  params.active_ids or []})

        ctx['parent'] = pctx
        ctx['context'] = parent_context
        ctx['active_id'] = params.active_id or False
        ctx['active_ids'] = params.active_ids or []

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

        if isinstance(context, dict):
            context = expr_eval(context, ctx)

        parent_context.update(context)
        if not isinstance(params.group_by, list):
            params.group_by = params.group_by.split(',')

        # Fixed header string problem for m2m,m2o field when parent context takes '_terp_view_name'
        parent_context.pop('_terp_view_name', None)

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
        res = proxy.fields_get()

        frm = {}
        all_values = {}

        for k, v in record.items():
            values = {}
            for key, val in v.items():
                for field in val:
                    fld = {}
                    datas = {}
                    fld['value'] = val[field]
                    fld['type'] = res[field].get('type')

                    data[field] = fld
                    try:
                        frm = TinyForm(**data).to_python()
                    except TinyFormError, e:
                        error_field = e.field
                        error = ustr(e)
                        return dict(error=error, error_field=error_field)
                    except Exception, e:
                        error = ustr(e)
                        return dict(error=error, error_field=error_field)

                    datas['rec'] = field

                    if fld['type'] == 'many2one':
                        datas['rec_val'] = fld['value']
                        frm[field] = 'many2one'
                    elif isinstance(frm[field], bool):
                        if frm[field]:
                            datas['rec_val'] = 1
                        else:
                            datas['rec_val'] = 0
                    else:
                        datas['rec_val'] = frm[field]

                datas['type'] = fld['type']
                values[key] = datas

            all_values[k] = values

        return dict(frm=all_values, error=error)

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
        ctx = expr_eval(c, {'self':v})

        context = rpc.session.context
        if ctx:
            ctx.update(context)

        domain = []
        check_domain = all_domains.get('check_domain')

        if check_domain and isinstance(check_domain, basestring):
            domain = expr_eval(check_domain, context) or []

        search_data = {}
        if domains:
            for field, value in domains.iteritems():
                if '/' in field:
                    fieldname, bound = field.split('/')

                    if bound in ('from', 'to'):
                        if bound == 'from': test = '>='
                        else: test = '<='

                        domain.append((fieldname, test, value))
                        search_data.setdefault(fieldname, {})[bound] = value

                elif isinstance(value, bool) and value:
                    search_data[field] = 1

                elif isinstance(value, int) and not isinstance(value, bool):
                    domain.append((field, '=', value))
                    search_data[field] = value

                elif 'selection_' in value:
                    domain.append((field, '=', value.split('selection_')[1]))
                    search_data[field] = value.split('selection_')[1]
                else:
                    if not 'm2o_' in value:
                        operator = 'ilike'
                        if '/' in value:
                            value, operator = value.split('/')
                            value = int(value)
                        domain.append((field, operator, value))
                        search_data[field] = value
                    else:
                        search_data[field] = value.split('m2o_')[1]

        def get_domain(x):
            if len(x) == 1:
                if isinstance(x[0], (int, list)):
                    return ustr(x[0])
                return x[0]

            elif len(x) == 4:
                if isinstance(x[3], (int, list)):
                    tuple_val = x[1], x[2], ustr(x[3])
                else:
                    tuple_val = x[1], x[2], x[3]
                return [x[0], tuple_val]

            else:
                if isinstance(x[2], (int, list)) and x[1] != 'in':
                    tuple_val = x[0], x[1], ustr(x[2])
                else:
                    tuple_val = x[0], x[1], x[2]
                return [tuple_val]

        cust_domain = []
        if custom_domains:
            custom_domains = eval(custom_domains)
            for val in custom_domains[:-1]:
                if val:
                    val.insert(0, '|')

            for cs_dom in custom_domains:
                for inner in cs_dom:
                    if len(inner) == 1 and len([x for x in inner if isinstance(x, list)]) == 0:
                        cust_domain += inner[0]
                    elif len([x for x in inner if isinstance(x, list)]) and not 'in' in inner:
                        for d in inner:
                            cust_domain += get_domain(d)
                    else:
                        cust_domain += get_domain(inner)

            if len(cust_domain)>1 and cust_domain[-2] in ['&','|']:
                if len(cust_domain) == 2:
                    cust_domain = [cust_domain[1]]
                else:
                    cust_domain = cust_domain[:-2] + cust_domain[-1:]

        if selection_domain and selection_domain not in ['blk', 'sf', 'mf']:
            selection_domain = expr_eval(selection_domain)
            if selection_domain:
                domain.extend(selection_domain)

        if not domain:
            domain = None
        if not isinstance(group_by_ctx, list):
            group_by_ctx = [group_by_ctx]
        if group_by_ctx:
            search_data['group_by_ctx'] = group_by_ctx
        return dict(domain=ustr(domain), context=ustr(ctx), search_data=ustr(search_data), filter_domain=ustr(cust_domain))

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
        return dict(name=rpc.name_get(model, id))

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
