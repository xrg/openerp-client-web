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
from openerp.utils import rpc, expr_eval, TinyDict, TinyForm, TinyFormError

import actions
from form import Form
from error_page import _ep
from openobject.tools import expose, ast


class Search(Form):

    _cp_path = "/openerp/search"

    @expose(template="templates/search.mako")
    def create(self, params, tg_errors=None):

        params.view_mode = ['tree', 'form']
        params.view_type = 'tree'

        params.offset = params.offset or 0
        params.limit = params.limit or 20
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
        params.limit = params.limit or 20
        ctx = rpc.session.context.copy()
        ctx.update(params.context or {})
        params.ids = []
        proxy = rpc.RPCProxy(model)
        ids = proxy.name_search(text or '', params.domain or [], 'ilike', ctx)
        if ids:
            params.ids = [id[0] for id in ids]
            if len(ids) < params.limit:
                count = len(ids)
            else:
                count = proxy.search_count(params.domain, ctx)
            params.count = count
        
        if kw and kw.get('return_to'):
            params['return_to'] = ast.literal_eval(kw['return_to'])
        return self.create(params)

    @expose('json')
    def eval_domain_and_context(self, **kw):
        params, data = TinyDict.split(kw)

        domain = kw.get('_terp_domain', [])
        context = params.context or {}

        parent_context = params.parent_context or {}
        parent_context.update(rpc.session.context.copy())
        if 'group_by' in parent_context.keys():
            if isinstance(params.group_by, str):
                parent_context['group_by'] = [params.group_by]
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
                if val==None:
                    context[key] = False
                    
        if isinstance(context, dict):
            context = expr_eval(context, ctx)

        ctx2 = parent_context
        parent_context.update(context)
        if not isinstance(params.group_by, list):
            params.group_by = [params.group_by]
        
        return dict(domain=ustr(domain), context=ustr(parent_context), group_by = ustr(params.group_by))

    @expose('json')
    def get(self, **kw):

        params, data = TinyDict.split(kw)

        model = params.model
        context = rpc.session.context

        record = kw.get('record')
        record = eval(record)

        proxy = rpc.RPCProxy(model)
        data = {}

        frm = {}
        error = ''
        values = {}

        for key, val in record.items():
            id = key
            for field in val:
                fld = {}
                datas = {}
                res = proxy.fields_get(field)

                fld['value'] = val[field]
                fld['type'] = res[field].get('type')

                data[field] = fld
                try:
                    frm = TinyForm(**data).to_python()
                except Exception, e:
                    error = ustr(e)
                    error_field = ustr(e.field)
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

        return dict(frm=values, error=error)

    @expose('json')
    def eval_domain_filter(self, **kw):
        
        all_domains = kw.get('all_domains')
        custom_domains = kw.get('custom_domain')
        model = kw.get('model')
        
        all_domains = eval(all_domains)

        domains = all_domains.get('domains')
        selection_domain = all_domains.get('selection_domain')
        search_context = all_domains.get('search_context')
        group_by_ctx = kw.get('group_by_ctx', [])
        if domains:
            domains = eval(domains)

        c = search_context.get('context', {})
        v = search_context.get('value')
        ctx = expr_eval(c, {'self':v})

        context = rpc.session.context
        if ctx:
            ctx.update(context)

        domain = []
        check_domain = []
        check_domain = all_domains.get('check_domain')

        if check_domain and isinstance(check_domain, basestring):
            domain = expr_eval(check_domain, context)

        if domain == None:
            domain = []

        search_data = {}
        if domains:
            for key in domains:
                if '/' in key:
                    check = key.split('/')
                    if check[1] == 'from':
                        domain += [(check[0], '>=', domains[key])]
                        if check[0] in search_data.keys():
                            search_data[check[0]]['from'] = domains[key]
                        else:
                            search_data[check[0]] = {'from': domains[key]}

                    if check[1] == 'to':
                        domain += [(check[0], '<=', domains[key])]
                        if check[0] in search_data.keys():
                            search_data[check[0]]['to'] = domains[key]
                        else:
                            search_data[check[0]] = {'to': domains[key]}

                if isinstance(domains[key], bool) and domains[key]:
                    domains[key] = int(domains[key])
                    search_data[key] = domains[key]

                elif isinstance(domains[key], int) and not isinstance(domains[key], bool):
                    domain += [(key, '=', domains[key])]
                    search_data[key] = domains[key]
                else:
                    domain += [(key, 'ilike', domains[key])]
                    search_data[key] = domains[key]

        inner_domain = []
        if custom_domains:
            tmp_domain = ''

            custom_domains = eval(custom_domains)
            for inner in custom_domains:
                if len(inner) == 4:
                    if isinstance(inner[3], (int, list)):
                        tmp_domain += '[\'' + inner[0] + '\', (\'' + inner[1] + '\', \'' + inner[2] + '\', ' + ustr(inner[3]) + ')]'
                    else:
                        tmp_domain += '[\'' + inner[0] + '\', (\'' + inner[1] + '\', \'' + inner[2] + '\', \'' + inner[3] + '\')]'
                elif len(inner) == 3:
                    if isinstance(inner[2], (int, list)):
                        tmp_domain += '[(\'' + inner[0] + '\', \'' + inner[1] + '\', ' + ustr(inner[2]) + ')]'
                    else:
                        tmp_domain += '[(\'' + inner[0] + '\', \'' + inner[1] + '\', \'' + inner[2] + '\')]'

            if tmp_domain :
                cust_domain = tmp_domain.replace('][', ', ')
                inner_domain += eval(cust_domain)

                if len(inner_domain)>1 and inner_domain[-2] in ['&','|']:
                    if len(inner_domain) == 2:
                        inner_domain = [inner_domain[1]]
                    else:
                        inner_domain = inner_domain[:-2] + inner_domain[-1:]

        if selection_domain:
            if selection_domain in ['blk', 'sf', 'mf']:
                if selection_domain == 'blk':
                    selection_domain = []
                
            else:
                selection_domain = expr_eval(selection_domain)
                if selection_domain:
                    domain += selection_domain

        if not domain:
            domain = None
        if not isinstance(group_by_ctx, list):
            group_by_ctx = [group_by_ctx]
        if group_by_ctx:
            search_data['group_by_ctx'] = group_by_ctx
        return dict(domain=ustr(domain), context=ustr(ctx), search_data=ustr(search_data), filter_domain=ustr(inner_domain))

    @expose()
    def manage_filter(self, **kw):
        act={'name':'Manage Filters',
                 'res_model':'ir.filters',
                 'type':'ir.actions.act_window',
                 'view_type':'form',
                 'view_mode':'tree,form',
                 'domain':'[(\'model_id\',\'=\',\''+kw.get('model')+'\'),(\'user_id\',\'=\',(\''+str(rpc.session.uid)+'\',))]'}

        return actions.execute(act, context=rpc.session.context)

    @expose(template="templates/save_filter.mako")
    def save_filter(self, **kw):
        model = kw.get('model')
        domain = kw.get('domain')
        flag = kw.get('flag')
        group_by = kw.get('group_by',None)
        return dict(model=model, domain=domain, flag=flag, group_by=group_by)

    @expose()
    def do_filter_sc(self, **kw):

        name = kw.get('sc_name')
        model = kw.get('model')
        domain = kw.get('domain')
        flag = kw.get('flag')        

        if name:
            datas={'name':name,
                   'model_id':model,
                   'domain':domain,
                   'context':str({}),
                   'user_id':rpc.session.uid
                   }
            action_id = rpc.session.execute('object', 'execute', 'ir.filters', 'create', datas, rpc.session.context)
        return 

    @expose('json')
    def ok(self, **kw):
        params, data = TinyDict.split(kw)

        ids = [int(id) for id in data.get('search_list', [])]
        return dict(ids=ids)

    @expose('json')
    def get_name(self, model, id):
        return dict(name=rpc.name_get(model, id))

    @expose('json')
    def get_matched(self, model, text, **kw):
        params, data = TinyDict.split(kw)
        limit = kw.get('limit', 10)

        domain = params.domain or []
        context = params.context or {}

        ctx = rpc.session.context.copy()
        ctx.update(context)

        error = None
        values = False
        try:
            proxy = rpc.RPCProxy(model)
            values = proxy.name_search(text, domain, 'ilike', ctx, int(limit))
        except Exception, e:
            error=ustr(e)

        return dict(values=values, error= error)


# vim: ts=4 sts=4 sw=4 si et
