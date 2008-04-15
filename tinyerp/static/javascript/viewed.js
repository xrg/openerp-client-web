////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://tinyerp.com) All Rights Reserved.
//
// $Id: master.js 1586 2008-01-23 10:54:04Z ame $
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

var onSelect = function(evt, node){
    MochiKit.DOM.getElement('view_ed').innerHTML = '';
}

var getXPath = function(node) {
    
    var path = node.getPath(1);
    
    var xp = '';
    var nd = path.pop()
    
    while (nd.record.items.localName != 'view') {
        
        var similar = MochiKit.Base.filter(function(n){
            return n.record.items.localName == nd.record.items.localName; 
        }, nd.parentNode.childNodes);
        
        var idx = MochiKit.Base.findIdentical(similar, nd) + 1
        
        xp = '/' + nd.record.items.localName + '[' + idx + ']' + xp;
        nd = path.pop();
    }
    
    return xp;
}

var onDelete = function(node){
    
    getElement('view_ed').innerHTML = '';

    var tree = view_tree;
    var selected = node || tree.selection[0] || null;
    
    if (!selected) {
        return;
    }        
    
    var record = selected.record;
    var data = record.items;
    
    if (data.localName == 'view' && !selected.parentNode.element) {
        return;
    }
    
    if (!confirm('Do you really want to remove this node?')) {
        return;
    }
    
    var act = data.localName == 'view' ? '/viewed/remove_view' : '/viewed/save/remove';
    
    var req = Ajax.JSON.post(act, {view_id: data.view_id, xpath_expr: getXPath(selected)});
    req.addCallback(function(obj){
        
        if (obj.error){
            return alert(obj.error);
        }
        
        selected.parentNode.removeChild(selected);
        getElement('view_ed').innerHTML = '';
    });
}

var onAdd = function(node){

    var tree = view_tree;
    var selected = node || tree.selection[0] || null;
    
    if (!selected) {
        return;
    }
    
    var record = selected.record;
    var data = record.items;
    
    if (data.localName == 'view') {
        return;
    }
    
    var req = Ajax.post('/viewed/add', {view_id: data.view_id, xpath_expr: getXPath(selected)});
    req.addCallback(function(xmlHttp){
        var el = getElement('view_ed');
        el.innerHTML = xmlHttp.responseText;
    });
}

var doAdd = function() {
    
    var tree = view_tree;
    var selected = tree.selection[0] || null;
    
    if (!selected) {
        return;
    }

    var form = getElement('view_form');
    var params = {};
    
    forEach(form.elements, function(el){
        params[el.name] = el.value;
    });
    
    var act = MochiKit.DOM.getElement('node').value == 'view' ? '/viewed/create_view' : '/viewed/save/node';
    
    var req = Ajax.JSON.post(act, params);
    req.addCallback(function(obj) {
        
        if (obj.error){
            return alert(obj.error);
        }
        
        var node = tree.createNode(obj.record);
        var pnode = selected.parentNode;
        
        var pos = MochiKit.DOM.getElement('position').value;
        
        if (pos == 'after') {
            pnode.insertBefore(node, selected.nextSibling);    
        }
        
        if (pos == 'before') {
            pnode.insertBefore(node, selected);
        }
        
        if (pos == 'inside') {
            selected.appendChild(node);
        }
        
        getElement('view_ed').innerHTML = '';

    });
    
    return false;
}

var onEdit = function(node) {

    var tree = view_tree;
    var selected = node || tree.selection[0] || null;
    
    if (!selected) {
        return;
    }
    
    var record = selected.record;
    var data = record.items;
    
    var el = getElement('view_ed');
    
    if (data.localName == 'view') {
        el.innerHTML = '';
        return;
    };
    
    var req = Ajax.post('/viewed/edit', {view_id: data.view_id, xpath_expr: getXPath(selected)});
    req.addCallback(function(xmlHttp){
        el.innerHTML = xmlHttp.responseText;
    });
}

var doEdit = function() {
    
    var tree = view_tree;
    var selected = tree.selection[0] || null;
    
    if (!selected) {
        return;
    }

    var form = getElement('view_form');
    var params = {};
    
    forEach(form.elements, function(el){
        
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
    
    var req = Ajax.JSON.post('/viewed/save/properties', params);
    req.addCallback(function(obj){
        
        if (obj.error){
            alert(obj.error);
        }
        
        selected.updateDOM(obj.record);
        getElement('view_ed').innerHTML = '';
        
    });
    
    return false;
}

var onButtonClick = function(evt, node) {
    
    var src = evt.src();
    
    if (src.name == 'edit') {
        return onEdit(node);   
    }
    
    if (src.name == 'delete') {
        return onDelete(node);   
    }
    
    if (src.name == 'add') {
        return onAdd(node);   
    }
}

var onInherit = function() {
    
    if (!confirm('Do you really wants to create an inherited view here?')) {
        return;
    }
    
    var tree = view_tree;
    var selected = tree.selection[0] || null;
    
    if (!selected) {
        return;
    }
    
    params = {
        view_id: getElement('view_id').value,
        xpath_expr: getXPath(selected)
    };
    
    var req = Ajax.JSON.post('/viewed/create_view', params);
    req.addCallback(function(obj) {
        
        if (obj.error){
            return alert(obj.error);
        }
        
        var node = tree.createNode(obj.record);
        selected.appendChild(node);
    });
    
    return false;
}

var onPreview = function() {
   var act = getURL('/viewed/preview/show', {'model' : getElement('view_model').value, 
                                             'view_id' : getElement('view_id').value,
                                             'view_type' : getElement('view_type').value});
   window.open(act);
}

var onNew = function(model){                          
    var act = getURL('/viewed/new_field/edit', {'for_model' : model});
    openWindow(act, {width: 650, height: 300});
}

var onClose = function(){
    window.opener.setTimeout("window.location.reload()", 1);
    window.close();
}

var toggleFields = function(selector) {
    MochiKit.DOM.getElement('name').style.display = selector.value == 'field' ? '' : 'none';
    MochiKit.DOM.getElement('new_field').style.display = selector.value == 'field' ? '' : 'none';
}

// vim: sts=4 st=4 et
