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


import xml.dom.minidom
from elementtree import ElementTree as ET

import turbogears as tg

from tinyerp import tools
from tinyerp import rpc

from interface import TinyWidget
from interface import TinyField

import form
import list

class Screen(tg.widgets.CompoundWidget):
    template = """<span>${widget.display()}
    </span>
    """
    member_widgets = ['widget']
    widget = None

    def __init__(self, prefix, model, id=None, ids=[], view_ids=[], view_mode=['form', 'tree'], views_preloaded={}, domain=[], context={}, selectable=False, editable=False):

        self.prefix = prefix
        self.model = model
        self.id = id
        self.ids = ids
        self.view_ids = view_ids
        self.view_mode = view_mode
        self.view_type = view_mode[0]
        self.views_preloaded = views_preloaded
        self.domain = domain
        self.context = context.copy()
        self.selectable = selectable
        self.editable = editable

        self.rpc = rpc.RPCProxy(model)

        view_id = False
        if view_ids:
            view_id = view_ids[0]

        view_type = view_mode[0]

        if view_type in views_preloaded:
            view = views_preloaded[view_type]
        else:
            view = self.rpc.fields_view_get(view_id, view_type, self.context)

        if view_type == 'form':
            self.widget = form.Form(prefix=prefix, model=model, view=view, ids=(id or []) and [id], editable=editable, selectable=selectable)
        else:
            self.widget = list.List(model=model, view=view, ids=ids, editable=editable, selectable=selectable)
            self.ids = self.widget.ids

        self.string = self.widget.string
