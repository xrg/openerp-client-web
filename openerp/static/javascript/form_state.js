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

var form_hookContextMenu = function(){
    if (!MochiKit.DOM.getElement('_terp_list')) {
        MochiKit.Signal.connect(window.document, 'oncontextmenu', on_context_menu);
    }
}

var form_hookOnChange = function() {

    var prefix = '';
    try {
        prefix = getElement('_terp_o2m').value + '/';
    }catch(e){}
    
    var id = getElement(prefix + '_terp_id').value;
    var view_type = getElement('_terp_view_type').value;
    var editable = getElement('_terp_editable').value;

    if (!(view_type == 'form' || editable == 'True')) {
        return;
    }

    var fields = getFormData();
    //TODO: remove onchange="${onchange}" from all templates and register onChange here

    // signal fake onchange events for default value in new record form
    id = parseInt(id) || 0;
    if (id) return;

    for(var name in fields) {
        var field = getElement(name);
        if (field && field.value && getNodeAttribute(field, 'callback')) {
            if (field.onchange) {
                field.onchange();
            } else {
                MochiKit.Signal.signal(field, 'onchange');
            }
        }
    }
}

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

        var state = getElement(prefix + 'state') || getElement(prefix + 'x_state');
        if (state) {
            fields[state.id] = state;
            MochiKit.Signal.connect(state, 'onStateChange', MochiKit.Base.partial(form_onStateChange, e, widget, states));
            MochiKit.Signal.connect(state, 'onchange', function(evt){
                MochiKit.Signal.signal(field, 'onStateChange');
            });
        }
    });
    
    for(var field in fields) {
        MochiKit.Signal.signal(field, 'onStateChange');
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
        attrs = attrs.replace(/uid/g, window.USER_ID);
        
        try {
            attrs = eval('(' + attrs + ')');
        } catch(e){
            return;
        }

        for (var attr in attrs) {
            var expr_fields = {}; // check if field appears more then once in the expr

            if (attrs[attr] == ''){
                return form_onAttrChange(container, widget, attr, attrs[attr]);
            }
            
            forEach(attrs[attr], function(n){

                if (typeof(n) == "number") { // {'invisible': [1]}
                    return form_onAttrChange(container, widget, attr, n);
                }

                var name = prefix + n[0];
                var field = MochiKit.DOM.getElement(name);
                if (field && !expr_fields[field.id]) {
                    fields[field.id] = 1;
                    expr_fields[field.id] = 1;
                    MochiKit.Signal.connect(field, 'onAttrChange', partial(form_onAttrChange, container, widget, attr, attrs[attr]));
                    MochiKit.Signal.connect(field, 'onchange', function(evt){
                        MochiKit.Signal.signal(field, 'onAttrChange');
                    });
                }
            });
        }
    });
    
    for(var field in fields) {
        MochiKit.Signal.signal(field, 'onAttrChange');
    }
}

var form_onAttrChange = function(container, widget, attr, expr, evt) {

    var prefix = widget.slice(0, widget.lastIndexOf('/')+1);
    var widget = MochiKit.DOM.getElement(widget);

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
        var elem_value = elem.value || getNodeAttribute(elem, 'value');
        
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
    
    var field = MochiKit.DOM.getElement(field);

    if (!field) {
        return;
    }
    
    var kind = MochiKit.DOM.getNodeAttribute(field, 'kind');
    
    if (kind == 'boolean') {        
        var i = MochiKit.DOM.getElement(field)
        field = MochiKit.DOM.getElement(i.id + '_checkbox_')
    }

    if (!kind && 
            MochiKit.DOM.getElement(field.id + '_id') && 
            MochiKit.DOM.getElement(field.id + '_set') &&
            MochiKit.DOM.getNodeAttribute(field.id + '_id', 'kind') == "many2many") {
        return Many2Many(field.id).setReadonly(readonly);
    }

	var type = MochiKit.DOM.getNodeAttribute(field, 'type');

    field.readOnly = readonly;
    field.disabled = readonly;
    
    if (readonly && (type != 'button')) {
        MochiKit.DOM.addElementClass(field, 'readonlyfield');
    } else {
        MochiKit.DOM.removeElementClass(field, 'readonlyfield');
    }
    
    if (field.type == 'hidden' && kind == 'many2one') {
        //form_setReadonly(container, getElement(field.name + '_text'), readonly);
        return ManyToOne(field).setReadonly(readonly);
    }
    
    if (!kind && MochiKit.DOM.getElement(field.id + '_btn_') || MochiKit.DOM.getElement('_o2m_'+field.id)) { // one2many
    	return new One2Many(field.id).setReadonly(readonly);
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
        var tab = tabber.tabs[idx];

        if (visible && tab.li.style.display == 'none') {
            tab.li.style.display = '';
            tabber.tabShow(idx);
        } else if (!visible && tab.li.style.display != 'none') {
            var tab = tabber.tabs[idx];
            tab.li.style.display = 'none';
            var was_active = hasElementClass(tab.li, 'tabberactive');
            tabber.tabHide(idx);
            //When not define any page it display always 1st one.
            //e.g state = 'dummy' not display page.
            //if (idx == active) {
              //  tabber.tabShow(0);
            //}
            if (!was_active) return;
            function selectCandidate(index) {
                // returns true if it found a candidate suitable for selection
                // (visible tab)
                var candidate = tabber.tabs[index];
                if(candidate.li.style.display != 'none') {
                    tabber.tabShow(index);
                    return true;
                }
                return false;
            }
            var i;
            // Search backwards for a visible tab
            for(i = idx-1; i >= 0; --i) {
                if(selectCandidate(i)) { return; }
            }
            // Not found one backwards, try forwards
            for(i = idx+1; i < tabber.tabs.length; ++i) {
                if(selectCandidate(i)) { return; }
            }
        }

    } else {
        container.style.display = visible ? '' : 'none';
        try {
            var label = getNodeAttribute(container, 'for');
            label = MochiKit.Selector.findChildElements(container.parentNode, ['td.label[for="' + label + '"]'])[0];
            if (!label){
            	container.style.display = visible ? '' : 'none';
            }
            else{
            	getFirstParentByTagAndClassName(container).style.display = visible ? '' : 'none';
            }
        }catch(e){}
    }
}

MochiKit.DOM.addLoadEvent(function(evt){    
    form_hookContextMenu();
    form_hookStateChange();
    form_hookAttrChange();
    form_hookOnChange();
});

// vim: ts=4 sts=4 sw=4 si et

