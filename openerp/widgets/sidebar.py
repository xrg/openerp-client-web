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

from turbogears import widgets

from openerp import rpc
from openerp import tools
from openerp.utils import TinyDict

from screen import Screen
from interface import TinyCompoundWidget

class Sidebar(TinyCompoundWidget):

    template = "openerp.widgets.templates.sidebar"
    params = ['reports', 'actions', 'relates', 'attachments']
    
    javascript = [widgets.JSSource("""
        function toggle_sidebar(forced) {
        
            var sb = MochiKit.DOM.getElement('sidebar');
            var sbp = MochiKit.DOM.getElement('sidebar_pane');

            sb.style.display = forced ? forced : (sb.style.display == "none" ? "" : "none");
            sbp.style.display = sb.style.display;

            set_cookie("terp_sidebar", sb.style.display);

            var img = MochiKit.DOM.getElementsByTagAndClassName('img', null, 'sidebar_hide')[0];
            if (sb.style.display == "none")
                img.src = '/static/images/sidebar_show.gif';
            else
                img.src = '/static/images/sidebar_hide.gif';
        }
        
        MochiKit.DOM.addLoadEvent(function(evt) {
            var sb = MochiKit.DOM.getElement('sidebar');
            if (sb) toggle_sidebar(get_cookie('terp_sidebar'));
        });    
    """)]
    
    def __init__(self, model, toolbar=None, id=None, view_type="form", multi=True, is_tree=False, context={}):
        
        super(Sidebar, self).__init__()
        
        self.model = model
        self.multi = multi
        self.context = context
        self.view_type = view_type
        
        toolbar = toolbar or {}
        
        self.reports = toolbar.get('print', [])
        self.actions = toolbar.get('action', [])
        self.relates = toolbar.get('relate', [])
        
        self.attachments = []
        
        proxy = rpc.RPCProxy('ir.values')
        
        if not self.actions:
            
            act = 'client_action_multi'
            if is_tree:
                act = 'tree_but_action'
            
            res = []
            try: # Deal with `You try to bypass an access rule`
                res = proxy.get('action', act, [(self.model, False)], False, self.context)
            except:
                pass

            actions = [a[-1] for a in res]
            self.actions = [a for a in actions if self.multi or not a.get('multi')]
            
        if not self.reports:
            res = []
            try:
                res = proxy.get('action', 'client_print_multi', [(self.model, False)], False, self.context)
            except:
                pass

            actions = [a[-1] for a in res]
            self.reports = [a for a in actions if self.multi or not a.get('multi')]
        
        
        if self.view_type == 'form':
            id = int(id)
            params = TinyDict()
            params.model = 'ir.attachment'
            params.view_mode = ['tree', 'form']
    
            params.domain = [('res_model', '=', model), ('res_id', '=', id)]
            screen = Screen(params, selectable=1)
            ids = screen.ids or []
            
            proxy = rpc.RPCProxy('ir.attachment')
            if ids:
                for i in ids:
                    attach = []
                    datas = proxy.read([i], ['datas_fname'])
                    attach += [datas[0].get('id')]
                    attach += [datas[0].get('datas_fname', '')]
                    if datas[0].get('datas_fname'):
                        self.attachments += [attach]
                    
# vim: ts=4 sts=4 sw=4 si et

