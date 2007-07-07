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
}

ListView.prototype.checkAll = function(clear){

    clear = clear == null ? true: clear;

    boxes = $(this.id).getElementsByTagName('input');
    forEach(boxes, function(box){
        box.checked = clear;
    });
}

ListView.prototype.getSelected = function() {

    boxes = getElementsByTagAndClassName('input', 'grid-record-selector', this.id);
    result = [];

    forEach(boxes, function(box){
        if (box.name && box.checked) result.push(box);
    });

    return result;
}

ListView.prototype.create = function(){
	this.edit(-1);
}

ListView.prototype.edit = function(id){
	this.reload(id);
}

ListView.prototype.save = function(id, model){

    var args = {};
    var parent_field = this.id.split('/');
    
    args['_terp_id'] = id;
    args['_terp_model'] = model;
    
    if (parent_field.length > 0){
		parent_field.pop();
	}
	
    parent_field = parent_field.join('/');
    parent_field = parent_field ? parent_field + '/' : '';
    
    args['_terp_parent/id'] = $(parent_field + '_terp_id').value;
    args['_terp_parent/model'] = $(parent_field + '_terp_model').value;
    args['_terp_parent/context'] = $(parent_field + '_terp_context').value;
    
    var inputs = [];
    var myself = this;

	inputs = inputs.concat(getElementsByTagAndClassName('input', null, this.id));
	inputs = inputs.concat(getElementsByTagAndClassName('select', null, this.id));

    forEach(inputs, function(e){
    	if (e.name && !hasElementClass(e, 'grid-record-selector')){
    		// remove '_terp_listfields/' prefix
    		var n = e.name.split('/');
            n.shift();

            var f = '_terp_form/' + n.join('/');
            var k = '_terp_kind/' + n.join('/');
            var r = '_terp_required/' + n.join('/');

            args[f] = e.value;
            args[k] = e.attributes['kind'].value;
            if (hasElementClass(e, 'requiredfield'))
            	args[k] += ' required';
        }
    });
    
    var req= Ajax.JSON.post('/listgrid/save', args);

    req.addCallback(function(obj){
        if (obj.error){
           alert(obj.error);
        }else{
            myself.reload(id ? null : -1);
        }
    });    
}

ListView.prototype.remove = function(record_id){
}

ListView.prototype.reload = function(edit_inline){

	var myself = this;
    var args = {};
    
    args['_terp_source'] = this.id;
    args['_terp_edit_inline'] = edit_inline;

    args['_terp_model'] = $('_terp_model').value;
    args['_terp_id'] = $('_terp_id').value;
    args['_terp_view_ids'] = $('_terp_view_ids').value;
    args['_terp_context'] = $('_terp_context').value;

    var req = Ajax.JSON.post('/listgrid/get', args);
    
    req.addCallback(function(obj){
    	
    	var ids = $(myself.id + '/_terp_ids');
    	if (ids)
    		ids.value = obj.ids;

        var d = DIV();
        d.innerHTML = obj.view;

        var l = d.getElementsByTagName('table')[0];
                  
        swapDOM(myself.id, l);
    });
    
    req.addErrback(function(err){
        logError(err);
    });
}
