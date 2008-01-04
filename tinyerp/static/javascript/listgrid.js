///////////////////////////////////////////////////////////////////////////////
//
// Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
//
// $Id$
//
// WARNING: This program as such is intended to be used by professional
// programmers who take the whole responsability of assessing all potential
// consequences resulting from its eventual inadequacies and bugs
// End users who are looking for a ready-to-use solution with commercial
// garantees and support are strongly adviced to contract a Free Software
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
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
//
///////////////////////////////////////////////////////////////////////////////

var ListView = function(id, terp){

    this.id = id;
    this.terp = terp;

    var prefix = id == '_terp_list' ? '' : id + '/';

    this.model = $(prefix + '_terp_model') ? $(prefix + '_terp_model').value : null;
    this.current_record = null;

    this.wait_counter = 0;
}

ListView.prototype.checkAll = function(clear){

    clear = clear ? false : true;

    boxes = $(this.id).getElementsByTagName('input');
    forEach(boxes, function(box){
        box.checked = clear;
    });
}

ListView.prototype.getSelectedRecords = function(boxes) {
    return map(function(box){
        return box.value;
    }, this.getSelectedItems());
}

ListView.prototype.getSelectedItems = function(boxes) {
    return filter(function(box){
        return box.name && box.checked;
    }, getElementsByTagAndClassName('input', 'grid-record-selector', this.id));
}

ListView.prototype.create = function(){
    this.edit(-1);
}

ListView.prototype.edit = function(id){
    if (this.wait_counter > 0)
        return;

    this.reload(id);
}

ListView.prototype.getEditors = function(named, dom){

    var editors = [];
    var dom = dom ? dom : this.id;

    editors = editors.concat(getElementsByTagAndClassName('input', null, dom));
    editors = editors.concat(getElementsByTagAndClassName('select', null, dom));
    editors = editors.concat(getElementsByTagAndClassName('textarea', null, dom));

    return filter(function(e){
        name = named ? e.name : e.id;
        return name &&  name.indexOf('_terp_listfields') == 0;
    }, editors);
}

ListView.prototype.getColumns = function(dom){
    dom = dom || this.id;
    var header = getElementsByTagAndClassName('tr', 'grid-header', dom)[0];
    
    return filter(function(c){
        return c.id ? true : false;
    }, getElementsByTagAndClassName('th', 'grid-cell', header));
}

ListView.prototype.adjustEditors = function(newlist){
    
    var editors = this.getEditors(false, newlist);

    forEach(editors, function(e) {
        // disable autocomplete (Firefox < 2.0 focus bug)
        setNodeAttribute(e, 'autocomplete', 'OFF');
    });

    if (/MSIE/.test(navigator.userAgent)){
        return editors;
    }

    var widths = {};
    
    // set the column widths of the newlist
    forEach(this.getColumns(), function(c){
        widths[c.id] = parseInt(c.offsetWidth) - 8;
    });
 
    forEach(this.getColumns(newlist), function(c){
        c.style.width = widths[c.id] + 'px';
    });

    var widths = {};
    forEach(this.getEditors(), function(e){
        widths[e.id] = parseInt(e.offsetWidth);
    });

    return editors;    
}

ListView.prototype.onKeyDown = function(evt){

    var key = evt.key();
    var src = evt.src();

    if (!(key.string == "KEY_TAB" || key.string == "KEY_ENTER" || key.string == "KEY_ESCAPE")) {
        return;
    }

    if (key.string == "KEY_ESCAPE"){
        evt.stop();
        this.reload();
        return;
    }

    if (key.string == "KEY_ENTER"){

        if (hasElementClass(src, "m2o")){

            var k = src.id;
            k = k.slice(0, k.length - 5);

            if (src.value && !getElement(k).value){
                return;
            }
        }

        evt.stop();
        this.save(this.current_record);

        return;
    }

    var editors = getElementsByTagAndClassName(null, 'listfields', this.id);

    var first = editors.shift();
    var last = editors.pop();

    if (src == last){
        evt.stop();
        first.focus();
        first.select();
    }
}

ListView.prototype.bindKeyEventsToEditors = function(editors){
    var self = this;

    var editors = filter(function(e){
        return e.type != 'hidden' && !e.disabled
    }, editors);

    forEach(editors, function(e){
        connect(e, 'onkeydown', self, self.onKeyDown);
        addElementClass(e, 'listfields');
    });
}

ListView.prototype.save = function(id){

    if (Ajax.COUNT > 0) {
        return callLater(1, bind(this.save, this), id);
    }

    var parent_field = this.id.split('/');
    var args = getFormData(2);

    args['_terp_id'] = id ? id : -1;
    args['_terp_model'] = this.model;

    if (parent_field.length > 0){
        parent_field.pop();
    }

    parent_field = parent_field.join('/');
    parent_field = parent_field ? parent_field + '/' : '';

    args['_terp_parent/id'] = $(parent_field + '_terp_id').value;
    args['_terp_parent/model'] = $(parent_field + '_terp_model').value;
    args['_terp_parent/context'] = $(parent_field + '_terp_context').value;
    args['_terp_source'] = this.id;

    var self = this;
    var req= Ajax.JSON.post('/listgrid/save', args);

    this.waitGlass();

    req.addCallback(function(obj){
        if (obj.error){
            alert(obj.error);

            if (obj.error_field) {
                var fld = getElement('_terp_listfields/' + obj.error_field);

                if (fld && getNodeAttribute(fld, 'kind') == 'many2one')
                    fld = getElement(fld.id + '_text');

                if (fld) {
                    fld.focus();
                    fld.select();
                }
            }
        } else {
            self.reload(id > 0 ? null : -1);
        }
    });

    req.addBoth(function(xmlHttp){
        self.waitGlass(true);
    });
}

ListView.prototype.remove = function(id){

    if (!confirm('Do you realy want to delete this record?')) {
        return false;
    }

    var self = this;
    var args = {};

    args['_terp_model'] = this.model;
    args['_terp_id'] = id;

    var req = Ajax.JSON.post('/listgrid/remove', args);

    this.waitGlass();

    req.addCallback(function(obj){
        if (obj.error){
            alert(obj.error);
        } else {
            self.reload();
        }
    });

    req.addBoth(function(xmlHttp){
        self.waitGlass(true);
    });
}

ListView.prototype.makeArgs = function(){

    var args = {};
    var names = this.id.split('/');

    var values = ['id', 'ids', 'model', 'view_ids', 'view_mode', 
                  'view_type', 'domain', 'context', 'offset', 'limit'];

    forEach(values, function(val){
        var key = '_terp_' + val;
        args[key] = getElement(key).value;
    });

    for(var i=0; i<names.length; i++){

        var name = names[i];
        var prefix = names.slice(0, i).join('/');

        prefix = prefix ? prefix + '/' + name : name;
        prefix = prefix + '/';

        forEach(values, function(val){
            var key = prefix + '_terp_' + val;
            var elem = getElement(key);

            if (elem) args[key] = elem.value;
        });
    }

    return args;
}

ListView.prototype.reload = function(edit_inline){

    var self = this;
    var args = this.makeArgs();

    // add args
    args['_terp_source'] = this.id;
    args['_terp_edit_inline'] = edit_inline;

    if (this.id == '_terp_list') {
        args['_terp_search_domain'] = $('_terp_search_domain').value;
    }

    var req = Ajax.JSON.post('/listgrid/get', args);

    this.waitGlass();

    req.addCallback(function(obj){

        var _terp_ids = $(self.id + '/_terp_ids') || $('_terp_ids');
        var _terp_count = $(self.id + '/_terp_count') || $('_terp_count');

        _terp_ids.value = obj.ids;
        _terp_count.value = obj.count;

        var d = DIV();
        d.innerHTML = obj.view;

        var newlist = d.getElementsByTagName('table')[0];
        var editors = self.adjustEditors(newlist);
        
        if (editors.length > 0)
            self.bindKeyEventsToEditors(editors);
            
        self.current_record = edit_inline;

        swapDOM(self.id, newlist);

        var ua = navigator.userAgent.toLowerCase();

        if ((navigator.appName != 'Netscape') || (ua.indexOf('safari') != -1)) {
            // execute JavaScript
            var scripts = getElementsByTagAndClassName('script', null, newlist);
            forEach(scripts, function(s){
                eval(s.innerHTML);
            });
        }

        // set focus on the first field
        var first = getElementsByTagAndClassName(null, 'listfields', this.id)[0] || null;
        if (first) {
            first.focus();
            first.select();
        }

    });

    req.addBoth(function(xmlHttp){
        self.waitGlass(true);
    });
}

ListView.prototype.onButtonClick = function(action, id, type){
    
    var self = this;
    var prefix = this.id == '_terp_list' ? '' : this.id + '/';
    
    var params = {
        _terp_model : this.model,
        _terp_id : id,
        _terp_button_name : action,
        _terp_button_type : type,
        _terp_context : $(prefix + '_terp_context').value
    }
    
    var req = Ajax.JSON.post('/listgrid/button_action', params);
    req.addCallback(function(obj){
        if (obj.error){
            return alert(obj.error);
        }
        self.reload();
    });
}

function findPosition(elem) {
    var x = y = 0;
    if (elem.offsetParent) {
        x = elem.offsetLeft
        y = elem.offsetTop
        while (elem = elem.offsetParent) {
            x += elem.offsetLeft
            y += elem.offsetTop
        }
    }
    return {x: x, y: y};
}

ListView.prototype.waitGlass = function(hide){

    this.wait_counter += hide ? -1 : 1;

    var block = $('listgrid_ajax_wait');

    if (!block){
        block = DIV({id: 'listgrid_ajax_wait', style: "position: absolute; display: none; background-color: gray;"});
        setOpacity(block, 0.2);

        appendChildNodes(document.body, block);
    }

    if (this.wait_counter == 0){
        hideElement(block);
        return;
    }

    if (this.wait_counter > 1){
        return;
    }

    var thelist = $(this.id);

    //var p = elementPosition(thelist);
    var p = findPosition(thelist);
    var d = elementDimensions(thelist);

    setElementPosition(block, p);
    setElementDimensions(block, d);

    showElement(block);
}

ListView.prototype.exportData = function(){
    openWindow(getURL('/impex/exp', {_terp_model: this.model, 
                                     _terp_source: this.id, 
                                     _terp_search_domain: $('_terp_search_domain').value, 
                                     _terp_ids: $(this.id)}), {height: '840'});
}

ListView.prototype.importData = function(){
    openWindow(getURL('/impex/imp', {_terp_model: this.model, _terp_source: this.id}));
}

ListView.prototype.go = function(action){

    var prefix = '';

    if (this.id != '_terp_list') {
        prefix = this.id + '/';
    }

    var o = $(prefix + '_terp_offset');
    var l = $(prefix + '_terp_limit');
    var c = $(prefix + '_terp_count');

    var ov = o.value ? parseInt(o.value) : 0;
    var lv = l.value ? parseInt(l.value) : 0;
    var cv = c.value ? parseInt(c.value) : 0;

    switch(action) {
        case 'next':
            o.value = ov + lv;
            break;
        case 'previous':
            o.value = lv > ov ? 0 : ov - lv;
            break;
        case 'first':
            o.value = 0;
            break;
        case 'last':
            o.value = cv - (cv % lv);
            break;
    }

    this.reload();
}

// vim: sts=4 st=4 et

