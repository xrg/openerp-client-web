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
import random

from openerp.utils import rpc
from openerp.widgets import get_widget

from listgrid import List, CELLTYPES


class ListGroup(List):

    template = "templates/listgroup.mako"
    params = ['grp_records', 'group_by_ctx', 'grouped']

    def __init__(self, name, model, view, ids=[], domain=[], context={}, **kw):

        self.context = context or {}
        self.domain = domain or []

        self.selectable = kw.get('selectable', 0)
        self.editable = kw.get('editable', False)
        self.pageable = kw.get('pageable', True)

        self.offset = kw.get('offset', 0)
        self.limit = kw.get('limit', 0)
        self.count = kw.get('count', 0)
        self.link = kw.get('nolinks')

        proxy = rpc.RPCProxy(model)

        if ids == None:
            if self.limit > 0:
                ids = proxy.search(self.domain, self.offset, self.limit, 0, self.context)
            else:
                ids = proxy.search(self.domain, 0, 0, 0, self.context)
            
            if len(ids) < self.limit:
                self.count = len(ids)
            else:
                self.count = proxy.search_count(domain, context)

        if ids and not isinstance(ids, list):
            ids = [ids]

        self.ids = ids

        self.concurrency_info = None

        self.group_by_ctx = kw.get('group_by_ctx', [])

        if not isinstance(self.group_by_ctx, list):
            self.group_by_ctx = [self.group_by_ctx]

        fields = view['fields']

        self.grp_records = []
        group_field = None

        self.context.update(rpc.session.context.copy())
        grp = self.context.get('group_by', False)
        self.no_leaf = self.context.get('group_by_no_leaf', False)
        if self.no_leaf:
            self.editable = False
            
        super(ListGroup, self).__init__(
            name=name, model=model, view=view, ids=self.ids, domain=self.domain,
            context=self.context, limit=self.limit, count=self.count,
            offset=self.offset, editable=self.editable,
            selectable=self.selectable)

        if self.group_by_ctx:
            t = []
            if self.group_by_ctx and isinstance(self.group_by_ctx[0], basestring):
                self.group_by_ctx = self.group_by_ctx[0].split(',')
            
            for i in self.group_by_ctx:
                if 'group_' in i:
                    t.append((i.split('group_'))[1])
                else:
                    t.append(i)
                    
            gb = t[0]
            self.group_by_ctx = gb

            new_hidden = ()
            for hidden in self.hiddens:
                if gb == hidden[0]:
                    hiden = {}
                    for h in hidden[1]:
                        if h != 'invisible':
                            hiden[h] = hidden[1].get(h)
                    new_hidden = (gb, hiden)
                    self.headers.insert(0, new_hidden)
            if not new_hidden:
                for cnt, header in enumerate(self.headers):
                    head = header
                    if header[0] == gb:
                        self.headers.pop(cnt)
                        self.headers.insert(0, head)

            self.grp_records = proxy.read_group(self.context.get('__domain', []) + (self.domain or []),
                                                fields.keys(), gb, 0, False, self.context)    
        
        self.grouped = []
        
        for grp in self.grp_records:
            inner = {}
            for key, head in self.headers:
                if not isinstance(head, int):
                    kind = head.get('type')
                    if kind == 'progressbar':
                        inner[key] = CELLTYPES[kind](value=grp.get(key), **head)
            self.grouped.append(inner)
                
        grp_ids = []
        
        if self.grp_records:
            for rec in self.grp_records:
                child = True
                if not rec.get(self.group_by_ctx):
                    rec[self.group_by_ctx] = ''

                rec_dom =  rec.get('__domain')
                dom = [('id', 'in', self.ids), rec_dom[0]]
                inner_gb = self.context.get('group_by', [])
                if self.no_leaf and not len(inner_gb):
                    child = False
                ch_ids = []
                if child:
                    grp_ids = proxy.search(dom, self.offset, self.limit, 0, self.context)
                    for id in grp_ids:
                        for d in self.data:
                            if d.get('id') == id:
                                ch_ids.append(d)
                rec['child_rec'] = ch_ids
                rec['group_id'] = 'group_' + str(random.randrange(1, 10000))
                