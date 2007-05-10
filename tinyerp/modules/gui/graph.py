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

import os
import time
import base64
import tempfile

import matplotlib

matplotlib.use('Agg')  # force the antigrain backend
matplotlib.rcParams['xtick.labelsize'] = 10
matplotlib.rcParams['ytick.labelsize'] = 10

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.numerix import arange
import matplotlib.numerix as nx

from turbogears import expose
from turbogears import controllers

import cherrypy

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp.tinyres import TinyResource

from tinyerp.modules.utils import TinyDict
from tinyerp.modules.utils import TinyParent

class Graph(controllers.Controller, TinyResource):

    @expose(content_type="image/png")
    def default(self, width=400, height=400, b64=None):

        if not b64:
            raise common.error('no graph data!')

        data = base64.decodestring(b64)
        data = eval(data)

        dpi = 72
        w = int(width) / dpi
        h = int(height) / dpi

        axis = data['axis']
        axis_data = data['axis_data']
        kind = data['kind']
        values = data['values']

        figure = Figure(figsize=(w, h))
        subplot = figure.add_subplot(111)

        tinygraph(subplot, kind, axis, axis_data, values)

        canvas = FigureCanvas(figure)

        fo = tempfile.TemporaryFile()
        canvas.print_figure(fo, dpi=dpi, facecolor=None)
        fo.seek(0)
        fdata = fo.read()
        fo.close()

        return fdata

def tinygraph(subplot, type='pie', axis={}, axis_data={}, datas=[]):

    subplot.clear()

    operators = {
        '+': lambda x,y: x+y,
        '*': lambda x,y: x*y,
        'min': lambda x,y: min(x,y),
        'max': lambda x,y: max(x,y),
        '**': lambda x,y: x**y
    }
    for field in axis_data:
        group = axis_data[field].get('group', False)
        if group:
            keys = {}
            for d in datas:
                if d[field] in keys:
                    for a in axis:
                        if a<>field:
                            oper = operators[axis_data[a].get('operator', '+')]
                            keys[d[field]][a] = oper(keys[d[field]][a], d[a])
                else:
                    keys[d[field]] = d
            datas = keys.values()

    data = []
    for d in datas:
        res = []
        for x in axis:
            res.append(d[x])
        data.append(res)

    if not data:
        return False

    if type == 'pie':
        value = tuple([x[1] for x in data])
        labels = tuple([x[0] for x in data])
        subplot.pie(value, autopct='%1.1f%%')
        subplot.legend(labels, loc='lower right')

    elif type == 'bar':
        ind = arange(len(data))
        n = float(len(data[0])-1)
        for i in range(n):
            value = tuple([x[1+i] for x in data])
            labels = tuple([x[0] for x in data])
            subplot.set_xticks(ind)
            subplot.set_xticklabels(labels, visible=True, ha='left', rotation='vertical', va='bottom')
            subplot.bar(ind+i/n, value, 1/n)
    else:
        raise 'Graph type '+type+' does not exist !'
