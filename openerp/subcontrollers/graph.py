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

import os
import time
import math
import pkg_resources

from StringIO import StringIO

from turbogears import expose
from turbogears import controllers

import cherrypy

from openerp import rpc
from openerp import tools
from openerp import common

from openerp.tinyres import TinyResource
from openerp.utils import TinyDict
from openerp.widgets.graph import GraphData

class Graph(controllers.Controller, TinyResource):

    @expose('json')
    def pie(self, **kw):
                                
        params, data = TinyDict.split(kw)
        data = GraphData(params.model, params.view_id, params.ids, params.domain, params.context)
        
        return dict(data=data.get_pie_data())
        
    @expose('json')
    def bar(self, **kw):
        
        params, data = TinyDict.split(kw)
        data = GraphData(params.model, params.view_id, params.ids, params.domain, params.context)
        
        return dict(data=data.get_bar_data())
    
# vim: ts=4 sts=4 sw=4 si et

