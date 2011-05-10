////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY OpenERP SA. All Rights Reserved.
//
// $Id$
//
// Developed by OpenERP (http://openerp.com) and Axelor (http://axelor.com).
//
// The OpenERP web client is distributed under the "OpenERP Public License".
// It's based on Mozilla Public License Version (MPL) 1.1 with following 
// restrictions:
//
// -   All names, links and logos of OpenERP must be kept as in original
//     distribution without any changes in all software screens, especially
//     in start-up page and the software header, even if the application
//     source code has been changed or updated or code has been added.
//
// You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
//
////////////////////////////////////////////////////////////////////////////////

function onSelect(evt, node){
}

function getXPath(node) {

    var path = node.getPath(1);

    var xp = '';
    var nd = path.pop();

    while (nd.record.items.localName != 'view') {

        var similar = MochiKit.Base.filter(function(n){
            return n.record.items.localName == nd.record.items.localName;
        }, nd.parentNode.childNodes);

        var idx = MochiKit.Base.findIdentical(similar, nd) + 1;

        xp = '/' + nd.record.items.localName + '[' + idx + ']' + xp;
        nd = path.pop();
    }

    return xp;
}

function onDelete(node){

    var tree = treeGrids['view_tree'];
    var selected = node || tree.selection[0] || null;

    if (!selected) {
        return;
    }

    var record = selected.record;
    var data = record.items;

    if (data.localName == 'view' && !selected.parentNode.element) {
        return;
    }

    if (!confirm(_('Do you really want to remove this node?'))) {
        return;
    }

    var act = data.localName == 'view' ? '/openerp/viewed/remove_view' : '/openerp/viewed/save/remove';

    var req = openobject.http.postJSON(act, {view_id: data.view_id, xpath_expr: getXPath(selected)});
    req.addCallback(function(obj){

        if (obj.error){
            return error_display(obj.error);
        }

        selected.parentNode.removeChild(selected);
    });
}

function onAdd(node){

    var tree = treeGrids['view_tree'];
    var selected = node || tree.selection[0] || null;
    
    if (!selected) {
        return;
    }
    
    var record = selected.record;
    var data = record.items;
    
    if (data.localName == 'view') {
        return;
    }
    
    var req = openobject.http.post('/openerp/viewed/add', {view_id: data.view_id, xpath_expr: getXPath(selected)});
    req.addCallback(function(xmlHttp){
        var el = window.mbox.content;
        el.innerHTML = xmlHttp.responseText;

        var scripts = openobject.dom.select('script', el);
        forEach(scripts, function(s){
            eval('(' + s.innerHTML + ')');
        });

        var dim = getElementDimensions(document.body);

        window.mbox.width = 400;
        window.mbox.height = 150;
        window.mbox.onUpdate = doAdd;

        window.mbox.show();
    });
}

function doAdd() {

    var tree = treeGrids['view_tree'];
    var selected = tree.selection[0] || null;

    if (!selected) {
        return;
    }

    var form = document.forms['view_form'];
    var params = {};

    forEach(form.elements, function(el){
        params[el.name] = el.value;
    });

    var act = openobject.dom.get('node').value == 'view' ? '/openerp/viewed/create_view' : '/openerp/viewed/save/node';

    var req = openobject.http.postJSON(act, params);
    req.addCallback(function(obj) {

        if (obj.error){
            return error_display(obj.error);
        }

        var node = tree.createNode(obj.record);
        var pnode = selected.parentNode;

        var pos = openobject.dom.get('position').value;

        if (pos == 'after') {
            pnode.insertBefore(node, selected.nextSibling);
        }

        if (pos == 'before') {
            pnode.insertBefore(node, selected);
        }

        if (pos == 'inside') {
            selected.appendChild(node);
        }

        node.onSelect();

        if (obj.record.items && obj.record.items.edit)
            MochiKit.Async.callLater(0.1, onEdit, node);
    });

    req.addBoth(function(obj){
        window.mbox.hide();
    });
    
    return false;
}

function onEdit(node) {

    var tree = treeGrids['view_tree'];
    var selected = node || tree.selection[0] || null;
    
    if (!selected) {
        return;
    }
    
    var record = selected.record;
    var data = record.items;
    
    if (data.localName == 'view') {
        return;
    }
    
    var req = openobject.http.post('/openerp/viewed/edit', {view_id: data.view_id, xpath_expr: getXPath(selected)});
    req.addCallback(function(xmlHttp){
        
        var el = window.mbox.content;
        el.innerHTML = xmlHttp.responseText;
        
        var scripts = openobject.dom.select('script', el);
        forEach(scripts, function(s){
            eval(s.innerHTML);
        });

        var dim = getElementDimensions(document.body);

        window.mbox.width = Math.max(dim.w - 100, 0);
        window.mbox.height = Math.max(dim.h - 100, 0);
        window.mbox.onUpdate = doEdit;

        window.mbox.show();
    });
}

function doEdit() {

    var tree = treeGrids['view_tree'];
    var selected = tree.selection[0] || null;

    if (!selected) {
        return;
    }

    var form = document.forms['view_form'];
    var params = {};

    forEach(form.elements, function(el){

        if (!el.name) return;

        var val = el.type == 'checkbox' ? el.checked ? 1 : null : el.value;

        if (el.type == 'select-multiple') {

            val = MochiKit.Base.filter(function(o){
                return o.selected;
            }, el.options);

            val = MochiKit.Base.map(function(o){
                return o.value;
            }, val);

            val = val.join(',');
        }

        if (val) {
           params[el.name] = val;
        }
    });

    var req = openobject.http.postJSON('/openerp/viewed/save/properties', params);
    req.addCallback(function(obj){

        if (obj.error){
            error_display(obj.error);
        }

        selected.updateDOM(obj.record);
    });

    req.addBoth(function(obj){
        window.mbox.hide();
    });

    return false;
}

function onMove(direction, node) {

    var tree = treeGrids['view_tree'];
    var selected = node || tree.selection[0] || null;

    if (!selected) {
        return;
    }

    var refNode = direction == 'up' ? selected.previousSibling : selected;
    var node = direction == 'up' ? selected : selected.nextSibling;

    if (!node || (direction == 'up' && !refNode)) {
        return;
    }

    var record = node.record;
    var data = record.items;

    var params = {
        view_id: data.view_id,
        xpath_expr: getXPath(node),
        xpath_ref: getXPath(refNode)
    };

    var req = openobject.http.postJSON('/openerp/viewed/save/move', params);

    req.addCallback(function(obj) {

        if (obj.error){
            return error_display(obj.error);
        }

        var pnode = node.parentNode;
        var nnode = tree.createNode(record);

        pnode.removeChild(node);
        pnode.insertBefore(nnode, refNode);

        if (direction == 'up') {
            nnode.onSelect();
        } else {
            refNode.onSelect();
        }
    });

    return true;
}

function onButtonClick(evt, node) {

    var src = evt.src();

    switch (src.name) {
        case 'edit':
            return onEdit(node);
        case 'delete':
            return onDelete(node);
        case 'add':
            return onAdd(node);
        case 'up':
        case 'down':
            return onMove(src.name, node);
    }
}

function onInherit() {

    if (!confirm(_('Do you really wants to create an inherited view here?'))) {
        return;
    }

    var tree = treeGrids['view_tree'];
    var selected = tree.selection[0] || null;

    if (!selected) {
        return;
    }

    params = {
        view_id: openobject.dom.get('view_id').value,
        xpath_expr: getXPath(selected)
    };

    var req = openobject.http.postJSON('/openerp/viewed/create_view', params);
    req.addCallback(function(obj) {

        if (obj.error){
            return error_display(obj.error);
        }

        var node = tree.createNode(obj.record);
        selected.appendChild(node);
    });

    return false;
}

function onPreview() {
   var act = openobject.http.getURL('/openerp/viewed/preview/show', {'model' : openobject.dom.get('view_model').value,
                                             'view_id' : openobject.dom.get('view_id').value,
                                             'view_type' : openobject.dom.get('view_type').value});

    if (window.browser.isGecko19) {
        return jQuery.frame_dialog({src:act});
    }

    return jQuery.frame_dialog({src:act});
}

function onNew(model){
    var act = openobject.http.getURL('/openerp/viewed/new_field/edit', {'for_model' : model});
    jQuery.frame_dialog({src: act}, {'source-window': jQuery(window)[0]});
}

function onClose(){
    window.top.setTimeout('window.location.reload()', 1);
    window.frameElement.close();
}

function toggleFields(selector) {
    openobject.dom.get('name').style.display = selector.value == 'field' ? '' : 'none';
    openobject.dom.get('new_field').style.display = selector.value == 'field' ? '' : 'none';
}

function onUpdate(){
    window.mbox.onUpdate();
}

function addNewFieldName(name) {
    var op = openobject.dom.get("name").options;
    op[op.length] = new Option(name, name, 0, 1);
}

jQuery(document).ready(function(){

    window.mbox = new ModalBox({
        title: 'Properties',
        buttons: [
            {text: 'Update', onclick: onUpdate}
        ]
    });

});

// vim: sts=4 st=4 et
