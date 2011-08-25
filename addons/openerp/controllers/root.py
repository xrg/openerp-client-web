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
import cherrypy

import openobject
from openerp.controllers import SecuredController, unsecured, actions, login as tiny_login, form, widgets
from openerp.utils import rpc, cache, TinyDict

from openobject.tools import url, expose, redirect
from openobject.tools.ast import literal_eval

_MAXIMUM_NUMBER_WELCOME_MESSAGES = 3

def _cp_on_error():
    cherrypy.request.pool = openobject.pooler.get_pool()

    errorpage = cherrypy.request.pool.get_controller("/openerp/errorpage")
    message = errorpage.render()
    cherrypy.response.status = 500
    cherrypy.response.body = [message]

cherrypy.config.update({'request.error_response': _cp_on_error})

class Root(SecuredController):

    _cp_path = "/openerp"

    @expose()
    def index(self, next=None):
        """Index page, loads the view defined by `action_id`.
        """
        if not next:
            user_action_id = rpc.RPCProxy("res.users").read([rpc.session.uid], ['action_id'], rpc.session.context)[0]['action_id']
            if user_action_id:
                next = '/openerp/home'
        
        return self.menu(next=next)

    @expose()
    def home(self):
        context = rpc.session.context
        user_action_id = rpc.RPCProxy("res.users").read([rpc.session.uid], ['action_id'], context)[0]['action_id']
        if user_action_id:
            from openerp import controllers
            return controllers.actions.execute_by_id(
                user_action_id[0], home_action=True, context=context)
        return ''

    @expose(content_type='application/octet-stream')
    def report(self, report_name=None, **kw):
        import actions
        return actions.execute_report(report_name, **TinyDict(**kw))
    
    @expose()
    def custom_action(self, action):
        menu_ids = rpc.RPCProxy('ir.ui.menu').search(
                [('id', '=', int(action))], 0, 0, 0, rpc.session.context)

        return actions.execute_by_keyword(
                'tree_but_open', model='ir.ui.menu', id=menu_ids[0], ids=menu_ids,
                context=rpc.session.context, report_type='pdf')

    @expose()
    def info(self):
        return """
    <html>
    <head></head>
    <body>
        <div align="center" style="padding: 50px;">
            <img border="0" src="%s"></img>
        </div>
    </body>
    </html>
    """ % (url("/openerp/static/images/loading.gif"))

    @expose(template="/openerp/controllers/templates/index.mako")
    def menu(self, active=None, next=None):
        from openerp.widgets import tree_view
        
        try:
            id = int(active)
        except:
            id = False
            form.Form().reset_notebooks()
        ctx = rpc.session.context.copy()
        menus = rpc.RPCProxy("ir.ui.menu")

        domain = [('parent_id', '=', False)]
        user_menu_action_id = rpc.RPCProxy("res.users").read([rpc.session.uid], ['menu_id'], ctx)[0]['menu_id']
        if user_menu_action_id:
            act = rpc.RPCProxy('ir.actions.act_window').read([user_menu_action_id[0]], ['res_model', 'domain'], ctx)[0]
            if act['res_model'] == 'ir.ui.menu' and act['domain']:
                domain = literal_eval(act['domain'])

        ids = menus.search(domain, 0, 0, 0, ctx)
        parents = menus.read(ids, ['name', 'action', 'web_icon_data', 'web_icon_hover_data'], ctx)

        for parent in parents:
            if parent['id'] == id:
                parent['active'] = 'active'
                if parent.get('action') and not next:
                    next = url('/openerp/custom_action', action=id)
            # If only the hover image exists, use it as regular image as well
            if parent['web_icon_hover_data'] and not parent['web_icon_data']:
                parent['web_icon_data'] = parent['web_icon_hover_data']

        if next or active:
            if not id and ids:
                id = ids[0] 
            ids = menus.search([('parent_id', '=', id)], 0, 0, 0, ctx)
            tools = menus.read(ids, ['name', 'action'], ctx)
            #searching id for the hierarchycal tree view of ir.ui.menu 
            view_id = rpc.RPCProxy('ir.ui.view').search([('model','=','ir.ui.menu'),('type','=','tree')],0,0,'id')[0]
            view = cache.fields_view_get('ir.ui.menu', view_id, 'tree', {})
            fields = cache.fields_get(view['model'], False, ctx)
            
            for tool in tools:
                tid = tool['id']
                tool['tree'] = tree = tree_view.ViewTree(view, 'ir.ui.menu', tid,
                                        domain=[('parent_id', '=', tid)],
                                        context=ctx, action="/openerp/tree/action", fields=fields)
                tree._name = "tree_%s" %(tid)
                tree.tree.onselection = None
                tree.tree.onheaderclick = None
                tree.tree.showheaders = 0
        else:
            # display home action
            tools = None

        return dict(parents=parents, tools=tools, load_content=(next and next or ''),
                    welcome_messages=rpc.RPCProxy('publisher_warranty.contract').get_last_user_messages(_MAXIMUM_NUMBER_WELCOME_MESSAGES),
                    show_close_btn=rpc.session.uid == 1,
                    widgets=openobject.pooler.get_pool()\
                                      .get_controller('/openerp/widgets')\
                                      .user_home_widgets(ctx))

    @expose(allow_json=True)
    @unsecured
    def login(self, db=None, user=None, password=None, style=None, location=None, message=None, **kw):
        location = url(location or '/', kw or {})

        if cherrypy.request.params.get('tg_format') == 'json':
            if rpc.session.login(db, user, password) > 0:
                return dict(result=1)
            return dict(result=0)

        if style in ('ajax', 'ajax_small'):
            return dict(db=db, user=user, password=password, location=location,
                    style=style, cp_template="/openerp/controllers/templates/login_ajax.mako")

        return tiny_login(target=location, db=db, user=user, password=password, action="login", message=message)

    @expose()
    @unsecured
    def logout(self):
        """ Logout method, will terminate the current session.
        """
        rpc.session.logout()
        raise redirect('/')

    @expose(template="/openerp/controllers/templates/about.mako")
    @unsecured
    def about(self):
        from openobject import release
        version = _("Version %s") % (release.version,)
        return dict(version=version)
    
    @expose()
    def blank(self):
        return ''
    
    @openobject.tools.expose('json', methods=('POST',))
    def remove_log(self, log_id):
        error = None
        try:
            rpc.RPCProxy('publisher_warranty.contract').del_user_message(log_id)
        except Exception, e:
            error = e
        return dict(error=error)


# vim: ts=4 sts=4 sw=4 si et
