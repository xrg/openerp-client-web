////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://openerp.com) All Rights Reserved.
//
// $Id$
//
// WARNING: This program as such is intended to be used by professional
// programmers who take the whole responsibility of assessing all potential
// consequences resulting from its eventual inadequacies and bugs
// End users who are looking for a ready-to-use solution with commercial
// guarantees and support are strongly advised to contract a Free Software
// Service Company
//
// This program is Free Software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the 
// Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
// Boston, MA  02111-1307, USA.
//
////////////////////////////////////////////////////////////////////////////////

var FORM_STATE_INFO = [];

var form_hookStateChange = function() {
    
    var items = [];
    
    items = items.concat(getElementsByTagAndClassName('td', 'item'));
    items = items.concat(getElementsByTagAndClassName('td', 'label'));
    items = items.concat(getElementsByTagAndClassName('div', 'tabbertab'));
    
    items = MochiKit.Base.filter(function(e){
        return getNodeAttribute(e, 'states');
    }, items);
    
    FORM_STATE_INFO = items;
    MochiKit.Signal.connect('state', 'onchange', form_onStateChange);   
}

var form_onStateChange = function(evt) {
    
    var val = MochiKit.DOM.getElement('state').value;
    
    for(var i=0; i<FORM_STATE_INFO.length; i++) {
            
        var item = FORM_STATE_INFO[i];
        var states = getNodeAttribute(item, 'states');
        states = states.split(',');
        
        // notebook page?
        if (item.tagName == 'DIV') {
            
            var tabber = item.parentNode.tabber;
            
            if (!tabber)  {
               return MochiKit.Async.callLater(0, form_onStateChange, evt);
            }
            
            if (tabber) {
                var tabs = getElementsByTagAndClassName('div', 'tabbertab', item.parentNode);
                var idx = findIdentical(tabs, item);
                var idx2 = -1;
                
                var tab = tabber.tabs[idx];
                
                if (hasElementClass(tab.li, 'tabberactive') && tab.li.style.display != 'none' && tabs.length > 1) {
                    
                    for (var j=idx-1; j>-1;j--){                        
                        if (idx2 > -1) 
                            break;
                        if (tabs[j].style.display != 'none')
                            idx2 = j;
                    }
                    
                    for (var j=idx+1; j<tabs.length; j++){                        
                        if (idx2 > -1) 
                            break;
                        if (tabs[j].style.display != 'none')
                            idx2 = j;
                    }
                    
                    if (idx2 > -1) {
                        tabber.tabShow(idx2);
                    }
                }
                
                tab.li.style.display = findIdentical(states, val) == -1 ? 'none' : '';
                tab.div.style.display = findIdentical(states, val) == -1 ? 'none' : '';
            }
        } else {
            item.style.display = findIdentical(states, val) == -1 ? 'none' : '';
        }
    }
}

MochiKit.DOM.addLoadEvent(function(evt){
    if (MochiKit.DOM.getElement('state')) {
        form_hookStateChange();
        form_onStateChange();
    }
});

// vim: sts=4 st=4 et
