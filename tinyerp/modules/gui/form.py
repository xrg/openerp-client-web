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

import re

from turbogears import expose
from turbogears import widgets
from turbogears import controllers
from turbogears import validators
from turbogears import validate
from turbogears import error_handler

import cherrypy

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp import widgets as tw
from tinyerp.tinyres import TinyResource

from tinyerp.modules.utils import TinyDict
from tinyerp.modules.utils import TinyParent

import search

class Form(controllers.Controller, TinyResource):

    @expose(template="tinyerp.modules.gui.templates.form")
    def create(self, params, tg_errors=None):
        if tg_errors:
            form = cherrypy.request.terp_form
            
        elif params.view_mode[0] == 'tree': # use search view instead of list view
            params.found_ids = []
            return search.Search().create(params)
        
        else:
            form = tw.form_view.ViewForm(params, name="view_form", action="/form/save")

        if cherrypy.request.path.startswith('/tree/open'):
            self.del_notebook_cookies()

        return dict(form=form)

    @expose()
    def new(self, **kw):
        params, data = TinyDict.split(kw)

        if params.id or params.ids:
            params.id = None

        if params.view_mode[0] == 'tree':
            params.view_mode.reverse()

        if params.view_mode[0] != 'form':
            params.view_mode = ['form', 'tree']

        self.del_notebook_cookies()
        return self.create(params)

    @expose()
    def edit(self, **kw):            
        params, data = TinyDict.split(kw)

        current = params[params.source or ''] or params
        current.editable = True
        
        if params.inline is None and ('model' in data and 'id' in data):
            current.view_mode = ['form', 'tree']
            current.model = data.get('model')
            current.id = data.get('id')

        if current.view_mode[0] == 'tree':
            current.view_mode.reverse()

        if current.view_mode[0] != 'form':
            current.view_mode = ['form', 'tree']

        return self.create(params)
    
    @expose()
    def view(self, model, id):
        params = TinyDict(model=model, id=id, view_mode=['form', 'tree'], editable=False)
        return self.create(params)

    def get_form(self):
        params, data = TinyDict.split(cherrypy.request.params)

        cherrypy.request.terp_validators = {}
        params.nodefault = True
        form = tw.form_view.ViewForm(params, name="view_form", action="/form/save")
        cherrypy.request.terp_form = form

        vals = cherrypy.request.terp_validators
        schema = validators.Schema(**vals)

        form.validator = schema

        return form

    @expose()
    @validate(form=get_form)
    def save(self, tg_errors=None, tg_source=None, tg_exceptions=None, **kw):
        """Controller method to save/button actions...

        @param tg_errors: TG special arg, used durring validation
        @param tg_source: TG special arg, used durring validation
        @param tg_exceptions: TG special arg, used durring validation
        @param kw: keyword arguments

        @return: form view
        """
        params, data = TinyDict.split(kw)
        if tg_errors:
            return self.create(params, tg_errors=tg_errors)

        proxy = rpc.RPCProxy(params.model)

        if not params.id:
            id = proxy.create(data, params.context)
            params.ids = (params.ids or []) + [int(id)]
        else:
            id = proxy.write([params.id], data, params.context)

        # perform button action
        if params.button:
            res = self.button_action(params)
            if res:
                return res

        current = params[params.source or '']
        if current:
            current.id = None
            if not params.id:
                params.id = int(id)

            if current.view_mode[0] == 'tree':
                current.view_mode.reverse()

            if current.view_mode[0] != 'form':
                current.view_mode = ['form', 'tree']
        return self.create(params)

    def button_action(self, params):

        button = params.button

        name = ustr(button.name)
        name = name.rsplit('/', 1)[-1]

        btype = button.btype
        model = button.model
        id = button.id

        id = (id or False) and int(id)
        ids = (id or []) and [id]

        if btype == 'workflow':
            rpc.session.execute('object', 'exec_workflow', model, name, id)

        elif btype == 'object':
            ctx = params.context or {}
            ctx.update(rpc.session.context.copy())
            rpc.session.execute('object', 'execute', model, name, ids, ctx)

        elif btype == 'action':
            from tinyerp.modules import actions
            action_id = int(name)

            res = actions.execute_by_id(action_id, model=model, id=id, ids=ids)
            if res:
                return res

        else:
            raise common.warning('Unallowed button type')

        params.pop('button')

    @expose()
    def delete(self, **kw):
        params, data = TinyDict.split(kw)

        params.is_navigating = True

        current = params[params.source or ''] or params

        proxy = rpc.RPCProxy(current.model)

        idx = -1
        if current.id:
            res = proxy.unlink([current.id])
            idx = current.ids.index(current.id)
            current.ids.remove(current.id)

            if idx == len(current.ids):
                idx = -1

        current.id = (current.ids or None) and current.ids[idx]

        self.del_notebook_cookies()
        return self.create(params)

    @expose()
    def prev(self, **kw):
        params, data = TinyDict.split(kw)
        params.is_navigating = True

        current = params[params.source or ''] or params

        idx = -1

        if current.id:
            idx = current.ids.index(current.id)
            idx = idx-1

            if idx == len(current.ids):
                idx = len(current.ids) -1

        if current.ids:
            current.id = current.ids[idx]

        return self.create(params)

    @expose()
    def next(self, **kw):
        params, data = TinyDict.split(kw)
        params.is_navigating = True

        current = params[params.source or ''] or params

        idx = 0

        if current.id:
            idx = current.ids.index(current.id)
            idx = idx + 1

            if idx == len(current.ids):
                idx = 0

        if current.ids:
            current.id = current.ids[idx]

        return self.create(params)

    @expose()
    def save_binary(self, **kw):
        model = kw.get("_terp_model")
        id = kw.get("_terp_id")
        field = kw.get("field_search")
        demo = ''

        try:
            proxy = rpc.RPCProxy(model)
            demo = proxy.read([id],[field])
            cherrypy.response.headers['Content-Type'] = "application/data"
            return demo[0]['datas']
        except Exception, e:
            return str(e)
        return dict()

    @expose()
    def clear_binary(self, **kw):
        params, data = TinyDict.split(kw)
        model = params.model
        id = params.id
        field = data.get('field_search')
        demo = ''
        try:
            proxy = rpc.RPCProxy(model)
            demo = proxy.write([int(id)],{field:False})
            return self.create(params)
        except Exception, e:
            return str(e)
        return dict()

    @expose()
    def find(self, **kw):
        params, data = TinyDict.split(kw)
        params.found_ids = []

        search_window = search.Search()
        return search_window.create(params)

    @expose()
    def switch(self, **kw):

        # get special _terp_ params and data
        params, data = TinyDict.split(kw)

        # select the right params field (if one2many toolbar button)
        current = params[params.source or ''] or params

        # switch the view mode
        current.view_mode.reverse()

        # if view_mode is different then the view_mode2 replace it with view_mode2
        if set(current.view_mode) - set(current.view_mode2):
            current.view_mode = current.view_mode2

        # set ids and id
        current.ids = current.ids or []
        if current.ids:
            current.id = current.ids[0]

        # regenerate the view
        return self.create(params)

    def do_action(self, name, adds={}, datas={}):
        params, data = TinyDict.split(datas)

        model = params.model
        view_type = params.view_mode[0]

        id = params.id or False
        ids = params.ids

        if view_type == 'form':
            #TODO: save current record
            ids = (id or []) and [id]

        if len(ids):
            from tinyerp.modules import actions
            return actions.execute_by_keyword(name, adds=adds, model=model, id=id, ids=ids, report_type='pdf')
        else:
            raise common.message("No record selected!")

    @expose()
    def report(self, **kw):
        return self.do_action('client_print_multi', adds={'Print Screen': {'report_name':'printscreen.list', 'name':'Print Screen', 'type':'ir.actions.report.xml'}}, datas=kw)

    @expose()
    def action(self, **kw):
        params, data = TinyDict.split(kw)

        action = params.data

        if not action:
            return self.do_action('client_action_multi', datas=kw)

        if not params.id:
            raise common.message('You must save this record to use the relate button !')

        from tinyerp.modules import actions
        return actions._execute(action, model=params.model, id=params.id, ids=params.ids, report_type='pdf')

    @expose()
    def dashlet(self, **kw):
        params, data = TinyDict.split(kw)
        current = params[str(params.source) or ''] or params

        return self.create(current)

    @expose('json')
    def on_change(self, **kw):
        params, data = TinyDict.split(kw)        

        caller = params.caller
        callback = params.callback
        model = params.model

        result = {}

        prefix = ''
        if '/' in caller:
            prefix = caller.rsplit('/', 1)[0]

        ctx = TinyParent(**kw)
        pctx = ctx

        if prefix:
            ctx = ctx[prefix.replace('/', '.')]

            if '/' in prefix:
                prefix = prefix.rsplit('/', 1)[0]
                pctx = pctx[prefix.replace('/', '.')]

        ctx.parent = pctx
        ctx.context = rpc.session.context.copy()

        match = re.match('^(.*?)\((.*)\)$', callback)
        if not match:
            raise common.error('Wrong on_change trigger: %s' % callback)

        func_name = match.group(1)
        arg_names = [n.strip() for n in match.group(2).split(',')]

        ctx_dict = dict(**ctx)
        args = [tools.expr_eval(arg, ctx_dict) for arg in arg_names]
                        
        proxy = rpc.RPCProxy(model)

        ids = ctx.id and [ctx.id] or []
        response = getattr(proxy, func_name)(ids, *args)

        if 'value' not in response:
            response['value'] = {}

        result.update(response)

        for k, v in result['value'].items():
            if isinstance(v, (list, tuple)):
                result['value'][k] = (v or '') and v[0]

        return result

    def del_notebook_cookies(self):
        names = cherrypy.request.simple_cookie.keys()

        for n in names:
            if n.endswith('_notebookTGTabber'):
                cherrypy.response.simple_cookie[n] = 0

