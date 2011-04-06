###############################################################################
#
#  Copyright (C) 2007-TODAY OpenERP SA. All Rights Reserved.
#
#  $Id$
#
#  Developed by OpenERP (http://openerp.com) and Axelor (http://axelor.com).
#
#  The OpenERP web client is distributed under the "OpenERP Public License".
#  It's based on Mozilla Public License Version (MPL) 1.1 with following 
#  restrictions:
#
#  -   All names, links and logos of OpenERP must be kept as in original
#      distribution without any changes in all software screens, especially
#      in start-up page and the software header, even if the application
#      source code has been changed or updated or code has been added.
#
#  You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################
import time
import copy
import cherrypy

from openerp.utils import TinyDict, expr_eval, rpc
from openerp.widgets import TinyInputWidget, register_widget
from openerp.widgets.screen import Screen

__all__ = ["O2M", "OneToMany"]

#O2M tuple format:
#
#(0, _, {values}): CREATE new record (linked to current) with values $values
#(1, id, {values}): UPDATE linked record $id with values $values
#(2, id, _): DELETE linked record $id
#(3, id, _): FORGET linked record $id (removes relation, but not linked record)
#(4, id, _): LINK TO existing record $id
#(5, _, _): FORGET ALL linked records
#(6, _, [ids]): REPLACE LINKS to links to $ids
class OneToMany(object):
    @classmethod
    def create(cls, values=None, **kw):
        """ Returns the command used to create a new o2m linked to the
        current record.

        The values for the record to create can be provided as a dict (or an
        iterable of pairs) and/or as **kwargs, as for the `dict` constructor
        or `dict.update`

        :param values: a dictionary or pair iterable
        :type values: {str: value}
        :rtype: (int, int, dict)
        """
        return 0, False, dict(values or {}, **kw)
    @classmethod
    def replace_all(cls, *with_ids):
        """ Returns the command used to replace all values of an o2m with the
         provided ids. Equivalent to a FORGET ALL followed by a LINK TO

         :param with_ids: the ids to set in the o2m
         :type with_ids: int...
         :rtype: (int, ?, [int])
        """
        return 6, False, with_ids
    @classmethod
    def update(cls, record_id, values):
        """ Returns the command used to update an existing o2m record with the
         provided values

         :param record_id: the id of the o2m record to update
         :type record_id: int
         :param values: the new values to set on the record
         :type values: dict
         :rtype: (int, int, dict)
        """
        return 1, record_id, values

class O2M(TinyInputWidget):
    """One2Many widget
    """
    template = "/openerp/widgets/form/templates/one2many.mako"
    params = ['id', 'parent_id', 'new_attrs', 'pager_info', 'switch_to',
              'default_get_ctx', 'source', 'view_type', 'default_value',
              'edition']
    member_widgets = ['screen']

    form = None
    valign = "top"
    default_value = []

    def __init__(self, **attrs):
        #FIXME: validation error in `Pricelist Version`
        attrs['required'] = False

        super(O2M, self).__init__(**attrs)

        self.new_attrs = { 'text': _("New"), 'help': _('Create new record.')}
        self.default_get_ctx = attrs.get('default_get', {}) or attrs.get('context', {})

        # get top params dictionary
        params = cherrypy.request.terp_params
        self.source = params.source
        self.edition = params.o2m_edit
        pprefix = ''
        if '/' in self.name:
            pprefix = self.name[:self.name.rindex('/')]

        pparams = params.chain_get(pprefix)
        if (pparams and not pparams.id) or (not pparams and not params.id):
            self.new_attrs = { 'text': _("Save/New"), 'help': _('Save parent record.')}

        self.parent_id = params.id
        if pparams:
            self.parent_id = pparams.id

        # get params for this field
        current = params.chain_get(self.name)

        self.model = attrs['relation']
        self.link = attrs.get('link', '')
        self.onchange = None # override onchange in js code

        view = attrs.get('views', {})
        mode = str(attrs.get('mode', 'tree,form')).split(',')

        self.view = view

        view_mode = mode
        view_type = mode[0]
        self.view_type = view_type
        
        if not current:
            current = TinyDict()

        if current.view_mode: view_mode = current.view_mode
        if current.view_type: view_type = current.view_type

        self.switch_to = view_mode[-1]
        if view_type == view_mode[-1]: self.switch_to = view_mode[0]

        ids = attrs.get('value') or []
        if not isinstance(ids, list):
            ids = [ids]

        if ids:
            if isinstance(ids[0], dict):
                current.default_data = ids
                for item in current.default_data:
                    self.default_value.append(
                        OneToMany.create(item))
                    item['id'] = 0
                ids = []
            elif isinstance(ids[0], tuple):
                [current_id[1] for current_id in ids]
        
        id = (ids or None) and ids[0]
        
        if self.name == self.source or self.name == params.source:
            if params.sort_key and ids:
                domain = current.domain or []
                domain.append(('id', 'in', ids))
                ids = rpc.RPCProxy(self.model).search(domain, current.offset, current.limit, params.sort_key + ' '+params.sort_order, current.context)
                id = ids[0]
        if current and params.source and self.name in params.source.split('/'):
            id = current.id

        id = id or None
                
        current.model = self.model
        current.id = id
        current.ids = ids
        current.view_mode = view_mode
        current.view_type = view_type
        current.domain = current.domain or []
        current.context = current.context or {}

        group_by_ctx = ''
        if self.default_get_ctx:
            ctx = dict(cherrypy.request.terp_record,
                       context=current.context,
                       active_id=self.parent_id or False)
            ctx[attrs['name']] = ids
            # XXX: parent record for O2M
            #if self.parent:
            #    ctx['parent'] = EvalEnvironment(self.parent)

            try:
                context = ctx.copy()
                ctx = expr_eval("dict(%s)" % self.default_get_ctx, context)
                ctx.update(expr_eval("dict(%s)" % attrs.get('context', '{}'), context))
                current.context.update(ctx)
            except:
                pass

            if ctx and ctx.get('group_by'):
                group_by_ctx = ctx.get('group_by')

        current.offset = current.offset or 0
        current.limit = current.limit or 50
        current.count = len(ids or [])

        # Group By for one2many list.
        if group_by_ctx:
            current.group_by_ctx = group_by_ctx
            current.domain = [('id', 'in', ids)]

        if current.view_type == 'tree' and self.readonly:
            self.editable = False

        if 'default_name' in current.context:
            del current.context['default_name']

        if self.view_type == 'tree' and pparams:
            self.editable = bool(pparams.id)

        self.screen = Screen(current, prefix=self.name, views_preloaded=view,
                             editable=self.editable, readonly=self.readonly,
                             selectable=0, nolinks=self.link, _o2m=1)
        
        self.id = id
        self.ids = ids

        if view_type == 'tree':
            self.id = None

        elif view_type == 'form':
            records_count = len(self.screen.ids or [])

            current_record = 0
            if records_count and self.screen.id in self.screen.ids:
                current_record = self.screen.ids.index(self.screen.id) + 1
                self.pager_info = _('%d of %d') % (current_record, records_count)
            else:
                self.pager_info = _('- of %d') % (records_count)

    def get_value(self):

        if not self.ids:
            return []

        values = getattr(self.screen.widget, 'values', [])

        return [(1, val.get('id', False), val) for val in values]

register_widget(O2M, ["one2many", "one2many_form", "one2many_list"])
