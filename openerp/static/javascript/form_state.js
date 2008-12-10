////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
//
// $Id$
//
// Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
//
// The OpenERP web client is distributed under the "OpenERP Public License".
// It's based on Mozilla Public License Version (MPL) 1.1 with following 
// restrictions:
//
// -   All names, links and logos of Tiny, Open ERP and Axelor must be 
//     kept as in original distribution without any changes in all software 
//     screens, especially in start-up page and the software header, even if 
//     the application source code has been changed or updated or code has been 
//     added.
//
// -   All distributions of the software must keep source code with OEPL.
// 
// -   All integrations to any other software must keep source code with OEPL.
//
// If you need commercial licence to remove this kind of restriction please
// contact us.
//
// You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
//
////////////////////////////////////////////////////////////////////////////////

var form_hookStateChange = function() {
    
    var items = [];
    
    items = items.concat(getElementsByTagAndClassName('td', 'item'));
    items = items.concat(getElementsByTagAndClassName('td', 'label'));
    items = items.concat(getElementsByTagAndClassName('div', 'tabbertab'));
    
    items = MochiKit.Base.filter(function(e){
        return getNodeAttribute(e, 'states');
    }, items);

    var fields = {};

    forEach(items, function(e) {
        var widget = getNodeAttribute(e, 'widget');
        var states = getNodeAttribute(e, 'states');
        var prefix = widget.slice(0, widget.lastIndexOf('/')+1) || '';

        // conver to JS
        states = states.replace(/u'/g, "'");
        states = states.replace(/True/g, '1');
        states = states.replace(/False/g, '0');
        states = eval('(' + states + ')');

        var state = getElement(prefix + 'state');
        if (state) {
            fields[state.id] = state;
            MochiKit.Signal.connect(state, 'onchange', MochiKit.Base.partial(form_onStateChange, e, widget, states));
        }
    });
    
    for(var field in fields) {
        MochiKit.Signal.signal(field, 'onchange');
    }
}

var form_onStateChange = function(container, widget, states, evt) {

    var src = evt.src();
    var value = typeof(src.value) == "undefined" ? getNodeAttribute(src, 'value') || src.innerHTML : src.value;

    if (MochiKit.Base.isArrayLike(states)) {
        return form_setVisible(container, widget, findIdentical(states, value) > -1);
    }

    var has_readonly = false;
    var has_required = false;

    for(var a in states) {
        a = states[a];
        has_readonly = has_readonly || typeof(a.readonly) != "undefined";
        has_required = has_required || typeof(a.required) != "undefined";
    }

    var attr = states[value];

    if (attr && has_readonly)
        form_setReadonly(container, widget, attr['readonly']);

    if (attr && has_required)
        form_setRequired(container, widget, attr['required']);

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
        var prefix = widget.slice(0, widget.lastIndexOf('/')+1) || '';

        // Convert Python statement into it's equivalent in JavaScript.
        attrs = attrs.replace(/\(/g, '[');
        attrs = attrs.replace(/\)/g, ']');
        attrs = attrs.replace(/True/g, '1');
        attrs = attrs.replace(/False/g, '0');
        
        try {
            attrs = eval('(' + attrs + ')');
        } catch(e){
            return;
        }
        
        for (var attr in attrs) {
            var expr_fields = {}; // check if field appears more then once in the expr
            forEach(attrs[attr], function(n){
                var name = prefix + n[0];
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
    
    var result = true;
    
    for(var i=0; i<expr.length; i++) {
        
        var ex = expr[i];
        var elem = MochiKit.DOM.getElement(prefix + ex[0]);
        
        if (!elem) 
            continue;
        
        var op = ex[1];
        var val = ex[2];
        var elem_value = elem.value || getNodeAttribute(elem, 'value') || elem.innerHTML;
        
        switch (op.toLowerCase()) {
            
            case '=':
            case '==':
                result = result && (elem_value == val);
                break;
            case '!=':
            case '<>':
                result = result && (elem_value != val);
                break;
            case '<':
                result = result && (elem_value < val);
                break;
            case '>':
                result = result && (elem_value > val);
                break;
            case '<=':
                result = result && (elem_value <= val);
                break;
            case '>=':
                result = result && (elem_value >= val);
                break;
            case 'in':
                result = result && MochiKit.Base.findIdentical(val, elem_value) > -1;
                break;
            case 'not in':
                result = result && MochiKit.Base.findIdentical(val, elem_value) == -1;
                break;
        }
    }
    
    return result;
}

var form_setReadonly = function(container, field, readonly) {
    
    if (!field)
        return;
    
    field = MochiKit.DOM.getElement(field);
    
    if (field) {
        field.readOnly = readonly;
        field.disabled = readonly;
    }
    
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
        if (img)
            img.parentNode.style.display = readonly ? 'none' : '';
    }
}

var form_setRequired = function(container, field, required) {
    
    if (required) {
        MochiKit.DOM.addElementClass(field, 'requiredfield');
    } else {
        MochiKit.DOM.removeElementClass(field, 'requiredfield');
    }
    MochiKit.DOM.removeElementClass(field, 'errorfield');

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
    form_hookStateChange();
    form_hookAttrChange();
});

// vim: ts=4 sts=4 sw=4 si et

