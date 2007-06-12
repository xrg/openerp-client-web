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
from StringIO import StringIO
import pkg_resources

from turbogears import expose
from turbogears import controllers

import cherrypy

from tinyerp import rpc
from tinyerp import tools
from tinyerp import common

from tinyerp.tinyres import TinyResource
from tinyerp.tinygraph import tinygraph

from tinyerp.modules.utils import TinyDict
from tinyerp.modules.utils import TinyParent

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from PIL import Image as PILImage

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
        axis_group_field = data['axis_group_field']
        kind = data['kind']
        values = data['values']
        orientation = data['orientation']

        figure = Figure(figsize=(w, h), dpi=dpi, frameon=False)
        subplot = figure.add_subplot(111, axisbg='#eeeeee')
        
        if kind == 'bar':
            if orientation == 'vertical':
                figure.subplots_adjust(left=0.08,right=0.98,bottom=0.25,top=0.98)
            else:
                figure.subplots_adjust(left=0.20,right=0.97,bottom=0.07,top=0.98)
        else:
            figure.subplots_adjust(left=0.03,right=0.97,bottom=0.03,top=0.97)

        if not (values and tinygraph(subplot, kind, axis, axis_data, values, axis_group_field, orientation)):
            cherrypy.response.headers['Content-Type'] = "image/gif"
            return cherrypy.lib.cptools.serveFile(pkg_resources.resource_filename("tinyerp", "static/images/blank.gif"))

        canvas = FigureCanvas(figure)
        canvas.draw()

        size = canvas.get_renderer().get_canvas_width_height()
        try:
            buf = canvas.buffer_rgba(0, 0) # matplotlib-0.90
        except:
            buf = canvas.buffer_rgba() # matplotlib-0.82

        im=PILImage.frombuffer('RGBA', size, buf, 'raw', 'RGBA', 0, 1)

        imgdata=StringIO()
        im.save(imgdata, 'PNG')

        return imgdata.getvalue()
