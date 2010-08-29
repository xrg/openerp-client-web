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
// -   All names, links and logos of Tiny, OpenERP and Axelor must be 
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

function form_hookContextMenu(){
    if (!openobject.dom.get('_terp_list')) {
        MochiKit.Signal.connect(window.document, 'oncontextmenu', on_context_menu);
    }
}

function form_hookOnChange() {
    var prefix = '';
    try {
        prefix = openobject.dom.get('_terp_o2m').value + '/';
    }catch(e){}

    var view_type = jQuery('#_terp_view_type').val();
    var editable = jQuery('#_terp_editable').val();

    if (!(view_type == 'form' || editable == 'True')) {
        return;
    }

    var fields = getFormData();
    if (parseInt(openobject.dom.get(prefix + '_terp_id').value, 10) || 0) return;

    for(var name in fields) {
        var field = openobject.dom.get(name);
        if (field && field.value && getNodeAttribute(field, 'callback')) {
            if (field.onchange) {
                field.onchange();
            } else {
                MochiKit.Signal.signal(field, 'onchange');
            }
        }
    }
}

function form_hookStateChange() {
    var fields = {};

    jQuery('td.item, td.label, div.tabbertab').filter(function(){
        return jQuery(this).attr('states');
    }).each(function() {
        var $this = jQuery(this);
        var widget = $this.attr('widget');
        var prefix = widget.slice(0, widget.lastIndexOf('/')+1) || '';

        // convert states from Python serialization to JS/JSON
        var states = eval(
                '(' + $this.attr('states')
                      .replace(/u'/g, "'")
                      .replace(/True/g, '1')
                      .replace(/False/g, '0') + ')');

        var state = openobject.dom.get(prefix + 'state') || openobject.dom.get(prefix + 'x_state');
        if (state) {
            fields[state.id] = state;
            MochiKit.Signal.connect(state, 'onStateChange', MochiKit.Base.partial(form_onStateChange, this, widget, states));
            MochiKit.Signal.connect(state, 'onchange', function (){
                MochiKit.Signal.signal(field, 'onStateChange');
            });
        }
    });
    
    for(var field in fields) {
        MochiKit.Signal.signal(field, 'onStateChange');
    }
}

function form_onStateChange(container, widget, states, evt) {

    var src = evt.src();
    var value = typeof(src.value) == "undefined" ? getNodeAttribute(src, 'value') || src.innerHTML : src.value;

    if (MochiKit.Base.isArrayLike(states)) {
        form_setVisible(container, widget, findIdentical(states, value) > -1);
        return;
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

function form_hookAttrChange() {
    
    var items = [];
    
    items = items.concat(openobject.dom.select('td.item'));
    items = items.concat(openobject.dom.select('td.label'));
    items = items.concat(openobject.dom.select('div.notebook-page'));
    
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
                var field = openobject.dom.get(name);
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

function form_onAttrChange(container, widgetName, attr, expr) {
    var prefix = widgetName.slice(0, widgetName.lastIndexOf('/') + 1);
    var widget = openobject.dom.get(widgetName);

    var result = form_evalExpr(prefix, expr);

    switch (attr) {
        case 'readonly': form_setReadonly(container, widget, result);
            break;
        case 'required': form_setRequired(container, widget, result);
            break;
        case 'invisible': form_setVisible(container, widget, !result);
            break;
        default:
    }
}

function form_evalExpr(prefix, expr) {

    var stack = [];
    for (var i = 0; i < expr.length; i++) {

        var ex = expr[i];
        var elem = openobject.dom.get(prefix + ex[0]);
        
        if (ex.length==1) {
            stack.push(ex[0]);
            continue;
        }
        
        if (!elem) 
            continue;
        
        var op = ex[1];
        var val = ex[2];
        var elem_value = elem.value || getNodeAttribute(elem, 'value') || elem.innerHTML;
        
        switch (op.toLowerCase()) {
            case '=':
            case '==':
                stack.push(elem_value == val);
                break;
            case '!=':
            case '<>':
                stack.push(elem_value != val);
                break;
            case '<':
                stack.push(elem_value < val);
                break;
            case '>':
                stack.push(elem_value > val);
                break;
            case '<=':
                stack.push(elem_value <= val);
                break;
            case '>=':
                stack.push(elem_value >= val);
                break;
            case 'in':
                stack.push(MochiKit.Base.findIdentical(val, elem_value) > -1);
                break;
            case 'not in':
                stack.push(MochiKit.Base.findIdentical(val, elem_value) == -1);
                break;
        }
    }

    for (var j=stack.length-1; j>-1; j--) {
        if(stack[j] == '|'){
            var result = stack[j+1] || stack[j+2];
            stack.splice(j, 3, result)
        }
    }
    // shouldn't find any `false` left at this point
    return stack.indexOf(false) == -1;
}

function form_setReadonly(container, fieldName, readonly) {
    
    var field = openobject.dom.get(fieldName);

    if (!field) {
        return;
    }
    
    var kind = MochiKit.DOM.getNodeAttribute(field, 'kind');
    
    if (kind == 'boolean') {
        var boolean_id = jQuery(fieldName).attr('id')
        var boolean_field = jQuery('input#'+boolean_id+'_checkbox_')
        boolean_field.attr('disabled', readonly)
        boolean_field.attr('readOnly', readonly)
    }

    if (!kind && 
            openobject.dom.get(field.id + '_id') && 
            MochiKit.DOM.getElement(field.id + '_set') &&
            MochiKit.DOM.getNodeAttribute(field.id + '_id', 'kind') == "many2many") {
         Many2Many(field.id).setReadonly(readonly)
        return;
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
        ManyToOne(field).setReadonly(readonly);
        return
    }
    
    if (!kind && MochiKit.DOM.getElement(field.id + '_btn_') || MochiKit.DOM.getElement('_o2m_'+field.id)) { // one2many
        new One2Many(field.id).setReadonly(readonly);
        return
    }
    
    if (kind == 'date' || kind == 'datetime' || kind == 'time') {
        var img = openobject.dom.get(field.name + '_trigger');
        if (img)
            img.parentNode.style.display = readonly ? 'none' : '';
    }
}

function form_setRequired(container, field, required) {
    
    if (!field) {
        field = container;
    }
    
    if (required) {
        MochiKit.DOM.addElementClass(field, 'requiredfield');
    } else {
        MochiKit.DOM.removeElementClass(field, 'requiredfield');
    }
    MochiKit.DOM.removeElementClass(field, 'errorfield');

    var kind = MochiKit.DOM.getNodeAttribute(field, 'kind');
    
    if (field.type == 'hidden' && kind == 'many2one') {
        form_setRequired(container, openobject.dom.get(field.name + '_text'), required);
    }
}

function form_setVisible(container, field, visible) {

    if (MochiKit.DOM.hasElementClass(container, 'notebook-page')) { // notebook page?
    
        var nb = container.parentNode.parentNode.notebook;
        
        if (!nb)  {
           MochiKit.Async.callLater(0, form_setVisible, container, field, visible);
           return;
        }
        
        var i = findIdentical(nb.pages, container);
        
        if (visible) {
            nb.show(i, false);
        } else {
            nb.hide(i);
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

jQuery(document).ready(function(){
    form_hookContextMenu();
    form_hookStateChange();
    form_hookAttrChange();
    form_hookOnChange();
});
