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
from turbogears import redirect
import time

import cherrypy

from tinyerp import rpc
from tinyerp import common

from tinyerp import widgets as tw
from tinyerp.tinyres import TinyResource


class Preferences(controllers.Controller, TinyResource):

    @expose(template="tinyerp.modules.gui.templates.preferences")
    def create(self):
        sock =rpc.RPCProxy('ir.values')
        res = sock.get('meta', False, [['res.users', False]], True, {}, True)
        lang = cherrypy.request.simple_cookie.get('terp_lang','')
        if lang:
            lang=lang.value
        field = tw.form.Selection({'name':'lang','selection':res[0][3]['selection'],'label':'Language','string':'Language'});
        field.set_value(lang)

        return dict(field=field)

    @expose()
    def ok(self, lang, cancel=None):
        if cancel:
            return " "

        cherrypy.session['terp_lang'] = lang

        rpc.session.logout()

        raise redirect('/')


