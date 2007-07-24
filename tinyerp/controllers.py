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

"""
This module implementes the RootController of the TurboGears application.
For more information on TG controllers, please see the TG docs.
"""

import sys
import cgitb

from turbogears import controllers
from turbogears import expose
from turbogears import redirect
from turbogears import config

import cherrypy

from tinyerp import rpc
from tinyerp import common
from tinyerp import stdvars

from tinyerp import subcontrollers

from tinyerp.tinyres import TinyResource, unsecured

import pkg_resources
from turbogears.widgets import register_static_directory

treegrid_static_dir = pkg_resources.resource_filename("tinyerp",  "static")
register_static_directory("tinyerp", treegrid_static_dir)

class SessionStore(object):

    def __getitem__(self, name):
        try:
            return cherrypy.session[name]
        except:
            return None

    def __setitem__(self, name, value):
        try:
            cherrypy.session[name] = value
        except:
            pass

    def __delitem__(self, name):
        try:
            del cherrypy.session[name]
        except:
            pass

    def get(self, name, default=None):
        try:
            return cherrypy.session.get(name, default)
        except:
            return default

    def clear(self):
        cherrypy.session.clear()

# initialize the rpc session
rpc.session = rpc.RPCSession(store=SessionStore())

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

    @expose(template="tinyerp.templates.error")
    def error(self):

        title = "Internal error!"
        error = "Unknown error!"
        
        if hasattr(cherrypy.session, '_last_error'):
            error = cherrypy.session._last_error

        if isinstance(error, common.TinyException):
            title = error.title
            error = error.message            
        
        return dict(title=title, message=error)

    @expose(template="tinyerp.templates.login")
    @unsecured
    def login(self, db=None, user=None, passwd=None):

        host = config.get('host', path="tinyerp")
        port = config.get('port', path="tinyerp")
        protocol = config.get('protocol', path="tinyerp")

        dblist = rpc.session.listdb(host, port, protocol)

        url = "%s://%s:%s"%(protocol, host, port)

        return dict(target='/', url=url, dblist=dblist, user=user, passwd=passwd, db=db, action='login', message=None, origArgs={})

    @expose()
    @unsecured
    def logout(self):
        """ Logout method, will terminate the current session.
        """
        rpc.session.logout()
        raise redirect('/')

    @expose(template="tinyerp.templates.about")
    @unsecured
    def about(self):
        return dict()

    form = subcontrollers.form.Form()
    tree = subcontrollers.tree.Tree()
    graph = subcontrollers.graph.Graph()
    wizard = subcontrollers.wizard.Wizard()
    search = subcontrollers.search.Search()
    dbadmin = subcontrollers.dbadmin.DBAdmin()
    pref = subcontrollers.preferences.Preferences()
    selection = subcontrollers.selection.Selection()
    shortcuts = subcontrollers.shortcuts.Shortcuts()
    requests = subcontrollers.requests.Requests()
    openm2o = subcontrollers.openm2o.OpenM2O()
    openo2m = subcontrollers.openo2m.OpenO2M()
    configure = subcontrollers.confeditor.ConfEditor()
    listgrid = subcontrollers.listgrid.List()
    attachment = subcontrollers.attachment.Attachment()
    translator = subcontrollers.translator.Translator()
    impex = subcontrollers.impex.ImpEx()
    fieldpref = subcontrollers.fieldpref.FieldPref()
    