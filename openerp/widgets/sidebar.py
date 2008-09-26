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
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from turbogears import widgets

from openerp import rpc
from openerp import tools

from interface import TinyCompoundWidget

class Sidebar(TinyCompoundWidget):

    template = "openerp.widgets.templates.sidebar"
    params = ['reports', 'actions', 'relates']
    
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
    
    def __init__(self, model, toolbar=None, multi=True, is_tree=False, context={}):
        
        super(Sidebar, self).__init__()
        
        self.model = model
        self.multi = multi
        self.context = context
        
        toolbar = toolbar or {}
        
        self.reports = toolbar.get('print', [])
        self.actions = toolbar.get('action', [])
        self.relates = toolbar.get('relate', [])
        
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
            
# vim: ts=4 sts=4 sw=4 si et

