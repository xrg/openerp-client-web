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

import turbogears as tg
import cherrypy

from tinyerp import rpc
from tinyerp.modules.utils import TinyDict

import tinyerp.widgets as tw

import search

class ViewSearch(tg.widgets.Form):

    template = "tinyerp.widgets_search.templates.search"

    params = ['model', 'state', 'id', 'ids', 'view_ids', 'view_mode', 'view_mode2', 'domain', 'context', 'textid', 'hiddenname']
    member_widgets = ['form_view', 'list_view']

    def __init__(self, terp, **kw):

        super(ViewSearch, self).__init__(**kw)

        self.model         = terp.model
        self.state         = terp.state or None
        self.id            = terp.id or None
        self.ids           = terp.ids or []
        self.view_ids      = terp.view_ids or []
        self.view_mode     = terp.view_mode or ['form', 'tree']
        self.view_mode2    = terp.view_mode2 or ['tree', 'form']

        self.view_type     = self.view_mode[0]
        self.domain        = terp.domain or []
        self.context       = terp.context or {}

        self.textid = terp.textid
        self.hiddenname = terp.hiddenname

        proxy = rpc.RPCProxy(self.model)

        view_form = proxy.fields_view_get({}, 'form', {})
        view_tree = proxy.fields_view_get({}, 'tree', {})

        self.form_view = search.Form(model=self.model, view=view_form, domain=self.domain, context=self.context)
        self.list_view = tw.list.List(model=self.model, ids=self.ids or [], view=view_tree, domain=self.domain, context=self.context, selectable=True)

        self.string = self.form_view.string
