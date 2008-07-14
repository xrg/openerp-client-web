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

var ListView = function(id, terp){

    this.id = id;
    this.terp = terp;
    
    var prefix = id == '_terp_list' ? '' : id + '/';

    this.model = $(prefix + '_terp_model') ? $(prefix + '_terp_model').value : null;
    this.current_record = null;
    
    var view_ids = getElement(prefix + '_terp_view_ids');
    var view_mode = getElement(prefix + '_terp_view_mode');
    var def_ctx = getElement(prefix + '_terp_default_get_ctx');
    
    this.view_ids = view_ids ? view_ids.value : null;
    this.view_mode = view_mode ? view_mode.value : null;
    
    // if o2m
    this.default_get_ctx = def_ctx ? def_ctx.value : null;
    
    this.m2m = getElement(id + '_set');
}

ListView.prototype.checkAll = function(clear){

    clear = clear ? false : true;

    boxes = $(this.id).getElementsByTagName('input');
    forEach(boxes, function(box){
        box.checked = clear;
    });
}

ListView.prototype.getRecords = function() {
    var records = map(function(row){
        return parseInt(getNodeAttribute(row, 'record')) || 0;
    }, getElementsByTagAndClassName('tr', 'grid-row', this.id));
    
    return filter(function(rec){
        return rec;
    }, records);
}

ListView.prototype.getSelectedRecords = function() {
    return map(function(box){
        return box.value;
    }, this.getSelectedItems());
}

ListView.prototype.getSelectedItems = function() {
    return filter(function(box){
        return box.id && box.checked;
    }, getElementsByTagAndClassName('input', 'grid-record-selector', this.id));
}

ListView.prototype.create = function(){
    
    var tbl = $(this.id + '_grid');
    var editor = getElementsByTagAndClassName('tr', 'editors', tbl)[0];
    MochiKit.DOM.setNodeAttribute(editor, 'record', 0);
    
    this.edit(-1);
}

ListView.prototype.loadEditors = function(edit_inline, args){
    
    var self = this;
    var req = Ajax.JSON.post('/listgrid/get_editor', args);

    req.addCallback(function(obj){
		
		if(obj.source == '_terp_list')
			prefix = '_terp_listfields';
		else
        	prefix = '_terp_listfields' + '/' + obj.source;

        var tbl = $(obj.source + '_grid');
        var tr = null;
        var idx = 1;
        
        var editor_row = getElementsByTagAndClassName('tr', 'editors', tbl)[0];
        var editors = self.adjustEditors(editor_row);
        
        if (editors.length > 0)
            self.bindKeyEventsToEditors(editors);

            record_id = MochiKit.DOM.getNodeAttribute(editor_row, 'record');

            if(edit_inline != -1) {

                for (var i=0; i<tbl.rows.length; i++){
                    
                    var e = tbl.rows[i];
                    tr = MochiKit.DOM.getNodeAttribute(e, 'record') == edit_inline ? e : null;
                    if (tr) break;
                }

                if (tbl.last) {
                    tbl.last.style.display = '';
                }

                idx = findIdentical(tbl.rows, tr);
            }

            var tr_tmp = tbl.insertRow(idx);
            swapDOM(tr_tmp, editor_row);

            if(edit_inline == -1 && record_id == null){
                editor_row.style.display = '';
            } else if(edit_inline == -1 && record_id >= 0){
                if (tbl.last) {
                    tbl.last.style.display = '';
                }
                editor_row.style.display = '';
            } else {
                tr.style.display = 'none';
                editor_row.style.display = '';

                MochiKit.DOM.setNodeAttribute(editor_row, 'record', edit_inline);
            }

            elements = [];

            elements = elements.concat(getElementsByTagAndClassName('input', null, editor_row));
            elements = elements.concat(getElementsByTagAndClassName('select', null, editor_row));

            forEach(elements, function(f) {
                getElement(f).value = "";
            });

            for(var r in obj.res) {
                var id = prefix + '/' + r;
                var kind = 'char';
                var elem = getElement(id);
	
                if (elem) {
                    kind = MochiKit.DOM.getNodeAttribute(elem, 'kind');

                    if (kind ==  'many2one') {
                        val = obj.res[r] || ['', '']
                            elem.value = val[0];
                        try {
                            getElement(id + '_text').value = val[1];
                        } catch(e) {}
                    } else {
                        elem.value = obj.res[r];
                    }
                }
            }

            tbl.last = tr;
            var first = getElementsByTagAndClassName(null, 'listfields', this.id)[0] || null;
            if (first) {
                first.focus();
                first.select();
            }
    });
}

ListView.prototype.edit = function(edit_inline){

    var self = this;
    var args = this.makeArgs();
    
    // add args
    args['_terp_source'] = this.id;
    args['_terp_edit_inline'] = edit_inline;
    
    if (this.id == '_terp_list') {
        args['_terp_search_domain'] = $('_terp_search_domain').value;
    }
    
    if (!this.default_get_ctx) {
        return self.loadEditors(edit_inline, args)  
    }

    var req = eval_domain_context_request({source: this.id, context : this.default_get_ctx});
    
    req.addCallback(function(res){
        args['_terp_context'] = res.context;        
        self.loadEditors(edit_inline, args);        
    });
}

ListView.prototype.cancel_editor = function(row){
    
    var editor_cancel = getElementsByTagAndClassName('tr', 'editors', tbl)[0];

    if(!row) {
        row = editor_cancel;
    }

    editor_cancel.style.display = 'none';
    var tbl = row.parentNode.parentNode;

    if(tbl.last) {
        MochiKit.DOM.setNodeAttribute(editor_cancel, 'record', 0);
        tbl.last.style.display = '';
    }
}

ListView.prototype.save_editor = function(row){
    this.save(MochiKit.DOM.getNodeAttribute(row, 'record'));
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
        this.cancel_editor();
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

        if (src.onchange) {
            src.onchange();
        }
        
        var tbl = $(this.id + '_grid');
        
        var editor_save = getElementsByTagAndClassName('tr', 'editors', tbl)[0];
        
        evt.stop();
        this.save(MochiKit.DOM.getNodeAttribute(editor_save, 'record'));

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
            self.makeRow(obj.rec_id);
         }
     });
 }
 
ListView.prototype.getParentTag = function(element, tagName, className) {
	var pNode = element.parentNode;
	
	while (pNode) {
		
		if(tagName == null && hasElementClass(pNode, className)){
			break;
		}
		else if ((tagName) && pNode.tagName == tagName.toUpperCase() && className == null) {
			break;
		}
		else if ((tagName) && pNode.tagName == tagName.toUpperCase() && hasElementClass(pNode, className)) {
			break;
		}
		
		pNode = pNode.parentNode;	
	}
	return pNode;
}

ListView.prototype.makeRow = function(rec_id) {
	var self = this;
	var tbl = $(this.id + '_grid');
	
	var editor_row = getElementsByTagAndClassName('tr', 'editors', tbl)[0];
	
	var col = getElementsByTagAndClassName('td', 'grid-cell', editor_row);
	
	record_id = MochiKit.DOM.getNodeAttribute(editor_row, 'record');
	
	if(record_id > 0) {
	    rec_id = record_id;
	}
	
	var elem = [];
	var elements = [];
	var tds = [];
	var parent_tag = [];
	
	elem = self.getColumns();
	
	elements = elements.concat(getElementsByTagAndClassName('input', null, editor_row));
	elements = elements.concat(getElementsByTagAndClassName('select', null, editor_row));
	
	forEach(elem, function(e){
		elem_id = getElement(e).id.replace('grid-data-column', '_terp_listfields');
		temp_id = elem_id;
		for(var i=0; i<elements.length; i++) {
			if(getElement(elements[i]).type != 'hidden') {
				if(elem_id == getElement(elements[i]).id || (elem_id + '_text') == getElement(elements[i]).id){
					parent_tag = self.getParentTag(getElement(elements[i]), 'td', 'grid-cell');
					
					value = getElement(elements[i]).value;
					
					if(parent_tag.className.indexOf('many2one') != -1 || i == 0){
					    var col_anch = MochiKit.DOM.TD({'class': parent_tag.className});
					    
					    if(i==0) {
					       var anch = MochiKit.DOM.A({'onclick': 'do_select(\'' + rec_id + '\', \'' + self.id + '\'); return false;', 'href': 'javascript: void(0)'}, value);
					    }
					    else if(parent_tag.className.indexOf('many2one') != -1){
					        
					        var m2o_id = getElement(temp_id).value;
					        var relation = getNodeAttribute(getElement(elements[i]), 'relation');
					        
					        var action = '/form/view?model=' + relation + '&id= ' + m2o_id;
					        
					        var anch = MochiKit.DOM.A({'href': 'javascript: void(0)'}, value);
					        
					        MochiKit.DOM.setNodeAttribute(anch, 'href', action);
					    }
					    MochiKit.DOM.appendChildNodes(col_anch, anch);
					    tds.push(col_anch);
					}
					else {
					    var col = MochiKit.DOM.TD({'class': parent_tag.className}, value);
					    tds.push(col);
					}
				}
			}
		}
	});
	
	var td_edit = MochiKit.DOM.TD({'class': 'grid-cell selector', 'style': 'text-align: center; padding: 0px;'});	
	var edit = MochiKit.DOM.IMG({'class': 'listImage', 'border': '0', 'src': '/static/images/edit_inline.gif', 'onclick': 'new ListView(\''+ this.id +'\').edit('+ rec_id +')'});
	
	MochiKit.DOM.appendChildNodes(td_edit, edit);
	tds.push(td_edit);
	
	var td_del = MochiKit.DOM.TD({'class': 'grid-cell selector', 'style': 'text-align: center; padding: 0px;'});
	var del = MochiKit.DOM.IMG({'class': 'listImage', 'border': '0', 'src': '/static/images/delete_inline.gif', 'onclick': 'new ListView(\''+ this.id +'\').remove('+ rec_id +')'});
	
	MochiKit.DOM.appendChildNodes(td_del, del);	
	tds.push(td_del);
    
	if(record_id > 0) {
		var tr = MochiKit.DOM.TR({'class': 'grid-row', 'record': record_id}, tds);
		
		idx = findIdentical(tbl.rows, editor_row);
        swapDOM(tbl.last, tr);
    	
		tr.style.display = '';
		editor_row.style.display = 'none';
        MochiKit.DOM.setNodeAttribute(editor_row, 'record', 0);
	}
	else {
	    var idx = 1;
		var tr = MochiKit.DOM.TR({'class': 'grid-row', 'record': rec_id}, tds);
        
        var tr_tmp = tbl.insertRow(idx + 1);
        swapDOM(tr_tmp, tr);
		
		self.create();
	}
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

    req.addCallback(function(obj){
        if (obj.error){
            alert(obj.error);
        } else {
            self.reload();
        }
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
}

ListView.prototype.onButtonClick = function(name, btype, id, sure){

    if (sure && !confirm(sure)){
        return;
    }
    
    var self = this;
    var prefix = this.id == '_terp_list' ? '' : this.id + '/';
    
    var params = {
        _terp_model : this.model,
        _terp_id : id,
        _terp_button_name : name,
        _terp_button_type : btype,
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

ListView.prototype.exportData = function(){
    
    var ids = this.getSelectedRecords();
    
    if (ids.length == 0) {
        ids = this.getRecords();
    }
    
    ids = '[' + ids.join(',') + ']';
    
    openWindow(getURL('/impex/exp', {_terp_model: this.model, 
                                     _terp_source: this.id, 
                                     _terp_search_domain: $('_terp_search_domain').value, 
                                     _terp_ids: ids,
                                     _terp_view_ids : this.view_ids,
                                     _terp_view_mode : this.view_mode}));
}

ListView.prototype.importData = function(){
    openWindow(getURL('/impex/imp', {_terp_model: this.model,
                                     _terp_source: this.id,
                                     _terp_view_ids : this.view_ids,
                                     _terp_view_mode : this.view_mode}));
}

ListView.prototype.go = function(action){

    if (Ajax.COUNT > 0){
        return;
    }

    var prefix = this.id == '_terp_list' ? '' : this.id + '/';

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

