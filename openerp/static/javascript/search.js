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
		
		var old_tr = MochiKit.DOM.getFirstElementByTagAndClassName('tr', null, filter_table);
		
		var new_tr = old_tr.cloneNode(true);
		
		if (new_tr.id.indexOf('/') != -1) {
			keys = new_tr.id.split('/');
			id = parseInt(keys[1]);
			id = id + 1;
			new_tr.id = keys[0] + '/' + id;
			
			var filter_column = MochiKit.DOM.getFirstElementByTagAndClassName('td', 'filter_column', new_tr);
			
			var filter_fields = MochiKit.DOM.getFirstElementByTagAndClassName('select', 'filter_fields', new_tr);
			var expr = MochiKit.DOM.getFirstElementByTagAndClassName('select', 'expr', new_tr);
			var qstring = MochiKit.DOM.getFirstElementByTagAndClassName('input', 'qstring', new_tr);
			
			var and_or = MochiKit.DOM.getFirstElementByTagAndClassName('td', 'and_or', new_tr);
			
			aid = and_or.id.split('/')[0];
			and_or.id = aid + '/' + id;
			
			var select_andor = MochiKit.DOM.getFirstElementByTagAndClassName('select', 'select_andor', and_or);
			sid = select_andor.id.split('/')[0];
			select_andor.id = sid + '/' + id;
			
			fcid = filter_column.id.split('/')[0];
			filter_column.id = fcid + '/' + id;
			
			fid = filter_fields.id.split('/')[0];
			filter_fields.id = fid + '/' + id;
			
			eid = expr.id.split('/')[0];
			expr.id = eid + '/' + id;
			
			qid = qstring.id.split('/')[0];
			qstring.id = qid + '/' + id;
			
			insertSiblingNodesBefore(old_tr, new_tr);
		}
		else {
			new_tr.id = new_tr.id +'/'+ row_id;
			
			var filter_column = MochiKit.DOM.getFirstElementByTagAndClassName('td', 'filter_column', new_tr);
			
			var filter_fields = MochiKit.DOM.getFirstElementByTagAndClassName('select', 'filter_fields', new_tr);
			var expr = MochiKit.DOM.getFirstElementByTagAndClassName('select', 'expr', new_tr);
			var qstring = MochiKit.DOM.getFirstElementByTagAndClassName('input', 'qstring', new_tr);
			
			filter_column.id = filter_column.id + '/' + row_id;
			
			filter_fields.id = filter_fields.id + '/' + row_id;
			expr.id = expr.id + '/' + row_id;
			qstring.id = qstring.id + '/' + row_id;
			
			var and_or = MochiKit.DOM.getFirstElementByTagAndClassName('td', 'and_or', new_tr);
			and_or.id = and_or.id + '/' + row_id;
			
			var select_andor = document.createElement('select');
			select_andor.id = 'select_andor/' + row_id;
			select_andor.className = 'select_andor';
			
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
		$('qstring').value = '';
	}
}
// Direct click on icon.
var search_image_filter = function(src, id) {
	domain = getNodeAttribute(id, 'value');
	search_filter(domain);
}

var search_filter = function(src, domain) {
	
	if (!domain) {
		domain = 'None';
	}
	
	check_domain = '';
	domains = {};
	
	var field_type = getNodeAttribute(src, 'type')
	
	var filter_table = $('filter_table');
	datas = $$('[name]', 'search_filter_data');
	
	forEach(datas, function(d) {
		if (d.type != 'checkbox' && d.name && d.value && d.name.indexOf('_terp_') == -1) {
			value = d.value;
			if (getNodeAttribute(d, 'kind') == 'selection') {
				value = parseInt(d.value);
				domains[d.name] = value;
			}
			else {
				domains[d.name] = value;	
			}
		}
	});
	
	domains = serializeJSON(domains);
		
	if (getNodeAttribute(src, 'type')=='checkbox') {
		id = SelectedDomains();
		id = id.toString();
		
		if (id.length > 0) {
			check_domain = id.replace(/(]\,\[)/g, ', ');
		}
		else {
			check_domain = 'None';
		}
	}
	
	var lst = new ListView('_terp_list');
	var req = Ajax.JSON.post('/search/eval_domain_filter', {source: '_terp_list', 
															check_domain: check_domain,
															domains: domains, 
															field_type: field_type});
	
	req.addCallback(function(obj){
		if (obj.domain) {
			var in_req = eval_domain_context_request({source: '_terp_list', domain: obj.domain});

		    in_req.addCallback(function(in_obj){
		    	$('_terp_search_domain').value = in_obj.domain;
		        lst.reload();
		    });	
		}
	});
}

var getSelectedDomain = function() {
    return filter(function(box){
        return box.id && box.checked;
    }, getElementsByTagAndClassName('input', 'grid-domain-selector'));
}

var SelectedDomains = function() {
    return map(function(box){
        return box.value;
    }, this.getSelectedDomain());
}
    