###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
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
# along with this program; if not, write to the 
# Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
# Boston, MA  02111-1307, USA.
#
###############################################################################

from turbogears import controllers
from turbogears import expose
from turbogears import redirect
#from turbogears import widgets
#from turbogears import validators
from turbogears import validate
from turbogears import flash

from turbogears import widgets as tg_widgets
from turbogears import validators as tg_validators

import pkg_resources
import cherrypy

from tinyerp import rpc
#from tinyerp import cache
from tinyerp import common
from tinyerp.utils import TinyDict
from tinyerp.tinyres import TinyResource
from tinyerp import widgets as tw

from form import Form


#rpc.session = rpc.RPCSession('localhost', '8070', 'socket', storage=cherrypy.session)

class State(Form):
    
    path = '/workflow/state'    # mapping from root
    
    @expose(template="tinyerp.subcontrollers.templates.wkf_popup")
    def create(self, params, tg_errors=None):  
              
        params.path = self.path
        params.function = 'create_state'
        
        if params.id and cherrypy.request.path == self.path + '/view':
            params.load_counter = 2
        
        form = self.create_form(params, tg_errors)  
        
        field = form.screen.widget.get_widgets_by_name('wkf_id')[0]     
        field.set_value(params.wkf_id or False)
        field.readonly = True
         
        form.hidden_fields = [tg_widgets.HiddenField(name='wkf_id', default=params.wkf_id)]
        vals = getattr(cherrypy.request, 'terp_validators', {})
        vals['wkf_id'] = tw.validators.Int()
        
        hide = []
        
        hide += form.screen.widget.get_widgets_by_name('out_transitions')
        hide += form.screen.widget.get_widgets_by_name('in_transitions')
        hide += form.screen.widget.get_widgets_by_name('', kind=tw.form.Separator)
        
        for w in hide:
            w.visible = False

        return dict(form=form, params=params, show_header_footer=False)

    @expose()    
    def edit(self, **kw):
        
        params, data = TinyDict.split(kw)
        
        if not params.model:
            params.update(kw)
       
        params.view_mode = ['form']
        params.view_type = 'form'        
        params.editable = True
        
        return self.create(params)
    
    @expose()
    def delete(self, id, **kw):
        
        error_msg = None 
        
        proxy_act = rpc.RPCProxy('workflow.activity')
        proxy_tr =  rpc.RPCProxy('workflow.transition')
        
        search_ids = proxy_act.search([('id','=', int(id))], 0, 0, 0, rpc.session.context)
        data = proxy_act.read(search_ids[0], ['out_transitions', 'in_transitions', 'flow_start'], rpc.session.context)
        
            
        if data['flow_start']:
            error_msg = _("The activity which start the flow can not be deleted.")
        else:
            #all transitions which are connected to the activity
            trs = data['out_transitions']          

            for tr in data['in_transitions']:
                if not trs.__contains__(tr):
                    trs.append(tr)
            
            data_trs = proxy_tr.read(trs, ['act_from', 'act_to'], rpc.session.context)

            opp_side_act = []
            for tr in data_trs:
                act_from = tr['act_from'][0]
                act_to = tr['act_to'][0]
                
                if not opp_side_act.__contains__(act_from): 
                    opp_side_act.append(act_from)              
                
                if not opp_side_act.__contains__(act_to):
                    opp_side_act.append(act_to)
                    
            if opp_side_act:
                opp_side_act.remove(int(id))
            
            data_opp_acts = proxy_act.read(opp_side_act, ['out_transitions', 'in_transitions'], rpc.session.context)
      
            error_msg = None
            
            for act in data_opp_acts:
                act_tr = act['out_transitions'] + act['in_transitions']
                diff_list = []
                                
                for tr in act_tr:
                    if tr not in trs:
                        diff_list.append(tr)
                
                if not diff_list:
                    error_msg = _('Graph can not be made disconnected')                   
                    break;
                
            if not error_msg:
                res_tr = proxy_tr.unlink(trs)
                
                if res_tr:
                    res_act = proxy_act.unlink(int(id))                

                if not res_act:
                    error_msg = _('Could not delete state')
                    
        return dict(error = error_msg)
    
    @expose('json')
    def get_info(self, id, **kw):
        
        proxy_act = rpc.RPCProxy('workflow.activity')
        search_act = proxy_act.search([('id', '=', int(id))], 0, 0, 0, rpc.session.context)
        data = proxy_act.read(search_act, [], rpc.session.context)
    
        return dict(data=data[0])

class Connector(Form):
    
    path = '/workflow/connector'    # mapping from root
    
    @expose(template="tinyerp.subcontrollers.templates.wkf_popup")
    def create(self, params, tg_errors=None):
        
        params.path = self.path
        params.function = 'update_connection'
        
        if params.id and cherrypy.request.path == self.path + '/view':
            params.load_counter = 2
            
        form = self.create_form(params, tg_errors)
        
        field_act_from = form.screen.widget.get_widgets_by_name('act_from')[0]
        field_act_from.set_value(params.start or False)
        field_act_from.readonly = True
        
        field_act_to = form.screen.widget.get_widgets_by_name('act_to')[0]
        field_act_to.set_value(params.end or False)
        field_act_to.readonly = True
        
        form.hidden_fields = [tg_widgets.HiddenField(name='act_from', default=params.start),
                            tg_widgets.HiddenField(name='act_to', default=params.end)]
        
        vals = getattr(cherrypy.request, 'terp_validators', {})
        vals['act_from'] = tw.validators.Int()
        vals['act_to'] = tw.validators.Int()
        
        return dict(form=form, params=params, show_header_footer=False)
                
    @expose()    
    def edit(self, **kw):
        
        params, data = TinyDict.split(kw)
        
        if not params.model:
            params.update(kw)
            
        params.view_mode = ['form']
        params.view_type = 'form'
        params.editable = True
        
        return self.create(params)
    
    @expose('json')
    def delete(self, id, **kw):
        
        error_msg = None
        proxy_tr = rpc.RPCProxy('workflow.transition')
        search_tr = proxy_tr.search([('id', '=', int(id))], 0, 0, 0, rpc.session.context)
        transition = proxy_tr.read(search_tr[0], ['act_from', 'act_to'], rpc.session.context)        
        
        act_list = []
        act_list.append(transition['act_from'][0])
        
        #check for loop transaction 
        if not act_list.__contains__(transition['act_to'][0]):
            act_list.append(transition['act_to'][0]);
        
        
        proxy_act = rpc.RPCProxy('workflow.activity')
        search_act = proxy_act.search([('id', 'in', act_list)], 0, 0, 0, rpc.session.context)
        data_act = proxy_act.read(search_act, ['out_transitions', 'in_transitions'], rpc.session.context)       
       
        for act in data_act:
            d = []
            d+=act['out_transitions']
            d+=act['in_transitions']
            d.remove(int(id))  
            
            if not d:
                error_msg = _('Activity can not be made isolated')
                break
            
        if not error_msg:    
            res_tr = proxy_tr.unlink(search_tr)
        
        return dict(error=error_msg)
    
    @expose('json')
    def auto_create(self, act_from, act_to, **kw):
        
        proxy_tr = rpc.RPCProxy('workflow.transition')
        id = proxy_tr.create({'act_from': act_from, 'act_to': act_to})
        data = proxy_tr.read(id, [], rpc.session.context);
        
        if id>0:
            return dict(flag=True,data=data)
        else:
            return dict(flag=False)
    
    @expose('json')
    def get_info(self, id, **kw):
                
        proxy_tr = rpc.RPCProxy('workflow.transition')
        search_tr = proxy_tr.search([('id', '=', int(id))], 0, 0, 0, rpc.session.context)
        data = proxy_tr.read(search_tr, [], rpc.session.context)
        
        return dict(data=data[0])
    
    @expose('json')
    def change_ends(self, id, field, value):     
           
        proxy_tr = rpc.RPCProxy('workflow.transition')
        id = proxy_tr.write([int(id)], {field: int(value)}, rpc.session.context)
        return dict()


class Workflow(Form):
    
    path = '/workflow'
    
    @expose(template="tinyerp.subcontrollers.templates.workflow")
    def index(self, model, id=None):
        
        proxy = rpc.RPCProxy("workflow")
        if id:
            ids = proxy.search([('id', '=', id)], 0, 0, 0, rpc.session.context)
        else:
            ids = proxy.search([('osv', '=', model)], 0, 0, 0, rpc.session.context)
        
        if not ids:
            raise common.message(_('No workflow associated!'))
        
        wkf = proxy.read(ids, [], rpc.session.context)[0]
        return dict(wkf=wkf, show_header_footer=False)
    
    @expose('json')
    def get_info(self, id, **kw):
        
        proxy = rpc.RPCProxy("workflow")
        search_ids = proxy.search([('id', '=' , int(id))], 0, 0, 0, rpc.session.context) 
        graph_search = proxy.graph_get(search_ids[0], (140, 160, 20, 20), rpc.session.context) 
         
        nodes = graph_search['node']
        transitions = graph_search['transition']
        
        connectors = {}
        list_tr = [];
            
        for tr in transitions:
            list_tr.append(tr)
            t = connectors.setdefault(tr,{})
            t['id'] = tr
            t['s_id'] = transitions[tr][0]
            t['d_id'] = transitions[tr][1]
            
        proxy_tr = rpc.RPCProxy("workflow.transition")
        search_trs = proxy_tr.search([('id', 'in', list_tr)], 0, 0, 0, rpc.session.context)
        data_trs = proxy_tr.read(search_trs, ['signal', 'condition', 'act_from', 'act_to'], rpc.session.context)

        for tr in data_trs:
            t = connectors.get(tr['id'])
            t['signal'] = tr['signal']
            t['condition'] = tr['condition']
            t['source'] = tr['act_from'][1]
            t['destination'] = tr['act_to'][1]
        
        proxy_act = rpc.RPCProxy("workflow.activity")
        search_acts = proxy_act.search([('wkf_id', '=', int(id))], 0, 0, 0, rpc.session.context) 
        data_acts = proxy_act.read(search_acts, ['action', 'kind', 'flow_start', 'flow_stop', 'subflow_id'], rpc.session.context)
        
        for act in data_acts:
            n = nodes.get(str(act['id'])) 
            n['id'] = act['id']
            n['flow_start'] = act['flow_start']
            n['flow_stop'] = act['flow_stop']
            n['action'] = act['action']
            n['kind'] = act['kind']
            n['subflow_id'] = act['subflow_id']
            
        return dict(nodes=nodes,conn=connectors)
    
    state = State()
    connector = Connector()
    

class WorkflowList(controllers.Controller, TinyResource):

    @expose(template="tinyerp.subcontrollers.templates.wkf_list")
    def index(self, model, active=False):
        
        params = TinyDict()
        params.model = 'workflow'
        params.view_mode = ['tree']
        
        params.domain = [('osv', '=', model)]
        
        screen = tw.screen.Screen(params, selectable=1)
        screen.widget.pageable = False
        
        return dict(screen=screen, model=model, active=active, show_header_footer=False)
    
    @expose()
    def create(self, model, **kw):
        
        wkf_name = kw.get('name')
        on_create = kw.get('on_create')
        
        if not wkf_name:
            raise redirect('/workflowlist', model=model)
        
        proxy = rpc.RPCProxy('workflow')
        proxy.create(dict(osv=model, name=wkf_name, on_create=on_create))
        
        raise redirect('/workflowlist', model=model)
    
    @expose()
    def delete(self, model, id):
        
        id = int(id)
        
        proxy = rpc.RPCProxy('workflow')
        proxy.unlink(id)
        
        raise redirect('/workflowlist', model=model)
    
    @expose()
    def activate(self, model, id):
        
        activate_id = int(id)
        
        proxy = rpc.RPCProxy('workflow')
        search_ids = proxy.search([('osv', '=', model)], 0, 0, 0, rpc.session.context)
        
        for id in search_ids:
            if id==activate_id:                
                proxy.write([id], {'on_create': True})
            else:
                proxy.write([id], {'on_create': False})
                
        raise redirect('/workflowlist', model=model)
        
