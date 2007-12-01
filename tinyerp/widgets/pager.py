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

from turbogears import widgets

from interface import TinyCompoundWidget

class Pager(TinyCompoundWidget):

    template = "tinyerp.widgets.templates.pager"
    params = ['offset', 'limit', 'count', 'prev', 'next', 'page_info', 'pager_id']

    css = [widgets.CSSLink('tinyerp', 'css/pager.css')]

    offset = 0
    limit = 20
    count = 0

    page_info = None
    pager_id = 'pager'

    def __init__(self, id=False, ids=[], offset=0, limit=20, count=0, view_type='tree'):

        super(Pager, self).__init__()

        self.limit = limit or 20
        self.offset = offset or 0
        self.count = count

        self.id = id or False
        self.ids = ids or []

        if view_type == 'form':

            index = 0
            if self.id in self.ids:
                index = self.offset + self.ids.index(self.id) + 1

            self.page_info = _("[%s/%s]") % (index or '-', self.count)

            self.prev = index > 1
            self.next = index < self.count

        else:
            index = (self.count or 0) and self.offset + 1

            self.page_info = _("[%s - %s of %s]") % (index, self.offset + len(self.ids), self.count)
            self.prev = self.offset > 0
            self.next = self.offset+len(self.ids) < self.count

