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

var add_filter_row = function() {
	
	var filter_table = $('filter_table');
	var vals = [];
	
	row_id = 1;
	
	first_row = $('filter_row');
	
	if (filter_table.style.display == 'none') {
		filter_table.style.display = '';
	}
	
	else if (first_row.style.display == 'none') {
		first_row.style.display = ''
	}
	
	else{
		
		var old_tr = MochiKit.DOM.getFirstElementByTagAndClassName('tr', null, filter_table)
		
		var new_tr = old_tr.cloneNode(true);
		
		if (new_tr.id.indexOf('/') != -1) {
			keys = new_tr.id.split('/');
			id = parseInt(keys[1]);
			id = id + 1;
			new_tr.id = keys[0] + '/' + id;
			
			insertSiblingNodesBefore(old_tr, new_tr);
		}
		else {
			new_tr.id = new_tr.id +'/'+ row_id;
			
			var and_or = MochiKit.DOM.getFirstElementByTagAndClassName('td', 'and_or', new_tr);
			
			var select_andor = document.createElement('select');
			var option = document.createElement('option');

			vals.push('AND');
			vals.push('OR');

			option = map(function(x){return OPTION({'value': x}, x)}, vals);

			appendChildNodes(select_andor, option);
			appendChildNodes(and_or, select_andor);
			insertSiblingNodesBefore(old_tr, new_tr);
		}
	}
}

var remove_row = function(id) {
	
	var filter_table = $('filter_table');
	
	node = MochiKit.DOM.getFirstParentByTagAndClassName(id, 'tr', 'filter_row_class');
	
	if (node.id.indexOf('/') != -1) {
		removeElement(node);
	}
	else {
		node.style.display = 'none';
	}
}

var search_image_filter = function(src, id) {
	domain = getNodeAttribute(id, 'value');
	search_filter(src, domain);
}

var search_filter = function(src, domain) {
	var type = getNodeAttribute(src, 'type');
	
	var lst = new ListView('_terp_list');
	var ids = []
	
	if (type=='checkbox') {
		id = SelectedDomains();
		id = id.toString();
		
		if (id.length > 0) {
			domain = id.replace(/(]\,\[)/g, ',');
		}
		else {
			domain = 'None';
		}
	}
	var req = eval_domain_context_request({source: '_terp_list', domain: domain});

    req.addCallback(function(obj){
    	$('_terp_search_domain').value = obj.domain;
        lst.reload();
    });
}

var getSelectedDomain = function() {
    return filter(function(box){
        return box.id && box.checked;
    }, getElementsByTagAndClassName('input', 'grid-domain-selector'));
}

var SelectedDomains = function() {
    return map(function(box){
    	log("box..."+box.value);
        return box.value;
    }, this.getSelectedDomain());
}
    