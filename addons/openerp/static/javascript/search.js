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
		var old_qstring = MochiKit.DOM.getFirstElementByTagAndClassName('input', 'qstring', old_tr);
		old_qstring.style.background = '#FFFFFF';
		
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
			qstring.style.background = '#FFFFFF';
			qstring.value = '';
			
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
			qstring.style.background = '#FFFFFF';
			qstring.value = '';
			
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
		$('qstring').style.background = '#FFFFFF';
	}
}
// Direct click on icon.
var search_image_filter = function(src, id) {
	domain = getNodeAttribute(id, 'value');
	search_filter(src);
}

var onKey_Event = function(evt) {
	
	dom = $('search_filter_data');
	
	var editors = [];
	
	editors = editors.concat(getElementsByTagAndClassName('input', null, dom));
    editors = editors.concat(getElementsByTagAndClassName('select', null, dom));
    editors = editors.concat(getElementsByTagAndClassName('textarea', null, dom));
    
    var editors = filter(function(e){
        return e.type != 'hidden' && !e.disabled
    }, editors);

    forEach(editors, function(e){
        connect(e, 'onkeydown', self, onKeyDown_search);
    });
}

var onKeyDown_search = function(evt) {
	var key = evt.key();
    var src = evt.src();
    
    if (key.string == "KEY_ENTER"){
    	search_filter();
    }
}

var search_filter = function(src) {
	
	all_domains = {};
	check_domain = 'None';
	domains = {};
	search_context = {};
	var group_by_ctx = [];
	
	domain = 'None';
	
	var filter_table = $('filter_table');
	datas = $$('[name]', 'search_filter_data');
	
	forEach(datas, function(d) {
		if (d.type != 'checkbox' && d.name && d.value && d.name.indexOf('_terp_') == -1  && d.name != 'filter_list') {
			value = d.value;
			if (getNodeAttribute(d, 'kind') == 'selection') {
				value = parseInt(d.value);
				if(getNodeAttribute(d, 'search_context')) {
					search_context['context'] = getNodeAttribute(d, 'search_context');
					search_context['value'] = value;
				}
			}
			domains[d.name] = value;
		}
	});
	
	domains = serializeJSON(domains);
	all_domains['domains'] = domains;
	all_domains['search_context'] =  search_context;
	
	selected_boxes = getElementsByTagAndClassName('input', 'grid-domain-selector');
	
	all_boxes = [];
	
	forEach(selected_boxes, function(box){
		if (box.id && box.checked && box.value != '[]') {
			all_boxes = all_boxes.concat(box.value);
		}
		if (box.id && box.checked && getNodeAttribute(box, 'group_by_ctx').length > 0) {
    		group = getNodeAttribute(box, 'group_by_ctx');
    		group_by_ctx = group_by_ctx.concat(group);
		}
	});
	
	openobject.dom.get('_terp_group_by_ctx').value = group_by_ctx;
	
	checked_button = all_boxes.toString();
	
	if (checked_button.length > 0) {
		check_domain = checked_button.replace(/(]\,\[)/g, ', ');
	}
	else {
		check_domain = 'None';
	}
	
	all_domains['check_domain'] = check_domain;
	
	var selection_domain = $('filter_list').value;
	
	if (selection_domain) {
		all_domains['selection_domain'] = selection_domain;
	}
	
	if(filter_table.style.display != 'none') {
		var custom_domains = [];
		var params = {};
		var record = {};
		
		children = MochiKit.DOM.getElementsByTagAndClassName('tr', 'filter_row_class', filter_table);
		forEach(children, function(ch){
			
			var ids = ch['id'];	// row id...
			if(ids && ids.indexOf('/')!= -1) {
				id = ids.split('/')[1];
				var qid = 'qstring/' + id;
				var fid = 'filter_fields/' + id;
				var eid = 'expr/' + id;
				
				if ($(qid) && $(qid).value) {
					var rec = {};
					rec[$(fid).value] = $(qid).value;
					params['_terp_model'] = openobject.dom.get('_terp_model').value;
				}
			}
			
			else {
				var qid = 'qstring';
				var fid = 'filter_fields';
				var eid = 'expr';
				
				var q_val = '';
				
				if ($(qid) && $(qid).value) {
					var rec = {};
					rec[$(fid).value] = $(qid).value;
					params['_terp_model'] = openobject.dom.get('_terp_model').value;
				}
			}
			if (rec) {
				record[ids] = rec;
			}
		});
		
		record = serializeJSON(record);
		params['record'] = record;
		
		var search_req = openobject.http.postJSON('/search/get', params);

		var custom_domain = [];
		search_req.addCallback(function(obj){
			if (obj.error) {
				forEach(children, function(child){
					var cids = child['id']
					if(cids && cids.indexOf('/')!= -1) {
						id = cids.split('/')[1];
						var fid = 'filter_fields/' + id;
					}
					else {
						var fid = 'filter_fields';
					}
					if ($(fid).value == obj.error_field) {
						if (fid.indexOf('/')!= -1) {
							f = fid.split('/')[1];
							$('qstring/'+f).style.background = '#FF6666';
						}
						else {
							$('qstring').style.background = '#FF6666';
						}						
					}
				});
			}
			if (obj.frm) {
    			for (var i in obj.frm) {
    				var temp_domain = [];
    				var operator = 'None';
    				
    				row_id = serializeJSON(i);
    				
    				if(row_id && row_id.indexOf('/')!= -1) {

						id = row_id.split('/')[1];
						id = parseInt(id);
						
						var fid = 'filter_fields/' + id;
						var eid = 'expr/' + id;
	    				var select_andor = 'select_andor/' + id;
	    				var type = obj.frm[i].type;
						
						if ($(select_andor).value == 'AND') {
							var operator = '&';
						}
						else {
							var operator = '|';
						}
    				}
    				else {
    					var fid = 'filter_fields';
						var eid = 'expr';
						var type = obj.frm[i].type;
    				}
    				
    				if (operator != 'None') {
    					temp_domain.push(operator);
    				}
    				
    				var first_text = obj.frm[i].rec;
    				var expression = $(eid).value;
    				var right_text = obj.frm[i].rec_val;
    				if (expression=='ilike'||expression=='not ilike'){
    					if (type=='integer'||type=='float'||type=='date'||type=='datetime'||type=='boolean'){
    						if (expression == 'ilike')
    							expression = '=';
    						else {
    							expression = '!=';
    						}
    					}
    				}
    				if ((expression == '<' || expression == '>') && (type!='integer'||type!='float'||type!='date'||type!='datetime'||type!='boolean')){
    					expression = '=';
    				}
    				if (expression == 'in' || expression == 'not in'){
    					right_text = right_text.split(',');
    				}
    				
					temp_domain.push(first_text);
					temp_domain.push(expression);
					temp_domain.push(right_text);
					
					custom_domain.push(temp_domain);
    			}
			}
			custom_domain = serializeJSON(custom_domain);
			all_domains = serializeJSON(all_domains);
			
			final_search_domain(custom_domain, all_domains, group_by_ctx);
		});
	}
	else {
		custom_domain = []
		all_domains = serializeJSON(all_domains);
		final_search_domain(custom_domain, all_domains, group_by_ctx);	
	}
}

var final_search_domain = function(custom_domain, all_domain, group_by_ctx) {
	
	var lst = new ListView('_terp_list');
	var req = openobject.http.postJSON('/search/eval_domain_filter', {source: '_terp_list',
															model: $('_terp_model').value, 
															custom_domain: custom_domain,
															all_domains: all_domains});
	
	req.addCallback(function(obj){
		if (obj.flag) {
			var params = {'domain': obj.sf_dom,
							'model': openobject.dom.get('_terp_model').value,
							'flag': obj.flag};
								
			openobject.tools.openWindow(openobject.http.getURL('/search/save_filter', params), {width: 400, height: 250});
		}
		if (obj.action) { // For manage Filter
			action = serializeJSON(obj.action);
			window.location.href = openobject.http.getURL('/search/manage_filter', {action: action});
		}
		if (obj.domain) { // For direct search
			var in_req = eval_domain_context_request({source: '_terp_list', domain: obj.domain, context: obj.context});

		    in_req.addCallback(function(in_obj){
		    	openobject.dom.get('_terp_search_domain').value = in_obj.domain;
		    	openobject.dom.get('_terp_context').value = in_obj.context;
		    	lst.reload();
		    });	
		}
	});
}

MochiKit.DOM.addLoadEvent(function(evt){
	onKey_Event(evt);
	search_filter();
});
