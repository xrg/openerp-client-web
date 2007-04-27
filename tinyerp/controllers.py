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

import cherrypy

from tinyerp import rpc
from tinyerp import common
from tinyerp import modules
from tinyerp import widgets as tw
from tinyerp.tinyres import TinyResource

from tinyerp.modules import *
from tinyerp.widgets import *
from tinyerp import rpc

class Root(controllers.RootController, TinyResource):
    """Turbogears root controller, see TG docs for more info.
    """

    @expose(template="tinyerp.templates.index")
    def index(self):
        """ The index page
        """
        menu = tree.Tree(id="menu", title="TinyERP", url="/menu_items", model="ir.ui.menu", action="/menu", target="contentpane")
        return dict(menu_tree=menu)

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

    @expose()
    def menu(self, model, id):
        id = int(id)
        return actions.execute_by_keyword('tree_but_open', model=model, id=id, ids=[id], report_type='pdf')

    menu_items = tree.Tree.items;

    form = gui.form.Form()
    tree = gui.tree.Tree()
    wizard = gui.wizard.Wizard()
    search = gui.search.Search()
    many2one = gui.many2one.M2O()
    many2many = gui.many2many.M2M()
    dbadmin = gui.dbadmin.DBAdmin()
    pref = gui.preferences.Preferences()
    selection = gui.selection.Selection()
