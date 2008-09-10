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
    
    var elem = MochiKit.DOM.getElement('state');
    var val = elem.value || getNodeAttribute(elem, 'value') || elem.innerHTML;

    for(var i=0; i<FORM_STATE_INFO.length; i++) {
            
        var item = FORM_STATE_INFO[i];
        var states = getNodeAttribute(item, 'states');
        states = states.split(',');
        
        form_setVisible(item, null, findIdentical(states, val) > -1);
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
        
        // Convert Python statement into it's equivalent in JavaScript.
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
            var expr_fields = {}; // check if field appears more then once in the expr
            forEach(attrs[attr], function(n){
                var name = prefix ? prefix + '/' + n[0] : n[0];
                var field = MochiKit.DOM.getElement(name);
                if (field && !expr_fields[field.id]) {
                    fields[field.id] = 1;
                    expr_fields[field.id] = 1;
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
    
    var widget = MochiKit.DOM.getElement(widget);
    var prefix = widget ? widget.id.slice(0, widget.id.lastIndexOf('/')+1) : '';
    
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
        
        if (!elem) 
            continue;
        
        var op = ex[1];
        var val = ex[2];
        var elem_value = elem.value || getNodeAttribute(elem, 'value') || elem.innerHTML;
        
        switch (op) {
            
            case '=':
            case '==':
                result = result || (elem_value == val);
                break;
            case '!=':
            case '<>':
                result = result || (elem_value != val);
                break;
            case '<':
                result = result || (elem_value < val);
                break;
            case '>':
                result = result || (elem_value > val);
                break;
            case '<=':
                result = result || (elem_value <= val);
                break;
            case '>=':
                result = result || (elem_value >= val);
                break;
        }
    }
    
    return result;
}

var form_setReadonly = function(container, field, readonly) {
    
    if (!field)
        return;
    
    field.disabled = readonly;
    
    if (readonly) {
        MochiKit.DOM.addElementClass(field, 'readonlyfield');
    } else {
        MochiKit.DOM.removeElementClass(field, 'readonlyfield');
    }
    
    var kind = MochiKit.DOM.getNodeAttribute(field, 'kind');
    
    if (field.type == 'hidden' && kind == 'many2one') {
        form_setReadonly(container, getElement(field.name + '_text'), readonly);
    }
    
    if (kind == 'date' || kind == 'datetime' || kind == 'time') {
        
        var img = getElement(field.name + '_trigger');
        if (readonly)
            img.parentNode.style.display = 'none';
        else
            img.parentNode.style.display = '';
    }
}

var form_setRequired = function(container, field, required) {
    
    if (required) {
       MochiKit.DOM.addElementClass(field, 'requiredfield');    
    } else {
       MochiKit.DOM.removeElementClass(field, 'requiredfield');    
       MochiKit.DOM.removeElementClass(field, 'errorfield');
    }
    
    var kind = MochiKit.DOM.getNodeAttribute(field, 'kind');
    
    if (field.type == 'hidden' && kind == 'many2one') {
        form_setRequired(container, getElement(field.name + '_text'), required);
    }
}

var form_setVisible = function(container, field, visible) {
    
    if (MochiKit.DOM.hasElementClass(container, 'tabbertab')) { // notebook page?
    
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

// vim: ts=4 sts=4 sw=4 si et

