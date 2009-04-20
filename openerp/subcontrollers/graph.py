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
import base64
import cherrypy

from openerp.tools import expose

from openerp.tinyres import TinyResource
from openerp.utils import TinyDict

from openerp.widgets.graph import BarChart
from openerp.widgets.graph import PieChart

class Graph(TinyResource):

    @expose('json')
    def pie(self, args):

        kw = base64.decodestring(args)
        kw = eval(kw)

        params, data = TinyDict.split(kw)
        data = PieChart(params.model, params.view_id, params.ids, params.domain, params.context)

        return data.get_data()

    @expose('json')
    def bar(self, args):

        kw = base64.decodestring(args)
        kw = eval(kw)

        params, data = TinyDict.split(kw)
        data = BarChart(params.model, params.view_id, params.ids, params.domain, params.context)

        return data.get_data()

# vim: ts=4 sts=4 sw=4 si et

