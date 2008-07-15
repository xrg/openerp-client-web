////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
//
// $Id$
//
// Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
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

var form_hookAttrChange = function() {
    
    var items = [];
    
    items = items.concat(getElementsByTagAndClassName('td', 'item'));
    items = items.concat(getElementsByTagAndClassName('td', 'label'));
    items = items.concat(getElementsByTagAndClassName('div', 'tabbertab'));
    
    items = MochiKit.Base.filter(function(e){
        return getNodeAttribute(e, 'attrs');
    }, items);
	
	var fields = {};
	
	forEach(items, function(e){
		
		var attrs = getNodeAttribute(e, 'attrs') || '{}';
		var widget = getNodeAttribute(e, 'widget') || '';
		var container = e;
		var prefix = widget.slice(0, widget.lastIndexOf('/')+1);
		
		// convert into Python statement into it's equivalent in JS
		attrs = attrs.replace(/\(/g, '[');
		attrs = attrs.replace(/\)/g, ']');
		attrs = attrs.replace(/True/g, '1');
		attrs = attrs.replace(/False/g, '0');
		
		try {
		    eval('attrs='+attrs);
		} catch(e){
			return;
		}
		
		for (var attr in attrs) {
			forEach(attrs[attr], function(n){
				var field = MochiKit.DOM.getElement(prefix ? prefix + '/' + n[0] : n[0]);
				if (field) {
					fields[field.id] = 1;
					MochiKit.Signal.connect(field, 'onchange', partial(form_onAttrChange, container, widget, attr, attrs[attr]));
				}
			});
		}
	});
	
	for(var field in fields) {
		MochiKit.Signal.signal(field, 'onchange');
	}
}

var form_onAttrChange = function(container, widget, attr, expr, evt) {
	
	var prefix = widget.slice(0, widget.lastIndexOf('/')+1);
	var result = form_evalExpr(prefix, expr);
	
	if (attr == 'readonly')
	   form_setReadonly(container, widget, result)
	
	if (attr == 'required')
	   form_setRequired(container, widget, result)
	
	if (attr == 'invisible')
	   form_setVisible(container, widget, !result)
}

var form_evalExpr = function(prefix, expr) {
	
	var result = false;
	
	for(var i=0; i<expr.length; i++) {
		var ex = expr[i];
		var elem = MochiKit.DOM.getElement(prefix ? prefix + '/' + ex[0] : ex[0]);
		if (!elem) continue;
		
		var op = ex[1];
		var val = ex[2];
		
		switch (op) {
			
			case '=':
			case '==':
			    result = result || (elem.value == val);
			    break;
		    case '!=':
			case '<>':
			    result = result || (elem.value != val);
				break;
			case '<':
                result = result || (elem.value < val);
                break;
			case '>':
                result = result || (elem.value > val);
                break;
			case '<=':
                result = result || (elem.value <= val);
                break;
			case '>=':
                result = result || (elem.value >= val);
                break;
		}
	}
	
	return result;
}

var form_setReadonly = function(container, field, readonly) {
	field.disabled = readonly;
	if (readonly) {
		MochiKit.DOM.addElementClass(field, 'readonlyfield');
	} else {
		MochiKit.DOM.removeElementClass(field, 'readonlyfield');
	}
}

var form_setRequired = function(container, field, required) {
    
	if (required) {
	   MochiKit.DOM.addElementClass(field, 'requiredfield');	
	} else {
	   MochiKit.DOM.removeElementClass(field, 'requiredfield');	
	   MochiKit.DOM.removeElementClass(field, 'errorfield');
	}
}

var form_setVisible = function(container, field, visible) {
	
	if (field && field.tagName == 'BUTTON') {
	   field.style.display = visible ? '' : 'none';
	   
	} else if (container && MochiKit.DOM.hasElementClass(container, 'tabbertab')) { // notebook page?
	
        var tabber = container.parentNode.tabber;
        
        if (!tabber)  {
           return MochiKit.Async.callLater(0, form_setVisible, container, field, visible);
        }

        var tabs = getElementsByTagAndClassName('div', 'tabbertab', container.parentNode);
        var idx = findIdentical(tabs, container);
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
        
        tab.li.style.display = visible ? '' : 'none';
        tab.div.style.display = visible ? '' : 'none';
		
	} else {
	   container.style.display = visible ? '' : 'none';	
	}
}

MochiKit.DOM.addLoadEvent(function(evt){
	
    if (MochiKit.DOM.getElement('state')) {
        form_hookStateChange();
        form_onStateChange();
    }
	
	form_hookAttrChange();
});

// vim: sts=4 st=4 et
