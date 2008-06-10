###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
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
from turbogears import widgets
from turbogears import validators
from turbogears import validate
from turbogears import flash

from turbogears import widgets as tg_widgets
from turbogears import validators as tg_validators

import pkg_resources
import cherrypy

from tinyerp import rpc
from tinyerp import cache
from tinyerp import common
from tinyerp import widgets as tw

from form import Form
from tinyerp.utils import TinyDict


rpc.session = rpc.RPCSession('localhost', '8070', 'socket', storage=cherrypy.session)

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
    def delete(self,**kw):
        
        error_msg = None 
        
        proxy_act = rpc.RPCProxy(kw['model'])
        search_ids = proxy_act.search([('id','=', int(kw['id']))], 0, 0, 0, rpc.session.context)
        data = proxy_act.read(search_ids[0], ['out_transitions', 'in_transitions', 'flow_start'], rpc.session.context)
        
        
        if data['flow_start']:
            error_msg = _("The activity which start the flow can not be deleted.")
        else:
            trs = data['out_transitions']
            
            for tr in data['in_transitions']:
                if not trs.__contains__(tr):
                    trs.append(tr)
            
            proxy_tr =  rpc.RPCProxy('workflow.transition')
            res_tr = proxy_tr.unlink(trs)
            
            if res_tr:
                res_act = proxy_act.unlink(int(kw['id']))                

            if not res_act:
                error_msg = _('Could not delete state')
                
        return dict(error = error_msg)
    
    @expose('json')
    def get_info(self,**kw):
                
        proxy_act = rpc.RPCProxy('workflow.activity')
        search_act = proxy_act.search([('id', '=', int(kw['id']))], 0, 0, 0, rpc.session.context)
        data = proxy_act.read(search_act, [], rpc.session.context)
    
        return dict(data=data[0])

class Connector(Form):
    
    path = '/workflow/connector'    # mapping from root
    
    @expose(template="tinyerp.subcontrollers.templates.wkf_popup")
    def create(self, params, tg_errors=None):
        
        params.path = self.path
        params.function = 'update_conn'
        
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
    
    @expose()
    def delete(self,**kw):
        
        error_msg = None
        proxy_tr = rpc.RPCProxy(kw['model'])
        search_tr = proxy_tr.search([('id', '=', int(kw['id']))], 0, 0, 0, rpc.session.context)
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
            d.remove(int(kw['id']))  
            
            if not d:
                error_msg = _('Activity can not be made isolated')
                break
            
        if not error_msg:    
            res_tr = proxy_tr.unlink(search_tr)
        
        return dict(error=error_msg)
    
    @expose('json')
    def auto_create(self,**kw):
        
        proxy_tr = rpc.RPCProxy('workflow.transition')
        id = proxy_tr.create({'act_from': kw['act_from'], 'act_to': kw['act_to']})
        data = proxy_tr.read(id, [], rpc.session.context);
        
        if id>0:
            return dict(flag=True,data=data)
        else:
            return dict(flag=False)
    
    @expose('json')
    def get_info(self,**kw):
                
        proxy_tr = rpc.RPCProxy('workflow.transition')
        search_tr = proxy_tr.search([('id', '=', int(kw['id']))], 0, 0, 0, rpc.session.context)
        data = proxy_tr.read(search_tr, [], rpc.session.context)
        
        return dict(data=data[0])
    
    @expose('json')
    def change_ends(self,**kw):     
           
        proxy_tr = rpc.RPCProxy('workflow.transition')
        id = proxy_tr.write([int(kw['id'])], {kw['field']:int(kw['value'])}, rpc.session.context)
        return dict()


class Workflow(Form):
    
    path = '/workflow'
    
    @expose(template="tinyerp.subcontrollers.templates.workflow")
    def index(self, model):
        
        proxy = rpc.RPCProxy("workflow")
        ids = proxy.search([('osv', '=', model)], 0, 0, 0, rpc.session.context)
        
        if not ids:
            raise common.message(_('No workflow associated!'))
        
        wkf = proxy.read(ids, [], rpc.session.context)[0]
        return dict(wkf=wkf, show_header_footer=False)
    
    @expose()
    def get_info(self, **kw):
        
        proxy = rpc.RPCProxy("workflow")
        search_ids = proxy.search([('id', '=' , int(kw['id']))], 0, 0, 0, rpc.session.context) 
        graph_search = proxy.graph_get(search_ids[0], (200, 200, 20, 20), rpc.session.context) 
         
        nodes = graph_search['node']
        transitions = graph_search['transition']
        
        connectors = {}
        list_tr = [];
            
        for tr in transitions:
            list_tr.append(tr)
            t = connectors.setdefault(tr,{})
            t['id'] = tr
            t['c'] = transitions[tr]
            
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
        search_acts = proxy_act.search([('wkf_id', '=', int(kw['id']))], 0, 0, 0, rpc.session.context) 
        data_acts = proxy_act.read(search_acts, ['action', 'kind', 'flow_start', 'flow_stop'], rpc.session.context)
        
        for act in data_acts:
            n = nodes.get(str(act['id'])) 
            n['id'] = act['id']
            n['flow_start'] = act['flow_start']
            n['flow_stop'] = act['flow_stop']
            n['action'] = act['action']
            n['kind'] = act['kind']
        print nodes
        return dict(list=nodes,conn=connectors)
    
    @expose(template="tinyerp.subcontrollers.templates.wkf_popup")
    def create(self, params, tg_errors=None):

        if params.id and cherrypy.request.path == '/workflow/view':
            params.load_counter = 2
            
        params.path = self.path
        params.function = 'create_wkf'
        
        form = self.create_form(params, tg_errors)
        
        return dict(form=form, params=params, show_header_footer=False)

    @expose()
    def edit(self,**kw):
        
        params, data = TinyDict.split(kw)
        if not params.model:
            params.update(kw)
       
        params.view_mode = ['form']
        params.view_type = 'form'
        
        params.editable = True
        
        return self.create(params)
    
    state = State()
    connector = Connector()


