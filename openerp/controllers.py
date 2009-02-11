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

"""
This module implementes the RootController of the TurboGears application.
For more information on TG controllers, please see the TG docs.
"""

import os

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
            common.warning(_('You can not log into the system!\nAsk the administrator to verify\nyou have an action defined for your user.'), _('Access Denied!'))
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
        message = self.errorpage.render()
        cherrypy.response.headers['Content-Type'] = 'text/html'
        cherrypy.response.body = [message]

    @expose(template="openerp.templates.login")
    @unsecured
    def login(self, db=None, user=None, password=None):

        message = None

        url = rpc.session.get_url()
        dblist = rpc.session.listdb()
        
        if dblist == -1:
            dblist = []
            message = _("Could not connect to server!")

        return dict(target='/', url=url, dblist=dblist, user=user, password=password, db=db, action='login', message=message, origArgs={})

    @expose()
    @unsecured
    def get_logo(self):          
        
        comp_url = config.get('company.url', path='openerp-web') or None
        
        res="""<img src="/static/images/openerp_big.png" alt="%(alt)s" border="0" width="200px" height="60px" usemap="#logo_map"/>
                    <map name="logo_map">
                        <area shape="rect" coords="102,42,124,56" href="http://openerp.com" target="_blank"/>
                        <area shape="rect" coords="145,42,184,56" href="http://axelor.com" target="_blank"/>
                    </map>"""%(dict(alt=_('OpenERP')))
                    
        if os.path.exists(pkg_resources.resource_filename("openerp", "static/images/company_logo.png")):
            if comp_url:
                res = """   <a href='"""+comp_url+"""' target='_blank'>
                                <img src='/static/images/company_logo.png' alt="" border="0" width="205px" height="58px"/> 
                            </a> """
            else:
                 res = """<img src="/static/images/company_logo.png" alt="" border="0" width="205px" height="58px"/>"""
        return res
    
    @expose()
    @unsecured
    def developped_by(self):
        comp_url = config.get('company.url', path='openerp-web') or None
        
        res="""<img src="/static/images/developped_by.png" border="0" width="200" height="60" alt="%(alt)s" usemap="#devby_map"/>
                    <map name="devby_map">
                        <area shape="rect" coords="0,20,100,60" href="http://axelor.com" target="_blank"/>
                        <area shape="rect" coords="120,20,200,60" href="http://openerp.com" target="_blank"/>
                    </map>"""%(dict(alt=_('Developped by Axelor and Tiny')))
                    
        if os.path.exists(pkg_resources.resource_filename("openerp", "static/images/company_logo.png")):
            if comp_url:
                res = """   <a href='"""+comp_url+"""' target='_blank'>
                                <img src='/static/images/company_logo.png' alt="" border="0" width="205px" height="58px"/> 
                            </a> """
            else:
                 res = """<img src="/static/images/company_logo.png" alt="" border="0" width="205px" height="58px"/>"""
        return res
    
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
        from openerp import release
        version = _("Version %s-%s") % (release.version, release.release)
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
    openm2m = subcontrollers.openm2m.OpenM2M()   
    listgrid = subcontrollers.listgrid.List()
    attachment = subcontrollers.attachment.Attachment()
    translator = subcontrollers.translator.Translator()
    impex = subcontrollers.impex.ImpEx()
    fieldpref = subcontrollers.fieldpref.FieldPref()
    calendar = subcontrollers.tinycalendar.TinyCalendar()
    calpopup = subcontrollers.tinycalendar.CalendarPopup()
    viewlog = subcontrollers.view_log.View_Log()
    image = subcontrollers.image.Image()    
    database = subcontrollers.database.Database()
    viewed = subcontrollers.viewed.ViewEd()
    viewlist = subcontrollers.viewlist.ViewList()
    workflow = subcontrollers.workflow.Workflow()
    workflowlist = subcontrollers.workflow.WorkflowList()
    process = subcontrollers.process.Process()
    wiki = subcontrollers.wiki.WikiView()
    errorpage = subcontrollers.error_page.ErrorPage()

# vim: ts=4 sts=4 sw=4 si et

