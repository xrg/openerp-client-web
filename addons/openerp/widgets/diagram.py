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

import time
import math
import copy
import locale
import xml.dom.minidom

import cherrypy

from openobject import tools

from openobject.i18n import format
from openobject.widgets import CSSLink, JSLink

from openerp.utils import rpc
from openerp.utils import icons
from openerp.utils import common
from openerp.utils import expr_eval
from openerp.utils import node_attributes

import form

from pager import Pager

from openerp.widgets import TinyWidget
from openerp.widgets import TinyInputWidget
from openerp.widgets import ConcurrencyInfo

from openerp.widgets import get_widget
from openerp.widgets import register_widget


class Diagram(TinyWidget):
    
    template = "templates/diagram.mako"
    member_widgets = []
    
    params = ['dia_id', 'node', 'connector', 'src_node', 'des_node']
    
    pager = None
    dia_id = None
    node = ''
    connector = ''
    src_node = ''
    des_node = ''
    node_attrs = []
    conn_attrs = []
    
    css = [CSSLink("openerp", 'workflow/css/graph.css')]
    javascript = [JSLink("openerp", 'workflow/javascript/draw2d/wz_jsgraphics.js'),
                  JSLink("openerp", 'workflow/javascript/draw2d/mootools.js'),
                  JSLink("openerp", 'workflow/javascript/draw2d/moocanvas.js'),
                  JSLink("openerp", 'workflow/javascript/draw2d/draw2d.js'),
                  JSLink("openerp", 'workflow/javascript/connector.js'),
                  JSLink("openerp", 'workflow/javascript/conn_anchor.js'),
                  JSLink("openerp", 'workflow/javascript/conn_decorator.js'),
                  JSLink("openerp", 'workflow/javascript/workflow.js'),
                  JSLink("openerp", 'workflow/javascript/toolbar.js'),
                  JSLink("openerp", 'workflow/javascript/ports.js'),
                  JSLink("openerp", 'workflow/javascript/state.js'),
                  JSLink("openerp", 'workflow/javascript/infobox.js')]
    
    def __init__(self, name, model, view, ids=[], domain=[], context={}, **kw):
        
        super(Diagram, self).__init__(name=name, model=model, ids=ids)
        print '==================================='
        print 'view=====================',view
        print 'ids=====================',ids
        
        if ids:
            self.dia_id = ids[0]
            
        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
        attrs = node_attributes(root)
        
        self.string = attrs.get('string')
        
        self.parse(root)
        
    def parse(self, root):
        elm = None        
        
        for node in root.childNodes: 
            if node.nodeName == 'node':
                attrs = node_attributes(node)
                self.node = attrs['object']
            elif node.nodeName == 'arrow':
                attrs = node_attributes(node)
                self.connector = attrs['object']
                self.src_node = attrs['source']
                self.des_node = attrs['destination']
        
                
                