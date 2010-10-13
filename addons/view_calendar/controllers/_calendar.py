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

import time
import math

import cherrypy

from openobject.tools import expose
from openobject.i18n import format

from openerp.utils import rpc, TinyDict, context_with_concurrency_info

from openerp.controllers.form import Form

from view_calendar import widgets as tc

class TinyCalendar(Form):

    _cp_path = "/view_calendar/calendar"

    @expose()
    def mini(self, year, month, forweek=False):
        params = TinyDict()

        params.year = year
        params.month = month
        params.forweek = forweek

        day = tc.utils.Day(params.year, params.month, 1)
        minical = tc.widgets.MiniCalendar(day, forweek=params.forweek, highlight=False)

        return minical.render()

    @expose('json')
    def get(self, day, mode, **kw):

        params, data = TinyDict.split(kw)
        
        options = TinyDict()
        options.selected_day = params.selected_day

        day = time.strptime(day, '%Y-%m-%d')

        options.year = day[0]
        options.month = day[1]

        options.date1 = day
        options.mode = mode
        
        if params.colors:
            try:
                options.colors = eval(kw['_terp_colors'])
            except:
                pass

        if params.color_values:
            options.color_values = ustr(params.color_values).split(',')

        options.search_domain = params.search_domain or []
        options.use_search = params.use_search
        if params.get('_terp_color_filters'):
            options.color_filters = params.color_filters
        params.kalendar = options

        form = self.create_form(params)
        
        return dict(
            calendar=ustr(form.screen.widget.render()),
            sidebar=ustr(form.sidebar.render()))

    @expose('json', methods=('POST',))
    def delete(self, **kw):

        params, data = TinyDict.split(kw)

        error = None

        ctx = rpc.session.context.copy()
        ctx.update(params.context or {})
        ctx = context_with_concurrency_info(ctx, params.concurrency_info)

        proxy = rpc.RPCProxy(params.model)

        try:
            proxy.unlink([params.id], ctx)
        except Exception, e:
            error = ustr(e)

        return dict(error=error)

    @expose('json', methods=('POST',))
    def save(self, **kw):
        params, data = TinyDict.split(kw)

        data = {}
        ds = tc.utils.parse_datetime(params.starts)
        de = tc.utils.parse_datetime(params.ends)

        data[params.fields['date_start']['name']] = format.parse_datetime(ds.timetuple())

        if 'date_stop' in params.fields:
            data[params.fields['date_stop']['name']] = format.parse_datetime(de.timetuple())
        elif 'date_delay' in params.fields:
            # convert the end time in hours
            day_length = params.fields['day_length']

            tds = time.mktime(ds.timetuple())
            tde = time.mktime(de.timetuple())

            n = (tde - tds) / (60 * 60)

            if n > day_length:
                d = math.floor(n / 24)
                h = n % 24

                n = d * day_length + h

            data[params.fields['date_delay']['name']] = n

        ctx = dict(rpc.session.context,
                   **(params.context or {}))
        ctx = context_with_concurrency_info(ctx, params.concurrency_info)

        error = None
        proxy = rpc.RPCProxy(params.model)

        try:
            proxy.write([params.id], data, ctx)
            info = proxy.read([params.id], ['__last_update'])[0]['__last_update']
            info = {'%s,%s'%(params.model, params.id): info}
        except Exception, e:
            error = ustr(e)

        return dict(error=error, info=info)

    @expose('json')
    def duplicate(self, **kw):
        params, data = TinyDict.split(kw)

        id = params.id
        ctx = params.context
        model = params.model

        proxy = rpc.RPCProxy(model)
        try:
            new_id = proxy.copy(id, {}, ctx)
        except Exception:
            pass

        return dict(id=new_id)

    def _get_gantt_records(self, model, ids=None, group=None):

        if group:
            return [{
                'id': group['id'],
                'items': {'name': group['title']},
                'action': None,
                'target': None,
                'icon': None,
                'children': self._get_gantt_records(model, group['items'])
            }]

        proxy = rpc.RPCProxy(model)
        ctx = dict(rpc.session.context)

        records = []
        for id in ids:
            records.append({
                'id': id,
                'items': {'name': proxy.name_get([id], ctx)[0][-1]},
                'action': 'javascript: void(0)',
                'target': None,
                'icon': None,
                'children': None
            })

        return records

    @expose('json')
    def gantt_data(self, **kw):
        params, data = TinyDict.split(kw)
        records = []

        if params.groups:
            for group in params.groups:
                records.extend(self._get_gantt_records(params.model, None, group))
        else:
            records = self._get_gantt_records(params.model, params.ids or [])

        return dict(records=records)

    @expose('json', methods=('POST',))
    def gantt_reorder(self, **kw):
        params, data = TinyDict.split(kw)

        id = params.id
        ids = params.ids or []
        model = params.model
        level = params.level
        level_value = params.level_value

        proxy = rpc.RPCProxy(model)
        fields = proxy.fields_get([])

        if id and level and level_value:
            try:
                proxy.write([id], {level['link']: level_value})
            except Exception, e:
                return dict(error=ustr(e))

        if 'sequence' not in fields:
            return dict(error=None)

        res = proxy.read(ids, ['sequence'])

        sequence = [r['sequence'] for r in res]
        sequence.sort()

        sequence2 = []
        for seq in sequence:
            if seq not in sequence2:
                sequence2.append(seq)
            else:
                sequence2.append(sequence2[-1]+1)

        for n, id in enumerate(ids):
            seq = sequence2[n]
            try:
                proxy.write([id], {'sequence': seq})
            except Exception, e:
                return dict(error=ustr(e))

        return dict()

class CalendarPopup(Form):

    _cp_path = "/view_calendar/calpopup"

    @expose(template="/view_calendar/controllers/templates/calpopup.mako")
    def create(self, params, tg_errors=None):
        params.editable = True

        if params.id and cherrypy.request.path_info == '/view_calendar/calpopup/view':
            params.load_counter = 2

        form = self.create_form(params, tg_errors)
        return dict(form=form, params=params)

    @expose('json')
    def get_defaults(self, **kw):
        params, data = TinyDict.split(kw)
        data = {}

        ds = tc.utils.parse_datetime(params.starts)
        de = tc.utils.parse_datetime(params.ends)

        if 'date_stop' in params.fields:
            kind = params.fields['date_stop']['kind']
            data[params.fields['date_stop']['name']] = format.format_datetime(de.timetuple(), kind)

        elif 'date_delay' in params.fields:
            # convert the end time in hours
            day_length = params.fields['day_length']

            tds = time.mktime(ds.timetuple())
            tde = time.mktime(de.timetuple())

            n = (tde - tds) / (60 * 60)

            if n > day_length:
                d = math.floor(n / 24)
                h = n % 24

                n = d * day_length + h

            data[params.fields['date_delay']['name']] = n

        kind = params.fields['date_start']['kind']
        data[params.fields['date_start']['name']] = format.format_datetime(ds.timetuple(), kind)

        return data
