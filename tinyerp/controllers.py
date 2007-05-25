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
from tinyerp import widgets as tw
from tinyerp.tinyres import TinyResource

from tinyerp.modules import *
from tinyerp.widgets import *

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

# initialize the rpc session
rpc.session = rpc.RPCSession(store=SessionStore())

class Root(controllers.RootController, TinyResource):
    """Turbogears root controller, see TG docs for more info.
    """

    @expose()
    def index(self):
        """ The index page
        """
        proxy = rpc.RPCProxy("res.users")
        act_id = proxy.read([rpc.session.uid], ['action_id', 'name'], rpc.session.context)

        if not act_id[0]['action_id']:
            common.warning('You can not log into the system !\nAsk the administrator to verify\nyou have an action defined for your user.','Access Denied !')
            rpc.session.logout()
            raise redirect('/');

        act_id = act_id[0]['action_id'][0]

        return actions.execute_by_id(act_id)

    def _cp_on_error(self, *args, **kw):
        etype, value, tb = sys.exc_info()

        if isinstance(value, common.TinyException):
            raise redirect('/error', message=value.message, title=value.title)

        elif not cherrypy.config.get('server.environment') == 'development':
            raise redirect('/error', message=value, title="Internal Error")

        else:
            message = cgitb.html((etype, value, tb))
            cherrypy.response.headers['Content-Type'] = 'text/html'
            cherrypy.response.body = [message]

    @expose(template="tinyerp.templates.error")
    def error(self, title=None, message=None):
        return dict(title=title, message=message)

    @expose()
    def logout(self):
        """ Logout method, will terminate the current session.
        """
        rpc.session.logout()
        raise redirect('/')

    form = gui.form.Form()
    tree = gui.tree.Tree()
    graph = gui.graph.Graph()
    wizard = gui.wizard.Wizard()
    search = gui.search.Search()
    many2one = gui.many2one.M2O()
    many2many = gui.many2many.M2M()
    dbadmin = gui.dbadmin.DBAdmin()
    pref = gui.preferences.Preferences()
    selection = gui.selection.Selection()
    shortcuts = gui.shortcuts.Shortcuts()
    requests = gui.requests.Requests()
    openm2o = gui.openm2o.Form()

