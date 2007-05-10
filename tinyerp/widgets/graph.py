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

import base64
import xml.dom.minidom

import turbogears as tg
import cherrypy

from tinyerp import icons
from tinyerp import tools
from tinyerp import rpc

from interface import TinyCompoundWidget

class Graph(TinyCompoundWidget):

    template = """<table width="100%">
        <tr>
            <td align="center">
                <img class="graph" src="/graph?b64=${b64}"/>
            </td>
        </tr>
    </table>
    """

    params = ['b64']
    b64 = None

    def __init__(self, model, view, ids=[], domain=[], context={}):

        self.axis = None
        self.axis_data = None
        self.kind = 'pie'
        self.values = []

        self.fields = view['fields']

        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
        self.parse(root, self.fields)

        proxy = rpc.RPCProxy(model)

        if not ids:
            ids = proxy.search(domain)

        self.ids = ids

        ctx = rpc.session.context.copy()
        ctx.update(context)

        values = proxy.read(ids, self.fields.keys(), ctx)

        for value in values:
            res = {}
            for x in self.axis:
                if self.fields[x]['type'] in ('many2one', 'char','time','text','selection'):
                    res[x] = value[x]
                    if isinstance(res[x], (list, tuple)):
                        res[x] = res[x][-1]
                    res[x] = str(res[x])
                elif self.fields[x]['type'] == 'date':
                    date = time.strptime(value[x], DT_FORMAT)
                    res[x] = time.strftime(locale.nl_langinfo(locale.D_FMT).replace('%y', '%Y'), date)
                elif self.fields[x]['type'] == 'datetime':
                    date = time.strptime(value[x], DHM_FORMAT)
                    if 'tz' in rpc.session.context:
                        try:
                            import pytz
                            lzone = pytz.timezone(rpc.session.context['tz'])
                            szone = pytz.timezone(rpc.session.timezone)
                            dt = DT.datetime(date[0], date[1], date[2], date[3], date[4], date[5], date[6])
                            sdt = szone.localize(dt, is_dst=True)
                            ldt = sdt.astimezone(lzone)
                            date = ldt.timetuple()
                        except:
                            pass
                    res[x] = time.strftime(locale.nl_langinfo(locale.D_FMT).replace('%y', '%Y')+' %H:%M:%S', date)
                else:
                    res[x] = float(value[x])

            self.values.append(res)

        data = dict(axis=self.axis, axis_data=self.axis_data, kind=self.kind, values=self.values)
        self.b64 = base64.encodestring(ustr(data))

    def parse(self, root, fields):
        attrs = tools.node_attributes(root)
        self.string = attrs.get('string', 'Unknown')

        axis = []
        axis_data = {}
        for node in root.childNodes:
            node_attrs = tools.node_attributes(node)
            if node.localName == 'field':
                axis.append(str(node_attrs['name']))
                axis_data[str(node_attrs['name'])] = node_attrs

        self.axis = axis
        self.axis_data = axis_data
        self.kind = attrs.get('type', 'pie')
