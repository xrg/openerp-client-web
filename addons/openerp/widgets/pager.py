###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# The OpenERP web client is distributed under the "OpenERP Public License".
# It's based on Mozilla Public License Version (MPL) 1.1 with following
# restrictions:
#
# -   All names, links and logos of Tiny, Open ERP and Axelor must be
#     kept as in original distribution without any changes in all software
#     screens, especially in start-up page and the software header, even if
#     the application source code has been changed or updated or code has been
#     added.
#
# -   All distributions of the software must keep source code with OEPL.
#
# -   All integrations to any other software must keep source code with OEPL.
#
# If you need commercial licence to remove this kind of restriction please
# contact us.
#
# You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################

from openobject.widgets import CSSLink
from openerp.widgets import TinyWidget


class Pager(TinyWidget):

    template = "templates/pager.mako"
    params = ['offset', 'limit', 'count', 'prev', 'next', 'page_info', 'pager_id', 'pager_options']

    css = [CSSLink("openerp", 'css/pager.css')]

    page_info = None
    pager_id = 1

    def __init__(self, id=False, ids=[], offset=0, limit=20, count=0, view_type='tree'):

        super(Pager, self).__init__()

        self.id = id
        self.ids = ids or []
        self.view_type = view_type

        self.offset = offset or 0
        self.limit = limit or 20
        self.count = count or 0
        self.pager_options = []
        
        
        self.pager_options = [20, 50, 100, 500]

        if self.limit != -1 and len(self.ids) > self.limit:
            self.ids = self.ids[self.offset:]
            self.ids = self.ids[:min(self.limit, len(self.ids))]

#        if self.view_type == 'form':
        if self.view_type in ['form', 'diagram']:        

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
