###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
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

import turbogears as tg

from interface import TinyField
from form import Form
from listgrid import List

from tinyerp import rpc
from tinyerp import cache

import validators as tiny_validators

class M2M(TinyField, tg.widgets.CompoundWidget):
    """many2many widget
    """

    template = "tinyerp.widgets.templates.many2many"
    params = ['relation', 'domain', 'context', 'inline']
    javascript = [tg.widgets.JSLink("tinyerp", "javascript/m2m.js", location=tg.widgets.js_location.bodytop)]

    relation = None
    domain = []
    context = {}
    inline = False

    member_widgets = ['list_view']

    def __init__(self, attrs={}):
        super(M2M, self).__init__(attrs)
        tg.widgets.CompoundWidget.__init__(self)

#        self.colspan = 4
#        self.nolabel = True
        self.inline = attrs.get('inline')
        self.relation = attrs.get('relation', '')
        self.domain = attrs.get('domain', [])
        self.context = attrs.get('context', {}) or {}

        self.view = attrs.get('views',{})
        self.domain  = attrs.get('domain',{})
        self.ids = attrs.get('value') or []

        if not self.view:
            ctx = rpc.session.context.copy()
            ctx.update(self.context)
            self.view = cache.fields_view_get(self.relation, {}, 'tree', ctx, False)

        self.list_view = List(self.name, self.relation, self.view, ids=self.ids, domain=self.domain, context=self.context, selectable=(self.editable or 0) and 2, pageable=False)
        self.list_view.show_links = -1

        self.validator = tiny_validators.many2many()

    def set_value(self, value):

        ids = value
        if isinstance(ids, basestring):
            if not ids.startswith('['):
                ids = '[' + ids + ']'

            ids = eval(ids)

        self.ids = ids
        self.list_view.ids = ids
