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
import re

import cherrypy

from openobject import tools

from openobject.tools import url
from openobject.tools import expose
from openobject.tools import redirect
from openobject.tools import find_resource

from openerp.utils import rpc
from openerp.utils import cache
from openerp.utils import common

from openerp.controllers import SecuredController, unsecured
from openerp.controllers import login as tiny_login


def _cp_on_error():
    
    errorpage = cherrypy.request.pool.get_controller("/errorpage")
    message = errorpage.render()
    cherrypy.response.status = 500
    #cherrypy.response.headers['Content-Type'] = 'text/html'
    cherrypy.response.body = [message]
    
cherrypy.config.update({'request.error_response': _cp_on_error})

class Root(SecuredController):

    _cp_path = "/"

    def user_action(self, id='action_id'):
        """Perform default user action.

        @param id: `action_id` or `menu_id`
        """

        proxy = rpc.RPCProxy("res.users")
        act_id = proxy.read([rpc.session.uid], [id, 'name'], rpc.session.context)
        
        if not act_id[0][id]:
            common.warning(_('You can not log into the system!\nAsk the administrator to verify\nyou have an action defined for your user.'), _('Access Denied!'))
            rpc.session.logout()
            raise redirect('/');

        act_id = act_id[0][id][0]
        
        import actions
        return actions.execute_by_id(act_id)

    @expose()
    def index(self):
        """Index page, loads the view defined by `action_id`.
        """
        return self.user_action('action_id')
        return dict()
    
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
    
    @expose(template="templates/menu.mako")
    def menu2(self, **kw):
         
        from openerp.widgets import tree_view
        from openerp.utils import icons
         
        p_id = kw.get('p_id', None)
        
        view = cache.fields_view_get('ir.ui.menu', 1, 'tree', {})
        tree = tree_view.ViewTree(view, 'ir.ui.menu', [], domain=[('parent_id', '=', False)], context={}, action="/tree/action")
        
        proxy = rpc.RPCProxy('ir.ui.menu')
        
        toolbar = tree.toolbar or []
        new_toolbar = []
        show_formview = False     # Below static tab, contents will initial display False.
        
        for tool in toolbar:
            if p_id and int(p_id) == tool['id']:
                    
                t = tree_view.ViewTree(view, 'ir.ui.menu', int(p_id), domain=[('parent_id', '=', int(p_id))], context={}, action="/tree/action")
                new_tool = []
                
                child_toolbar = t.toolbar
                
                for ch_tool in child_toolbar:
                    if ch_tool.get('icon'):
                        ch_tool['icon'] = icons.get_icon(ch_tool['icon'])
                    else:
                        ch_tool['icon'] = False
                    
                    t1 = tree_view.ViewTree(view, 'ir.ui.menu', ch_tool['id'], domain=[('parent_id', '=', ch_tool['id'])], context={}, action="/tree/action")

                    t1.tree._name = "tree_%s" %(ch_tool['id'])
                    t1.tree.onselection = None
                    t1.tree.onheaderclick = None
                    t1.tree.showheaders = 0
                    t1.tree.linktarget = "'appFrame'"
                    
                    ch_tool['tree'] = t1.tree
                    new_tool += [ch_tool]
                
                show_formview = True
                new_toolbar = new_tool
                
        return dict(new_toolbar=new_toolbar, toolbar=toolbar, show_formview=show_formview)
        
    @expose()
    def menu(self):
        """Main menu page, loads the view defined by `menu_id`.
        """
        return self.user_action('menu_id')

    @expose(allow_json=True)
    @unsecured
    def login(self, db=None, user=None, password=None, style=None, location=None, **kw):

        location = url(location or '/', kw or {})

        if db and user and user.startswith("anonymous"):
            if rpc.session.login(db, user, password):
                raise redirect(location)

        if cherrypy.request.params.get('tg_format') == 'json':
            if rpc.session.login(db, user, password) > 0:
                return dict(result=1)
            return dict(result=0)

        if style in ('ajax', 'ajax_small'):
            return dict(db=db, user=user, password=password, location=location, 
                    style=style, cp_template="templates/login_ajax.mako")

        return tiny_login(target=location, db=db, user=user, password=password, action="login")

    @expose()
    @unsecured
    def logout(self):
        """ Logout method, will terminate the current session.
        """
        rpc.session.logout()
        raise redirect('/')

    @expose(template="templates/about.mako")
    @unsecured
    def about(self):
        from openobject import release
        version = _("Version %s") % (release.version,)
        return dict(version=version)


# vim: ts=4 sts=4 sw=4 si et

