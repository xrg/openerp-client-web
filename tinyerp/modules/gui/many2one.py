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

import cherrypy

from turbogears import expose
from turbogears import widgets
from turbogears import controllers

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp import tools
from tinyerp import widgets as tw
from tinyerp import widgets_search as tws

from tinyerp.modules.utils import TinyDict

import search

class M2O(search.Search):

    def _get_onok(self, params):
        return "onok()"

    def _get_oncancel(self, params):
        return "window.close();"

    def _get_onfind(self, params):
        return "submit_form('/many2one/find')"

    def _get_javascript(self, params):
        code = []
        return code

    def _get_hiddenfield(self, params):
        field = widgets.HiddenField(name='_terp_m2o', default=params.m2o)
        return [field]

    @expose()
    def new(self, model, m2o, **kw):

        params = TinyDict()
        params.model = model
        params.m2o = m2o

        return self.create(params)

    @expose('json')
    def ok(self, **kw):
        params, data = TinyDict.split(kw)

        ids = [int(id) for id in data.get('search_list', [])]
        return dict(ids=ids)

    @expose('json')
    def get_name(self, model, id):
        name = tw.many2one.get_name(model, id)
        return dict(name=name)
