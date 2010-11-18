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
# -   All names, links and logos of Tiny, OpenERP and Axelor must be
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

from openerp.widgets import TinyWidget


class Pager(TinyWidget):

    template = "/openerp/widgets/templates/pager.mako"
    params = ['offset', 'limit', 'count', 'prev', 'next', 'page_info', 'pager_id', 'pager_options']

    page_info = None
    pager_id = 1
    UNLIMITED = -1

    def __init__(self, id=False, ids=[], offset=0, limit=50, count=0, view_type='tree'):

        super(Pager, self).__init__()

        self.id = id
        self.ids = ids or []
        self.view_type = view_type

        self.offset = offset or 0
        self.limit = limit or 50
        self.count = count or 0
        self.pager_options = []
        
        self.pager_options = [20, 50, 100, 500]

        if self.limit != Pager.UNLIMITED and len(self.ids) > self.limit:
            # if self.ids isn't clamped, it is entirely un-paginated.
            self.ids = self.ids[self.offset:self.offset + self.limit]

        if self.view_type in ['form', 'diagram']:        

            index = 0
            if self.id in self.ids:
                index = self.offset + self.ids.index(self.id) + 1

            self.page_info = _("%s") % (index or '-')

            self.prev = index > 1
            self.next = index < self.count

        else:
            index = (self.count or 0) and self.offset + 1

            o = self.offset + len(self.ids)
            o = min(self.count, o)

            self.page_info = _("%s - %s") % (index, o)
            self.prev = self.offset > 0
            self.next = self.offset+len(self.ids) < self.count

# vim: ts=4 sts=4 sw=4 si et
