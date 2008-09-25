###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
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
# along with this program; if not, write to the 
# Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
# Boston, MA  02111-1307, USA.
#
###############################################################################

"""
This module implementes the RootController of the TurboGears application.
For more information on TG controllers, please see the TG docs.
"""

import sys
import os.path
import cgitb

from turbogears import controllers
from turbogears import expose
from turbogears import redirect
from turbogears import config

import cherrypy

from openerp import rpc
from openerp import common
from openerp import stdvars

from openerp import subcontrollers
from openerp import cache

from openerp.tinyres import TinyResource, unsecured

import pkg_resources
from turbogears.widgets import register_static_directory

treegrid_static_dir = pkg_resources.resource_filename("openerp",  "static")
register_static_directory("openerp", treegrid_static_dir)

config.update({'i18n.gettext' : cache.gettext})

# initialize the rpc session
host = config.get('host', path="openerp")
port = config.get('port', path="openerp")
protocol = config.get('protocol', path="openerp")
rpc.session = rpc.RPCSession(host, port, protocol, storage=cherrypy.session)

class Root(controllers.RootController, TinyResource):
    """Turbogears root controller, see TG docs for more info.
    """

    def user_action(self, id='action_id'):
        """Perform default user action.

        @param id: `action_id` or `menu_id`
        """

        proxy = rpc.RPCProxy("res.users")
        act_id = proxy.read([rpc.session.uid], [id, 'name'], rpc.session.context)

        if not act_id[0][id]:
            common.warning(_('You can not log into the system !\nAsk the administrator to verify\nyou have an action defined for your user.'), _('Access Denied !'))
            rpc.session.logout()
            raise redirect('/');

        act_id = act_id[0][id][0]

        return subcontrollers.actions.execute_by_id(act_id)

    @expose()
    def index(self):
        """Index page, loads the view defined by `action_id`.
        """
        return self.user_action('action_id')

    @expose()
    def menu(self):
        """Main menu page, loads the view defined by `menu_id`.
        """
        return self.user_action('menu_id')

    def _cp_on_error(self, *args, **kw):
        etype, value, tb = sys.exc_info()

        if isinstance(value, common.TinyException) or not cherrypy.config.get('server.environment') == 'development':
            cherrypy.session._last_error = value
            raise redirect('/error')
        else:
            message = cgitb.html((etype, value, tb))
            cherrypy.response.headers['Content-Type'] = 'text/html'
            cherrypy.response.body = [message]

    @expose(template="openerp.templates.error")
    @unsecured
    def error(self):

        title = "Internal error!"
        error = "Unknown error!"

        if hasattr(cherrypy.session, '_last_error'):
            error = cherrypy.session._last_error

        if isinstance(error, common.TinyException):
            title = error.title
            error = error.message

        return dict(title=title, message=error)

    @expose(template="openerp.templates.login")
    @unsecured
    def login(self, db=None, user=None, password=None):

        message = None

        url = rpc.session.get_url()
        dblist = rpc.session.listdb()
        manage_visible = config.get('manage.visible', path='admin')
        
        if dblist == -1:
            dblist = []
            message = _("Could not connect to server !")

        return dict(target='/', url=url, manage_visible=manage_visible, dblist=dblist, user=user, password=password, db=db, action='login', message=message, origArgs={})

    @expose()
    @unsecured
    def get_logo(self):          
        
        comp_url = config.get('company_url', path='admin') or None
        
        res="""<img src="/static/images/openerp_big.png" alt="${_('Open ERP')}" border="0" width="200px" height="60px" usemap="#logo_map"/>
                    <map name="logo_map">
                        <area shape="rect" coords="102,42,124,56" href="http://openerp.com" target="_blank"/>
                        <area shape="rect" coords="145,42,184,56" href="http://axelor.com" target="_blank"/>
                    </map>"""
                    
        if os.path.exists(pkg_resources.resource_filename("openerp", "static/images/company_logo.png")):
            if comp_url:
                res = """   <a href='"""+comp_url+"""' target='_blank'>
                                <img src='/static/images/company_logo.png' alt="" border="0" width="205px" height="58px"/> 
                            </a> """
            else:
                 res = """<img src="/static/images/company_logo.png" alt="" border="0" width="205px" height="58px"/>"""
        return res
    
    @expose(template="openerp.templates.admin")
    @unsecured
    def admin(self):
        return dict()
    
    @expose()
    @unsecured
    def logout(self):
        """ Logout method, will terminate the current session.
        """
        rpc.session.logout()
        raise redirect('/')

    @expose(template="openerp.templates.about")
    @unsecured
    def about(self):
        from release import version
        return dict(version=version)

    form = subcontrollers.form.Form()
    tree = subcontrollers.tree.Tree()
    graph = subcontrollers.graph.Graph()
    wizard = subcontrollers.wizard.Wizard()
    search = subcontrollers.search.Search()
    pref = subcontrollers.preferences.Preferences()
    selection = subcontrollers.selection.Selection()
    shortcuts = subcontrollers.shortcuts.Shortcuts()
    requests = subcontrollers.requests.Requests()
    openm2o = subcontrollers.openm2o.OpenM2O()
    openo2m = subcontrollers.openo2m.OpenO2M()    
    listgrid = subcontrollers.listgrid.List()
    attachment = subcontrollers.attachment.Attachment()
    translator = subcontrollers.translator.Translator()
    impex = subcontrollers.impex.ImpEx()
    fieldpref = subcontrollers.fieldpref.FieldPref()
    calendar = subcontrollers.tinycalendar.TinyCalendar()
    calpopup = subcontrollers.tinycalendar.CalendarPopup()
    viewlog = subcontrollers.view_log.View_Log()
    image = subcontrollers.image.Image()    
    admin = subcontrollers.admin.Admin()
    viewed = subcontrollers.viewed.ViewEd()
    viewlist = subcontrollers.viewlist.ViewList()
    workflow = subcontrollers.workflow.Workflow()
    workflowlist = subcontrollers.workflow.WorkflowList()
    process = subcontrollers.process.Process()
    
# vim: ts=4 sts=4 sw=4 si et

