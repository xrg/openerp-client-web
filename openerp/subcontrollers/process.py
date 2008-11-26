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

from turbogears import controllers
from turbogears import expose
from turbogears import redirect

import cherrypy

from openerp import rpc
from openerp import common
from openerp import format

from openerp.utils import TinyDict
from openerp.tinyres import TinyResource

import form
import actions

class ResourcePopup(form.Form):
    
    path = '/process/resource'    # mapping from root
    
    @expose(template="openerp.subcontrollers.templates.process_open")
    def create(self, params, tg_errors=None):
        params.editable = True

        if params.id and cherrypy.request.path == self.path + '/view':
            params.load_counter = 2

        form = self.create_form(params, tg_errors)       
        return dict(form=form, params=params, show_header_footer=False)   

class Process(controllers.Controller, TinyResource):

    resource = ResourcePopup()
    
    @expose(template="openerp.subcontrollers.templates.process")
    def default(self, id=False, res_model=None, res_id=False):

        id = (id or False) and int(id)
        res_id = int(res_id)

        title = _("Select Workflow")
        selection = None

        proxy = rpc.RPCProxy('process.process')
        if id:
            res = proxy.read([id], ['name'], rpc.session.context)[0]
            title = res['name']
        else:
            selection = proxy.search_by_model(res_model, rpc.session.context)
            if len(selection):
                id, title = selection[0]
            else:
                raise common.message(_("Process not found for the given resource."))

        return dict(id=id, res_model=res_model, res_id=res_id, title=title)
    
    @expose('json')
    def get(self, id, res_model=None, res_id=False):

        id = int(id)
        res_id = int(res_id)

        proxy = rpc.RPCProxy('process.process')
        graph = proxy.graph_get(id, res_model, res_id, (80, 80, 150, 100), rpc.session.context)

        related = proxy.search_by_model(res_model, rpc.session.context) or {}
        graph['related'] = dict(related)

        # last modified by
        perm = graph['perm']
        perm['text'] = _("Last modified by:")

        # formate datetime
        try:
            perm['date'] = format.format_datetime(perm['write_date'] or perm['create_date'])
        except:
            pass

        for nid, node in graph['nodes'].items():
            if not node.get('res'):
                continue

            perm = node['res']['perm']
            perm['text'] = _("Last modified by:")

            # formate datetime
            try:
                perm['date'] = format.format_datetime(perm['write_date'] or perm['create_date'])
            except:
                pass

        return graph

    @expose('json')
    def action(self, **kw):
        params, data = TinyDict.split(kw)
        
        button = TinyDict()
        
        button.model = params.model
        button.id = params.id
        button.name = params.action
        button.btype = params.kind
        
        params.button = button

        fobj = form.Form()

        error = ""
        try:
            res = fobj.button_action(params)
        except Exception, e:
            error = str(e)

        return dict(error=error)

    @expose(content_type='application/pdf')
    def print_workflow(self, id, model):
        return actions.execute_report("workflow.instance.graph", ids=[], id=int(id), model=model, nested=False)

# vim: ts=4 sts=4 sw=4 si et

