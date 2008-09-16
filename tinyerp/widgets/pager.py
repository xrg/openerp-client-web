###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
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
    pager_id = 1

    def __init__(self, id=False, ids=[], offset=0, limit=20, count=0, view_type='tree'):

        super(Pager, self).__init__()

        self.limit = limit or 20
        self.offset = offset or 0
        self.count = count

        self.id = id or False
        self.ids = ids or []
        
        if len(self.ids) > self.limit:
            self.ids = self.ids[self.offset:]
            self.ids = self.ids[:min(self.limit, len(self.ids))]

        if view_type == 'form':

            index = 0
            if self.id in self.ids:
                index = self.offset + self.ids.index(self.id) + 1

            self.page_info = _("[%s/%s]") % (index or '-', self.count)

            self.prev = index > 1
            self.next = index < self.count

        else:
            index = (self.count or 0) and self.offset + 1
            
            o = self.offset + len(self.ids)
            o = min(self.count, o)

            self.page_info = _("[%s - %s of %s]") % (index, o, self.count)
            self.prev = self.offset > 0
            self.next = self.offset+len(self.ids) < self.count

# vim: ts=4 sts=4 sw=4 si et

