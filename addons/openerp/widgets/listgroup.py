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

def parse(group_by, hiddens, headers, group_level, groups):
    
    for grp in range(len(group_by)):
        if 'group_' in group_by[grp]:
            group_by[grp] = group_by[grp].split("group_")[-1]
            
    new_hidden = ()
    for grp_by in groups:
        for hidden in hiddens:
            if grp_by in hidden:
                new_hidden = hidden
                            
    if not new_hidden:
        for grp_by in groups:
            for cnt, header in enumerate(headers):
                if header[0] == grp_by:
                    headers.pop(cnt)
                    headers.insert(groups.index(grp_by), header)
    
    return group_by, hiddens, headers

def parse_groups(group_by, grp_records, headers, ids, model,  offset, limit, context, data):
    proxy = rpc.RPCProxy(model)
    grouped = []
    grp_ids = []
    for grp in grp_records:
        inner = {}
        for key, head in headers:
            if not isinstance(head, int):
                kind = head.get('type')
                if kind == 'progressbar':
                    inner[key] = CELLTYPES[kind](value=grp.get(key), **head)
        grouped.append(inner)
        
    child = len(group_by) == 1
       
    if grp_records:
        for rec in grp_records:
            for grp_by in group_by:
                if not rec.get(grp_by):
                    rec[grp_by] = ''

            rec_dom =  rec.get('__domain')
            dom = [('id', 'in', ids), rec_dom[0]]
            ch_ids = []
            if child:
                ch_ids = [d for id in proxy.search(dom, offset, limit, 0, context)
                            for  d in data
                            if d.get('id') == id]
                
            rec['child_rec'] = ch_ids
            rec['group_id'] = 'group_' + str(random.randrange(1, 10000))
            rec['group_by_id'] = group_by[0]+'_'+str(grp_records.index(rec))
            
    return grouped, grp_ids


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
            
        super(ListGroup, self).__init__(
            name=name, model=model, view=view, ids=self.ids, domain=self.domain,
            context=self.context, limit=self.limit, count=self.count,
            offset=self.offset, editable=self.editable,
            selectable=self.selectable)
        
        self.group_by_ctx, self.hiddens, self.headers = parse(self.group_by_ctx, self.hiddens, self.headers, None, self.group_by_ctx)
                            
        self.context['group_by'] = self.group_by_ctx
        
        
        self.grp_records = proxy.read_group(self.context.get('__domain', []) + (self.domain or []),
                                                fields.keys(), self.group_by_ctx, 0, False, self.context)   
        
        self.grouped, grp_ids = parse_groups(self.group_by_ctx, self.grp_records, self.headers, self.ids, model,  self.offset, self.limit, self.context, self.data)

                
class MultipleGroup(List):
    
    template = "templates/multiple_group.mako"
    params = ['grp_records', 'group_by_ctx', 'grouped', 'parent_group', 'group_level']
    
    def __init__(self, name, model, view, ids=[], domain=[], parent_group=None, group_level=0, groups = [], context={}, **kw):
        self.context = context or {}
        self.domain = domain or []

        self.selectable = kw.get('selectable', 0)
        self.editable = kw.get('editable', False)
        self.pageable = kw.get('pageable', True)

        self.offset = kw.get('offset', 0)
        self.limit = kw.get('limit', 80)
        self.count = kw.get('count', 0)
        self.link = kw.get('nolinks')
        self.parent_group = parent_group or None
        self.group_level = group_level or 0
        
        proxy = rpc.RPCProxy(model)
        if ids == None:
            if self.limit > 0:
                ids = proxy.search(self.domain, self.offset, self.limit, 0, rpc.session.context.copy())
            else:
                ids = proxy.search(self.domain, 0, 0, 0, rpc.session.context.copy())
            
            if len(ids) < self.limit:
                self.count = len(ids)
            else:
                self.count = proxy.search_count(domain, rpc.session.context.copy())

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
        super(MultipleGroup, self).__init__(
            name=name, model=model, view=view, ids=self.ids, domain=self.domain,
            parent_group=parent_group, group_level=group_level, groups=groups, context=self.context, limit=self.limit, 
            count=self.count,offset=self.offset, editable=self.editable,
            selectable=self.selectable)
        self.group_by_ctx, self.hiddens, self.headers = parse(self.group_by_ctx, self.hiddens, self.headers, self.group_level, groups)
                                         
        self.grp_records = proxy.read_group(self.context.get('__domain', []),
                                                fields.keys(), self.group_by_ctx, 0, False, self.context)   

        self.grouped, grp_ids = parse_groups(self.group_by_ctx, self.grp_records, self.headers, self.ids, model,  self.offset, self.limit, rpc.session.context.copy(), self.data)                            
                