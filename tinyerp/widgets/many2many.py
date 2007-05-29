###############################################################################
#
# Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id: list.py 7 2007-03-23 12:58:38Z ame $
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

from interface import TinyField
from form import Form
from list import List

from tinyerp import rpc

import validators as tiny_validators

class M2M(TinyField, tg.widgets.CompoundWidget):
    """many2many widget
    """

    template = "tinyerp.widgets.templates.many2many"
    params = ['relation', 'domain', 'context']

    relation = None
    domain = []
    context = {}

    member_widgets = ['list_view']

    def __init__(self, attrs={}):
        super(M2M, self).__init__(attrs)
        tg.widgets.CompoundWidget.__init__(self)

#        self.colspan = 4
#        self.nolabel = True

        self.relation = attrs.get('relation', '')
        self.domain = attrs.get('domain', [])
        self.context = attrs.get('context', {}) or {}

        self.view = attrs.get('views',{})
        self.domain  = attrs.get('domain',{})
        self.ids = attrs['value'] or []

        if not self.view:
            proxy = rpc.RPCProxy(self.relation)

            ctx = rpc.session.context.copy()
            ctx.update(self.context)

            self.view = proxy.fields_view_get({}, 'tree', ctx)

        self.list_view = List(self.name, self.relation, self.view, ids=self.ids, domain=self.domain, context=self.context, selectable=2, pageable=False)

        self.validator = tiny_validators.many2many()
