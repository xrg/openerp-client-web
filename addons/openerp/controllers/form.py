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
import base64
import re

import cherrypy
from openerp import utils, widgets as tw, validators
from openerp.controllers import SecuredController
from openerp.utils import rpc, common, TinyDict, TinyForm
from openerp.widgets.form import generate_url_for_picture
from error_page import _ep
from openobject.tools import expose, redirect, validate, error_handler, exception_handler
import openobject

def make_domain(name, value, kind='char'):
    """A helper function to generate domain for the given name, value pair.
    Will be used for search window...
    """

    if isinstance(value, int) and not isinstance(value, bool):
        return [(name, '=', value)]

    if isinstance(value, dict):

        start = value.get('from')
        end = value.get('to')

        if start and end:
            return [(name, '>=', start), (name, '<=', end)]

        elif start:
            return [(name, '>=', start)]

        elif end:
            return [(name, '<=', end)]

        return None

    if kind == "selection" and value:
        return [(name, '=', value)]

    if isinstance(value, basestring) and value:
        return [(name, 'ilike', value)]

    if isinstance(value, bool) and value:
        return [(name, '=', 1)]

    return []

def search(model, offset=0, limit=50, domain=[], context={}, data={}):
    """A helper function to search for data by given criteria.

    @param model: the resource on which to make search
    @param offset: offset from when to start search
    @param limit: limit of the search result
    @param domain: the domain (search criteria)
    @param context: the context
    @param data: the form data

    @returns dict with list of ids count of records etc.
    """

    domain = domain or []
    context = context or {}
    data = data or {}

    proxy = rpc.RPCProxy(model)
    fields = proxy.fields_get([], {})

    search_domain = domain[:]
    search_data = {}

    for k, v in data.items():
        t = fields.get(k, {}).get('type', 'char')
        t = make_domain(k, v, t)

        if t:
            search_domain += t
            search_data[k] = v

    l = limit
    o = offset

    if l < 1: l = 50
    if o < 0: o = 0

    ctx = rpc.session.context.copy()
    ctx.update(context)

    ids = proxy.search(search_domain, o, l, 0, ctx)
    if len(ids) < l:
        count = len(ids)
    else:
        count = proxy.search_count(search_domain, ctx)

    if isinstance(ids, list):
        count = len(ids)

    return dict(model=model, ids=ids, count=count, offset=o, limit=l,
                search_domain=search_domain, search_data=search_data)

def get_validation_schema(self):
    """Generate validation schema for the given Form instance. Should be used
    to validate form inputs with @validate decorator.

    @param self: and instance of Form

    @returns a new instance of Form with validation schema
    """

    kw = cherrypy.request.params
    params, data = TinyDict.split(kw)

    # bypass validations, if saving from button in non-editable view
    if params.button and not params.editable and params.id:
        return None

    cherrypy.request.terp_validators = {}
    cherrypy.request.terp_data = data

    params.nodefault = True

    form = self.create_form(params)
    cherrypy.request.terp_form = form

    vals = cherrypy.request.terp_validators
    keys = vals.keys()
    for k in keys:
        if k not in kw:
            vals.pop(k)

    form.validator = openobject.validators.Schema(**vals)
    return form

def default_error_handler(self, tg_errors=None, **kw):
    """ Error handler for the given Form instance.

    @param self: an instance for Form
    @param tg_errors: errors
    """
    params, data = TinyDict.split(kw)
    return self.create(params, tg_errors=tg_errors)

def default_exception_handler(self, tg_exceptions=None, **kw):
    """ Exception handler for the given Form instance.

    @param self: an instance for Form
    @param tg_exceptions: exception
    """
    # let _cp_on_error handle the exception
    raise tg_exceptions

class Form(SecuredController):

    _cp_path = "/openerp/form"

    def create_form(self, params, tg_errors=None):
        if tg_errors:
            return cherrypy.request.terp_form

        cherrypy.session['params'] = params

        params.offset = params.offset or 0
        params.limit = params.limit or 50
        params.count = params.count or 0
        params.view_type = params.view_type or params.view_mode[0]

        return tw.form_view.ViewForm(params, name="view_form", action="/openerp/form/save")

    @expose(template="/openerp/controllers/templates/form.mako")
    def create(self, params, tg_errors=None):

        params.view_type = params.view_type or params.view_mode[0]

        if params.view_type == 'tree':
            params.editable = True
        form = self.create_form(params, tg_errors)

        if not tg_errors:
            try:
                cherrypy.session.pop('remember_notebooks')
            except:
                self.reset_notebooks()

        editable = form.screen.editable
        mode = form.screen.view_type
        id = form.screen.id
        buttons = TinyDict()    # toolbar
        buttons.new = (not editable or mode == 'tree') and mode != 'diagram'
        buttons.edit = not editable and (mode == 'form' or mode == 'diagram')
        buttons.save = editable and mode == 'form'
        buttons.cancel = editable and mode == 'form'
        buttons.delete = not editable and mode == 'form'
        buttons.pager =  mode == 'form' or mode == 'diagram'# Pager will visible in edit and non-edit mode in form view.
        buttons.can_attach = id and mode == 'form'
        buttons.i18n = not editable and mode == 'form'
        buttons.show_grid = mode == 'diagram'
        buttons.create_node = mode == 'diagram' and editable

        from openerp.widgets import get_registered_views
        buttons.views = []

        for kind, view in get_registered_views():
            buttons.views.append(dict(kind=kind, name=view.name, desc=view.desc))

        target = getattr(cherrypy.request, '_terp_view_target', None)
        buttons.toolbar = (target != 'new' and not form.is_dashboard) or mode == 'diagram'
        pager = None
        if buttons.pager:
            pager = tw.pager.Pager(id=form.screen.id, ids=form.screen.ids, offset=form.screen.offset,
                                   limit=form.screen.limit, count=form.screen.count, view_type=params.view_type)

        can_shortcut = self.can_shortcut_create()
        shortcut_ids = []

        if cherrypy.session.get('terp_shortcuts'):
            for sc in cherrypy.session['terp_shortcuts']:
                if isinstance(sc['res_id'], tuple):
                    shortcut_ids.append(sc['res_id'][0])
                else:
                    shortcut_ids.append(sc['res_id'])        
        
        title = form.screen.string or ''
        display_name = {}
        if params.view_type == 'form':
            if params.id:
                if form.screen.view.get('fields') and form.screen.view['fields'].get('name'):
                    display_name = {'field': form.screen.view['fields']['name']['string'], 'value': ustr(form.screen.view['fields']['name']['value'])}
                    title= ustr(display_name['field']) + ':' + ustr(display_name['value'])
        elif params.view_type == 'diagram':
            display_name = {'field': form.screen.view['fields']['name']['string'], 'value': rpc.RPCProxy(params.model).name_get(form.screen.id)[0][1]}

        # For Corporate Intelligence visibility.
        obj_process = rpc.RPCProxy('ir.model').search([('model', '=', 'process.process')]) or None
        
        tips = params.display_menu_tip
        if params.view_type == params.view_mode[0] and tips:
            tips = tips

        return dict(form=form, pager=pager, buttons=buttons, path=self.path, can_shortcut=can_shortcut, shortcut_ids=shortcut_ids, display_name=display_name, title=title, tips=tips, obj_process=obj_process)

    @expose('json', methods=('POST',))
    def close_or_disable_tips(self):
        rpc.RPCProxy('res.users').write(rpc.session.uid,{'menu_tips':False}, rpc.session.context)

    def _read_form(self, context, count, domain, filter_domain, id, ids, kw,
                   limit, model, offset, search_data, search_domain, source,
                   view_ids, view_mode, view_type, notebook_tab, editable=False):
        """ Extract parameters for form reading/creation common to both
        self.edit and self.view
        """
        params, data = TinyDict.split({'_terp_model': model,
                                       '_terp_id' : id,
                                       '_terp_ids' : ids,
                                       '_terp_view_ids' : view_ids,
                                       '_terp_view_mode' : view_mode,
                                       '_terp_view_type' : view_type,
                                       '_terp_source' : source,
                                       '_terp_domain' : domain,
                                       '_terp_context' : context,
                                       '_terp_offset': offset,
                                       '_terp_limit': limit,
                                       '_terp_count': count,
                                       '_terp_search_domain': search_domain,
                                       '_terp_search_data': search_data,
                                       '_terp_filter_domain': filter_domain,
                                       '_terp_notebook_tab': notebook_tab})

        params.editable = editable

        if kw.get('default_date'):
            params.context.update({'default_date' : kw['default_date']})

        cherrypy.request._terp_view_target = kw.get('target')

        if params.view_mode and 'form' not in params.view_mode:
            params.view_type = params.view_mode[-1]

        if params.view_type == 'tree':
            params.view_type = 'form'

        if not params.ids:
            params.offset = 0

        return params

    @expose()
    def edit(self, model, id=False, ids=None, view_ids=None,
             view_mode=['form', 'tree'], view_type='form', source=None, domain=[], context={},
             offset=0, limit=50, count=0, search_domain=None,
             search_data=None, filter_domain=None, **kw):

        notebook_tab = kw.get('notebook_tab') or 0
        params = self._read_form(context, count, domain, filter_domain, id,
                                 ids, kw, limit, model, offset, search_data,
                                 search_domain, source, view_ids, view_mode,
                                 view_type, notebook_tab, editable=True)

        if not params.ids:
            params.count = 0

        # On New O2M
        if params.source:
            current = TinyDict()
            current.id = False
            params[params.source] = current

        return self.create(params)

    @expose()
    def view(self, model, id, ids=None, view_ids=None,
             view_mode=['form', 'tree'], view_type=None, source=None, domain=[], context={},
             offset=0, limit=50, count=0, search_domain=None,
             search_data=None, filter_domain=None, **kw):

        notebook_tab = kw.get('notebook_tab') or 0
        params = self._read_form(context, count, domain, filter_domain, id,
                                 ids, kw, limit, model, offset, search_data,
                                 search_domain, source, view_ids, view_mode,
                                 view_type, notebook_tab)

        if not params.ids:
            params.count = 1

        return self.create(params)

    @expose()
    def cancel(self, **kw):
        params, data = TinyDict.split(kw)

        if params.button:
            res = self.button_action(params)
            if res:
                return res
            raise redirect('/')

        if not params.id and params.ids:
            params.id = params.ids[0]

        if params.id and params.editable:
            raise redirect(self.path + "/view", model=params.model,
                                               id=params.id,
                                               ids=ustr(params.ids),
                                               view_ids=ustr(params.view_ids),
                                               view_mode=ustr(params.view_mode),
                                               domain=ustr(params.domain),
                                               context=ustr(params.context),
                                               offset=params.offset,
                                               limit=params.limit,
                                               count=params.count,
                                               search_domain=ustr(params.search_domain),
                                               search_data = ustr(params.search_data),
                                               filter_domain= ustr(params.filter_domain))

        params.view_type = 'tree'
        return self.create(params)

    @expose(methods=('POST',))
    @validate(form=get_validation_schema)
    @error_handler(default_error_handler)
    @exception_handler(default_exception_handler)
    def save(self, terp_save_only=False, **kw):
        """Controller method to save/button actions...

        @param tg_errors: TG special arg, used durring validation
        @param kw: keyword arguments

        @return: form view
        """
        params, data = TinyDict.split(kw)
        # remember the current page (tab) of notebooks
        cherrypy.session['remember_notebooks'] = True

        Model = rpc.RPCProxy(params.model)
        if params.id:
            ctx = utils.context_with_concurrency_info(params.context, params.concurrency_info)
            Model.write([params.id], data, ctx)
        else:
            if params.default_o2m:
                data.update(params.default_o2m)

            ctx = dict((params.context or {}), **rpc.session.context)
            params.id = int(Model.create(data, ctx))
            params.ids = (params.ids or []) + [params.id]
            params.count += 1
        tw.ConcurrencyInfo.update(
            params.model, Model.read([params.id], ['__last_update'], ctx)
        )

        button = params.button

        # perform button action
        if params.button:
            res = self.button_action(params)
            if res:
                return res

        current = params.chain_get(params.source or '')
        if current:
            current.id = None
        elif not button:
            params.editable = False

        if terp_save_only:
            return dict(params=params, data=data)

        def get_params(p, f):

            pp = p.chain_get(f)
            px = rpc.RPCProxy(p.model)

            _ids = pp.ids
            _all = px.read([p.id], [f])[0][f]
            _new = [i for i in _all if i not in _ids]

            pp.ids = _all
            if _new:
                pp.id = _new[0]

            return pp

        if params.source and len(params.source.split("/")) > 1:

            path = params.source.split("/")
            p = params
            for f in path:
                p = get_params(p, f)

            return self.create(params)

        args = {'model': params.model,
                'id': params.id,
                'ids': ustr(params.ids),
                'view_ids': ustr(params.view_ids),
                'view_mode': ustr(params.view_mode),
                'domain': ustr(params.domain),
                'context': ustr(params.context),
                'offset': params.offset,
                'limit': params.limit,
                'count': params.count,
                'search_domain': ustr(params.search_domain),
                'search_data': ustr(params.search_data),
                'filter_domain': ustr(params.filter_domain),
                'notebook_tab': params.notebook_tab}

        if params.editable or params.source or params.return_edit:
            raise redirect(self.path + '/edit', source=params.source, **args)
        raise redirect(self.path + '/view', **args)

    def button_action_cancel(self, name, params):
        if name:
            params.button.btype = "object"
            params.id = False
            res = self.button_action(params)
            if res:
                return res

        import actions
        return actions.close_popup()
    def button_action_save(self, _, params):
        params.id = False
        params.button = None

    def button_action_workflow(self, name, params):
        model, id, _, _ = self._get_button_infos(params)
        res = rpc.session.execute('object', 'exec_workflow', model, name, id)
        if isinstance(res, dict):
            import actions
            return actions.execute(res, ids=[id])
        params.button = None

    def button_action_object(self, name, params):
        model, id, ids, ctx = self._get_button_infos(params)

        res = rpc.session.execute('object', 'execute', model, name, ids, ctx)

        if isinstance(res, dict):
            import actions
            return actions.execute(res, ids=[id])
        params.button = None

    def button_action_action(self, name, params):
        model, id, ids, ctx = self._get_button_infos(params)
        import actions

        action_id = int(name)
        action_type = actions.get_action_type(action_id)

        if action_type == 'ir.actions.wizard':
            cherrypy.session['wizard_parent_form'] = self.path
            cherrypy.session['wizard_parent_params'] = params.parent_params or params

        res = actions.execute_by_id(
                action_id, type=action_type,
                model=model, id=id, ids=ids,
                context=ctx or {})
        if res:
            return res
        params.button = None

    BUTTON_ACTIONS_BY_BTYPE = {
        'action': button_action_action,
        'cancel': button_action_cancel,
        'object': button_action_object,
        'save': button_action_save,
        'workflow': button_action_workflow,
    }

    def _get_button_infos(self, params):
        model = params.button.model
        id = params.button.id or params.id
        id = (id or False) and (id)
        ids = (id or []) and [id]
        ctx = dict((params.context or {}), **rpc.session.context)
        ctx.update(params.button.context or {})
        return model, id, ids, ctx

    def button_action(self, params):
        button_name = openobject.ustr(params.button.name)
        button_name = button_name.rsplit('/', 1)[-1]

        btype = params.button.btype
        try:
            return self.BUTTON_ACTIONS_BY_BTYPE[btype](self, button_name, params)
        except KeyError:
            raise common.warning(_('Invalid button type "%s"') % btype)

    @expose()
    def duplicate(self, **kw):
        params, data = TinyDict.split(kw)

        id = params.id
        ctx = params.context
        model = params.model

        proxy = rpc.RPCProxy(model)
        new_id = proxy.copy(id, {}, ctx)

        if new_id:
            params.id = new_id
            params.ids += [int(new_id)]
            params.count += 1

        args = {'model': params.model,
                'id': params.id,
                'ids': ustr(params.ids),
                'view_ids': ustr(params.view_ids),
                'view_mode': ustr(params.view_mode),
                'domain': ustr(params.domain),
                'context': ustr(params.context),
                'offset': params.offset,
                'limit': params.limit,
                'count': params.count,
                'search_domain': ustr(params.search_domain),
                'filter_domain': ustr(params.filter_domain)}

        if new_id:
            raise redirect(self.path + '/edit', **args)

        raise redirect(self.path + '/view', **args)

    @expose()
    def delete(self, **kw):
        params, data = TinyDict.split(kw)

        current = params.chain_get(params.source or '') or params
        proxy = rpc.RPCProxy(current.model)

        idx = -1
        if current.id:
            ctx = utils.context_with_concurrency_info(current.context, params.concurrency_info)
            res = proxy.unlink([current.id], ctx)
            idx = current.ids.index(current.id)
            current.ids.remove(current.id)
            params.count = 0 # invalidate count

            if idx == len(current.ids):
                idx = -1

        current.id = (current.ids or None) and current.ids[idx]

        self.reset_notebooks()

        args = {'model': params.model,
                'id': params.id,
                'ids': ustr(params.ids),
                'view_ids': ustr(params.view_ids),
                'view_mode': ustr(params.view_mode),
                'domain': ustr(params.domain),
                'context': ustr(params.context),
                'offset': params.offset,
                'limit': params.limit,
                'count': params.count,
                'search_domain': ustr(params.search_domain),
                'filter_domain': ustr(params.filter_domain)}

        if not params.id:
            raise redirect(self.path + '/edit', **args)

        raise redirect(self.path + '/view', **args)

    @expose(content_type='application/octet-stream')
    def save_binary_data(self, _fname='file.dat', **kw):
        params, data = TinyDict.split(kw)

        cherrypy.response.headers['Content-Disposition'] = 'attachment; filename="%s"' % _fname

        if params.datas:
            form = params.datas['form']
            res = form.get(params.field)
            return base64.decodestring(res)
        
        elif params.id:
            proxy = rpc.RPCProxy(params.model)
            res = proxy.read([params.id],[params.field], rpc.session.context)
            return base64.decodestring(res[0][params.field])
        else:
            return base64.decodestring(data[params.field])
        

    @expose()
    def clear_binary_data(self, **kw):
        params, data = TinyDict.split(kw)

        proxy = rpc.RPCProxy(params.model)
        ctx = utils.context_with_concurrency_info(params.context, params.concurrency_info)

        if params.fname:
            proxy.write([params.id], {params.field: False, params.fname: False}, ctx)
        else:
            proxy.write([params.id], {params.field: False}, ctx)

        args = {'model': params.model,
                'id': params.id,
                'ids': ustr(params.ids),
                'view_ids': ustr(params.view_ids),
                'view_mode': ustr(params.view_mode),
                'domain': ustr(params.domain),
                'context': ustr(params.context),
                'offset': params.offset,
                'limit': params.limit,
                'count': params.count,
                'search_domain': ustr(params.search_domain),
                'filter_domain': ustr(params.filter_domain)}

        raise redirect(self.path + '/edit', **args)

    @expose()
    @validate(form=get_validation_schema)
    @error_handler(default_error_handler)
    @exception_handler(default_exception_handler)
    def filter(self, **kw):
        params, data = TinyDict.split(kw)
        if params.get('_terp_save_current_id'):
            ctx = dict((params.context or {}), **rpc.session.context)
            if params.id:
                rpc.RPCProxy(params.model).write([params.id], data, ctx)
            else:
                id = rpc.RPCProxy(params.model).create(data, ctx)
                params.ids.append(id)
                params.count += 1
            
        l = params.limit or 50
        o = params.offset or 0
        c = params.count or 0

        id = params.id or False
        ids = params.ids or []
        filter_action = params.filter_action

        if ids and filter_action == 'FIRST':
            o = 0
            id = ids[0]

        if ids and filter_action == 'LAST':
            o = c - c % l
            id = ids[-1]

        if ids and filter_action == 'PREV':
            if id == ids[0]:
                o -= l
            elif id in ids:
                id = ids[ids.index(id)-1]

        if ids and filter_action == 'NEXT':
            if id == ids[-1]:
                o += l
            elif id in ids:
                id = ids[ids.index(id)+1]
            elif id is False:
                o = 0
                id = ids[0]

        if filter_action:
            # remember the current page (tab) of notebooks
            cherrypy.session['remember_notebooks'] = True

        if params.offset != o:

            domain = params.domain
            if params.search_domain is not None:
                domain = params.search_domain
                data = params.search_data

            ctx = params.context or {}
            ctx.update(rpc.session.context.copy())
            res = search(params.model, o, l, domain=domain, context=ctx, data=data)

            o = res['offset']
            l = res['limit']
            if not c: c = res['count']

            params.search_domain = res['search_domain']
            params.search_data = res['search_data']

            ids = res['ids']
            id = False

            if ids and filter_action in ('FIRST', 'NEXT'):
                id = ids[0]

            if ids and filter_action in ('LAST', 'PREV'):
                id = ids[-1]

        params.id = id
        params.ids = ids
        params.offset = o
        params.limit = l
        params.count = c

        return self.create(params)

    @expose()
    def find(self, **kw):
        kw['_terp_offset'] = None
        kw['_terp_limit'] = None

        kw['_terp_search_domain'] = None
        kw['_terp_search_data'] = None
        kw['_terp_filter_action'] = 'FIND'

        return self.filter(**kw)

    @expose()
    def first(self, **kw):
        kw['_terp_filter_action'] = 'FIRST'
        return self.filter(**kw)

    @expose()
    def last(self, **kw):
        kw['_terp_filter_action'] = 'LAST'
        return self.filter(**kw)

    @expose()
    def previous(self, **kw):
        if '_terp_source' in kw:
            return self.previous_o2m(**kw)

        kw['_terp_filter_action'] = 'PREV'
        return self.filter(**kw)

    @expose()
    def next(self, **kw):
        if '_terp_source' in kw:
            return self.next_o2m(**kw)

        kw['_terp_filter_action'] = 'NEXT'
        return self.filter(**kw)

    @expose()
    @validate(form=get_validation_schema)
    @error_handler(default_error_handler)
    @exception_handler(default_exception_handler)
    def previous_o2m(self, **kw):
        params, data = TinyDict.split(kw)
        
        if params.get('_terp_save_current_id'):
            ctx = dict((params.context or {}), **rpc.session.context)
            if params.id:
                rpc.RPCProxy(params.model).write([params.id], data, ctx)
            else:
                id = rpc.RPCProxy(params.model).create(data, ctx)
                params.ids.append(id)
                params.count += 1
        
        current = params.chain_get(params.source or '') or params
        idx = -1
        
        if current.id:
            # save current record
            if params.editable:
                self.save(terp_save_only=True, **kw)

            idx = current.ids.index(current.id)
            idx = idx-1

            if idx == len(current.ids):
                idx = len(current.ids) -1

        if current.ids:
            current.id = current.ids[idx]

        return self.create(params)

    @expose()
    def next_o2m(self, **kw):
        params, data = TinyDict.split(kw)
        c = params.count or 0
        current = params.chain_get(params.source or '') or params

        idx = 0
        if current.id:

            # save current record
            if params.editable:
                self.save(terp_save_only=True, **kw)

            idx = current.ids.index(current.id)
            idx = idx + 1

            if idx == len(current.ids):
                idx = 0

        if current.ids:
            current.id = current.ids[idx]

        return self.create(params)

    @expose()
    @validate(form=get_validation_schema)
    def switch(self, **kw):
        params, data = TinyDict.split(kw)
        if params.get('_terp_save_current_id'):
            ctx = dict((params.context or {}), **rpc.session.context)
            if params.id:
                rpc.RPCProxy(params.model).write([params.id], data, ctx)
            else:
                id = rpc.RPCProxy(params.model).create(data, ctx)
                params.ids.append(id)
                params.count += 1
        # switch the view
        params.view_type = params.source_view_type
        return self.create(params)

    def do_action(self, name, adds={}, datas={}):
        params, data = TinyDict.split(datas)

        model = params.model

        id = params.id or False
        ids = params.selection or params.ids or []

        if params.view_type == 'form':
            #TODO: save current record
            ids = (id or []) and [id]

        if id and not ids:
            ids = [id]

        if len(ids):
            import actions
            return actions.execute_by_keyword(name, adds=adds, model=model, id=id, ids=ids, report_type='pdf')
        else:
            raise common.message(_("No record selected"))    
    
    @expose()
    def report(self, **kw):
        return self.do_action('client_print_multi', adds={'Print Screen': {'report_name':'printscreen.list',
                                                                           'name': _('Print Screen'),
                                                                           'type':'ir.actions.report.xml'}}, datas=kw)
    
    @expose()
    def action(self, **kw):
        params, data = TinyDict.split(kw)
        context_menu = kw.get('context_menu')

        id = params.id or False
        ids = params.selection or []

        if not ids and id:
            ids = [id]

        if not id and ids:
            id = ids[0]

        domain = params.domain or []
        context = params.context or {}
        action = {}

        if data.get('datas'):
            action = eval(data.get('datas'))
        type = action.get('type')
        act_id = params.action

        if not params.selection and not params.id:
            raise common.message(_('You must save this record to use the sidebar button'))

        if not act_id:
            return self.do_action('client_action_multi', datas=kw)

        if type is None:
            action_type = rpc.RPCProxy('ir.actions.actions').read(act_id, ['type'], rpc.session.context)['type']
            action = rpc.session.execute('object', 'execute', action_type, 'read', act_id, False, rpc.session.context)

        if domain:
            if isinstance(domain, basestring):
                domain = eval(domain)
            domain.extend(eval(action.get('domain', '[]')))
            action['domain'] = ustr(domain)

        action['context'] = context or {}

        import actions
        return actions.execute(action, model=params.model, id=id, ids=ids, report_type='pdf', context_menu=context_menu)

    @expose()
    def dashlet(self, **kw):
        params, data = TinyDict.split(kw)
        current = params.chain_get(str(params.source) or '') or params

        return self.create(current)

    @expose('json')
    def on_change(self, **kw):

        data = kw.copy()

        callback = data.pop('_terp_callback')
        caller = data.pop('_terp_caller')
        model = data.pop('_terp_model')
        context = data.pop('_terp_context')

        try:
            context = eval(context) # convert to python dict
        except:
            context = {}

        match = re.match('^(.*?)\((.*)\)$', callback)

        if not match:
            raise common.error(_('Application Error'), _('Wrong on_change trigger: %s') % callback)

        for k, v in data.items():
            try:
                data[k] = eval(v)
            except:
                pass

        result = {}

        prefix = ''
        if '/' in caller:
            prefix = caller.rsplit('/', 1)[0]

        ctx = TinyForm(**kw).to_python(safe=True)
        pctx = ctx

        if prefix:
            ctx = ctx.chain_get(prefix)

            if '/' in prefix:
                pprefix = prefix.rsplit('/', 1)[0]
                pctx = pctx.chain_get(pprefix)

        ctx2 = rpc.session.context.copy()
        ctx2.update(context or {})

        ctx['parent'] = pctx
        ctx['context'] = ctx2

        func_name = match.group(1)
        arg_names = [n.strip() for n in match.group(2).split(',')]

        ctx_dict = dict(**ctx)
        args = [utils.expr_eval(arg, ctx_dict) for arg in arg_names]

        proxy = rpc.RPCProxy(model)

        ids = ctx.id and [ctx.id] or []

        try:
            response = getattr(proxy, func_name)(ids, *args)
        except Exception, e:
             return dict(error=_ep.render())

        if response is False: # response is False when creating new record for inherited view.
            response = {}

        if 'value' not in response:
            response['value'] = {}

        result.update(response)

        # apply validators (transform values from python)
        values = result['value']
        values2 = {}
        for k, v in values.items():
            key = ((prefix or '') and prefix + '/') + k

            kind = data.get(key, {}).get('type', '')

            if key in data and key != 'id':
                values2[k] = data[key]
                values2[k]['value'] = v
            else:
                values2[k] = {'value': v}

            if kind == 'float':
                field = proxy.fields_get([k], ctx2)
                digit = field[k].get('digits')
                if digit: digit = digit[1]
                values2[k]['digit'] = digit or 2

        values = TinyForm(**values2).from_python().make_plain()

        # get name of m2o and reference fields
        for k, v in values2.items():
            kind = v.get('type')
            relation = v.get('relation')

            if relation and kind in ('many2one', 'reference') and values.get(k):
                values[k] = [values[k], rpc.name_get(relation, values[k])]

            if kind == 'picture':
                values[k] = generate_url_for_picture(model, k, ctx.id, values[k])

        result['value'] = values

        # convert domains in string to prevent them being converted in JSON
        if 'domain' in result:
            for k in result['domain']:
                result['domain'][k] = ustr(result['domain'][k])

        return result

    @expose('json')
    def get_context_menu(self, model, field, kind="char", relation=None, value=None):

        defaults = []
        actions = []
        relates = []

        defaults = [{'text': 'Set to default value', 'action': "set_to_default('%s', '%s')" % (field, model)},
                    {'text': 'Set as default', 'action': "set_as_default('%s', '%s')"  % (field, model)}]

        if kind=='many2one':

            act = (value or None) and "javascript: void(0)"

            actions = [{'text': 'Action', 'relation': relation, 'field': field, 'action': act and "do_action(this, true)"},
                       {'text': 'Report', 'action': act and "do_report('%s', '%s')" %(field, relation)}]
            
            res = rpc.RPCProxy('ir.values').get('action', 'client_action_relate', [(relation, False)], False, rpc.session.context)
            res = [x[2] for x in res]

            for x in res:
                act = (value or None) and "javascript: void(0)"
                x['string'] = x['name']
                relates += [{'text': '... '+x['name'],
                             'action_id': x['id'],
                             'field': field,
                             'relation': relation,
                             'action': act and "do_action(this, true)",
                             'domain': x.get('domain', []),
                             'context': x.get('context', {})}]

        return dict(defaults=defaults, actions=actions, relates=relates)

    @expose('json')
    def get_default_value(self, model, field):

        field = field.split('/')[-1]

        res = rpc.RPCProxy(model).default_get([field])
        value = res.get(field)

        return dict(value=value)

    def reset_notebooks(self):
        for name in cherrypy.request.cookie.keys():
            if name.startswith('_notebook_'):
                cherrypy.response.cookie[name] = 0

    @expose('json')
    def change_default_get(self, **kw):
        params, data = TinyDict.split(kw)

        ctx = rpc.session.context.copy()
        ctx.update(params.context or {})

        model = params.model
        field = params.caller.split('/')[-1]
        value = params.value or False

        proxy = rpc.RPCProxy('ir.values')
        values = proxy.get('default', '%s=%s' % (field, value), [(model, False)], False, ctx)

        data = {}
        for index, fname, value in values:
            data[fname] = value

        return dict(values=data)

    # Possible to create shortcut for particular object or not.
    def can_shortcut_create(self):
        return (rpc.session.is_logged() and
                rpc.session.active_id and
                (cherrypy.request.path_info == '/openerp/tree/open' and cherrypy.request.params.get('model') == 'ir.ui.menu')
                or
                (cherrypy.request.path_info == '/openerp/form/switch')
        )

    @expose()
    def action_submenu(self, **kw):
        params, data = TinyDict.split(kw)

        import actions

        act_id = rpc.session.execute('object', 'execute', 'ir.model.data', 'search', [('name','=', params.action_id)])
        res_model = rpc.session.execute('object', 'execute', 'ir.model.data', 'read', act_id, ['res_id'])

        res = rpc.session.execute('object', 'execute', 'ir.actions.act_window', 'read', res_model[0]['res_id'], False)

        if res:
            return actions.execute(res, model=params.model, id=params.id, context=rpc.session.context.copy())

# vim: ts=4 sts=4 sw=4 si et

