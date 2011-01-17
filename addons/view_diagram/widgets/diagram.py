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
import xml.dom.minidom

from openobject.widgets import CSSLink, JSLink
from openerp.utils import node_attributes
from openerp.widgets import TinyWidget


class Diagram(TinyWidget):

    template = "/view_diagram/widgets/templates/diagram.mako"
    member_widgets = []

    params = ['dia_id', 'node', 'connector', 'src_node', 'des_node',
              'node_flds', 'conn_flds', 'bgcolor', 'shapes',
              'node_flds_string', 'conn_flds_string']

    pager = None
    dia_id = None
    node = ''
    connector = ''
    src_node = ''
    des_node = ''
    node_flds = {}
    conn_flds = []
    bgcolor = {}
    shapes = {}
    node_flds_string = []
    conn_flds_string = []

    css = [CSSLink("view_diagram", 'css/graph.css')]
    javascript = [JSLink("view_diagram", 'javascript/draw2d/wz_jsgraphics.js'),
                  JSLink("view_diagram", 'javascript/draw2d/mootools.js'),
                  JSLink("view_diagram", 'javascript/draw2d/moocanvas.js'),
                  JSLink("view_diagram", 'javascript/draw2d/draw2d.js'),
                  JSLink("view_diagram", 'javascript/connector.js'),
                  JSLink("view_diagram", 'javascript/conn_anchor.js'),
                  JSLink("view_diagram", 'javascript/conn_decorator.js'),
                  JSLink("view_diagram", 'javascript/workflow.js'),
                  JSLink("view_diagram", 'javascript/ports.js'),
                  JSLink("view_diagram", 'javascript/state.js'),
                  JSLink("view_diagram", 'javascript/infobox.js')]

    def __init__(self, name, model, view,
                 ids=None, domain=None, context=None, **kw):
        super(Diagram, self).__init__(name=name, model=model, ids=ids)

        if ids:
            self.dia_id = ids[0]

        dom = xml.dom.minidom.parseString(view['arch'].encode('utf-8'))
        root = dom.childNodes[0]
        attrs = node_attributes(root)

        self.string = attrs.get('string')

        self.parse(root, view['fields'])

    def parse(self, root, fields):
        self.node_flds['visible'] = []
        self.node_flds['invisible'] = []

        for node in root.childNodes:
            if node.nodeName == 'node':
                attrs = node_attributes(node)
                self.node = attrs['object']
                self.bgcolor = attrs.get('bgcolor', '')
                self.shapes = attrs.get('shape', '')

                for fld in node.childNodes:
                    if fld.nodeName == 'field':
                        attrs = node_attributes(fld)
                        name = attrs['name']
                        if attrs.has_key('invisible') and attrs['invisible']=='1':
                            self.node_flds['invisible'].append(name)
                        else:
                            self.node_flds['visible'].append(name)
                            self.node_flds_string.append(fields[name].get('string', name.title()))
            elif node.nodeName == 'arrow':
                attrs = node_attributes(node)
                self.connector = attrs['object']
                self.src_node = attrs['source']
                self.des_node = attrs['destination']

                for fld in node.childNodes:
                    if fld.nodeName == 'field':
                        name = node_attributes(fld)['name']
                        self.conn_flds_string.append(fields[name].get('string', name.title()))
                        self.conn_flds.append(str(name))
