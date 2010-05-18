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
/**
 * @event onaddfilter triggered when adding a filter row
 *  @target #filter_table the element holding the filter rows
 *  @argument 'the newly added (or showed for first row?) filter row'
 */
var add_filter_row = function() {
	
	var filter_table = $('filter_table');
	var vals = [];
	var row_id = 1;
	
	var first_row = $('filter_row/0');
	var trs = MochiKit.DOM.getElementsByTagAndClassName('tr', null, filter_table)
	
	if (filter_table.style.display == 'none') {
		filter_table.style.display = '';
	}
	
	else if (first_row.style.display == 'none' && trs.length <= 1) {
		MochiKit.DOM.getFirstElementByTagAndClassName('select', 'filter_fields', first_row).selectedIndex = 0;
		MochiKit.DOM.getFirstElementByTagAndClassName('select', 'expr', first_row).selectedIndex = 0;
		var old_qstring = MochiKit.DOM.getFirstElementByTagAndClassName('input', 'qstring', first_row);
		old_qstring.value = '';
		old_qstring.style.background = '#FFFFFF';
		first_row.style.display = ''
	}
	
	else{
		
		var old_tr = trs[trs.length-1]
		var old_qstring = MochiKit.DOM.getFirstElementByTagAndClassName('input', 'qstring', old_tr);
		old_qstring.style.background = '#FFFFFF';
		
		var new_tr = old_tr.cloneNode(true);
		keys = new_tr.id.split('/');
		id = parseInt(keys[1], 0);
		row_id = id + row_id
		new_tr.id =  keys[0] +'/'+ row_id;
		var filter_column = MochiKit.DOM.getFirstElementByTagAndClassName('td', 'filter_column', new_tr);
		
		var filter_fields = MochiKit.DOM.getFirstElementByTagAndClassName('select', 'filter_fields', new_tr);
		var expr = MochiKit.DOM.getFirstElementByTagAndClassName('select', 'expr', new_tr);
		var qstring = MochiKit.DOM.getFirstElementByTagAndClassName('input', 'qstring', new_tr);
		
		filter_column.id = filter_column.id.split('/')[0] + '/' + row_id;
		filter_fields.id = filter_fields.id.split('/')[0] + '/' + row_id;
		expr.id = expr.id.split('/')[0] + '/' + row_id;
		qstring.id = qstring.id.split('/')[0] + '/' + row_id;
		qstring.style.background = '#FFFFFF';
		qstring.value = '';
		
		var image_col = MochiKit.DOM.getFirstElementByTagAndClassName('td', 'image_col', new_tr);
		image_col.id = 'image_col/' + row_id
		
		var and_or = MochiKit.DOM.getFirstElementByTagAndClassName('td', 'and_or', new_tr);
		if (and_or){removeElement(and_or); }
		
		var and_or = MochiKit.DOM.createDOM('td');
		and_or.id = 'and_or/' + id;
		and_or.className = 'and_or';
		
		var select_andor = MochiKit.DOM.createDOM('select');
		select_andor.id = 'select_andor/' + id;
		select_andor.className = 'select_andor';
		
		var option = MochiKit.DOM.createDOM('option');
		
		vals.push('AND');
		vals.push('OR');
		
		option = map(function(x){return OPTION({'value': x}, x)}, vals);
		image_replace = openobject.dom.get('image_col/'+ id);
		if(MochiKit.DOM.getFirstElementByTagAndClassName('td', 'and_or', old_tr) == null){
			insertSiblingNodesBefore(image_replace, and_or)
		}
		
		appendChildNodes(select_andor, option);
		appendChildNodes(and_or, select_andor);
		insertSiblingNodesAfter(old_tr, new_tr);
		
		MochiKit.Signal.connect(new_tr, 'onkeydown', this, onKeyDown_search);
		MochiKit.Signal.signal(filter_table, 'onaddfilter', new_tr || first_row);
	}
}

/**
 * @event onremovefilter triggered when removing a filter row
 *  @target #filter_table the element holding the filter rows
 *  @argument 'the removed (or hidden) filter row'
 */
var remove_row = function(id) {
	
	var filter_table = $('filter_table');
	
	node = MochiKit.DOM.getFirstParentByTagAndClassName(id, 'tr', 'filter_row_class');
	
	if (node.id != 'filter_row/0') {
		removeElement(node);
	}
	else {
		node.style.display = 'none';
		if ($('and_or/0'))
			removeElement($('and_or/0'));
		$('qstring/0').value = '';
		$('qstring/0').style.background = '#FFFFFF';
	}
	MochiKit.Signal.signal(filter_table, 'onremovefilter', node);
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
    
    var active_editors = filter(function(e){
        return e.type != 'hidden' && !e.disabled
    }, editors);

    forEach(active_editors, function(e){
        MochiKit.Signal.connect(e, 'onkeydown', self, onKeyDown_search);
    });
}

var onKeyDown_search = function(evt) {
	var key = evt.key();
    var src = evt.src();
    
    if (key.string == "KEY_ENTER"){
    	search_filter();
    }
}

var display_Customfilters = function(all_domains, group_by_ctx){

	var filter_table = $('filter_table');
	
	var params = {};
	var record = {};
	
	children = MochiKit.DOM.getElementsByTagAndClassName('tr', 'filter_row_class', filter_table);
	forEach(children, function(ch){
		
		var ids = ch['id'];	// row id...
		var id = ids.split('/')[1];
		var qid = 'qstring/' + id;
		var fid = 'filter_fields/' + id;
		var eid = 'expr/' + id;
		if ($(qid) && $(qid).value) {
			var rec = {};
			rec[$(fid).value] = $(qid).value;
			params['_terp_model'] = openobject.dom.get('_terp_model').value;
		}
		if (rec) {
			record[ids] = rec;
		}
	});
	
	record = serializeJSON(record);
	params['record'] = record;
	var custom_domain = [];
	var search_req = openobject.http.postJSON('/search/get', params);
	search_req.addCallback(function(obj){
		if (obj.error) {
			forEach(children, function(child){
				var cids = child['id']
				var id = cids.split('/')[1];
				var fid = 'filter_fields/' + id;
				if ($(fid).value == obj.error_field) {
					f = fid.split('/')[1];
					$('qstring/'+f).style.background = '#FF6666';
					$('qstring/'+f).value = obj.error;
				}
			});
		}
		if (obj.frm) {
   			for (var i in obj.frm) {
   				var temp_domain = [];
   				var operator = 'None';
   				
				var id = serializeJSON(i).split('/')[1];
				id = parseInt(id, 10);
				
				var fid = 'filter_fields/' + id;
				var eid = 'expr/' + id;
				var select_andor = 'select_andor/' + id;
				var type = obj.frm[i].type;
				
				if($(select_andor)){
					var operator = $(select_andor).value == 'AND'? '&': '|';
				}
				  				
   				if (operator != 'None') {
   					temp_domain.push(operator);
   				}
   				
   				var first_text = obj.frm[i].rec;
   				var expression = $(eid).value;
   				var right_text = obj.frm[i].rec_val;
   				
   				if (expression=='ilike'||expression=='not ilike'){
   					if (type=='integer'||type=='float'||type=='date'||type=='datetime'||type=='boolean'){
   						expression = expression == 'ilike'? '=': '!=';
   					}
   				}
   				if ((expression == '<' || expression == '>') && (type!='integer'||type!='float'||type!='date'||type!='datetime'||type!='boolean')){
   					expression = '=';
   				}
   				if (expression == 'in' || expression == 'not in'){
   					right_text = typeof right_text == 'string'? right_text.split(',') : right_text[right_text.length-1][right_text[right_text.length-1].length-1];
   				}
   				
				temp_domain.push(first_text, expression, right_text);
				custom_domain.push(temp_domain);
   			}
		}
		custom_domain = serializeJSON(custom_domain);
		final_search_domain(custom_domain, all_domains, group_by_ctx);
	});	
}

var group_by = [];

var search_filter = function(src, id) {
	var all_domains = {};
	var check_domain = 'None';
	var domains = {};
	var search_context = {};
	var group_by_ctx = [];
	var all_boxes = [];
	var domain = 'None';
	
	if(src) {
		if(src.checked==false) {
			src.checked = true
			id.className = 'active_filter';
			if(jQuery(src).attr('group_by_ctx')) {
				group_by.push(jQuery(src).attr('group_by_ctx'))
			}
		}
		else {
			src.checked = false
			id.className = 'inactive_filter';
			group_by = jQuery.grep(group_by, function(grp) {
				return grp != jQuery(src).attr('group_by_ctx');
			})
		}
	}
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
			if (getNodeAttribute(d, 'kind') == 'many2one'){
				value = openobject.dom.get(d.name+'_text').value || value;
			}
			domains[d.name] = value;
		}
	});
	
	domains = serializeJSON(domains);
	all_domains['domains'] = domains;
	all_domains['search_context'] =  search_context;
	selected_boxes = getElementsByTagAndClassName('input', 'grid-domain-selector');
	
	forEach(selected_boxes, function(box){
		if (box.id && box.checked && box.value != '[]') {
			all_boxes = all_boxes.concat(box.value);
		}
	});
	
	openobject.dom.get('_terp_group_by_ctx').value = group_by;
	
	checked_button = all_boxes.toString();
	check_domain = checked_button.length > 0? checked_button.replace(/(]\,\[)/g, ', ') : 'None';
	all_domains['check_domain'] = check_domain;
	
	if ($('filter_list')) {
		all_domains['selection_domain'] = $('filter_list').value;
	}
	
	all_domains = serializeJSON(all_domains);
	var fil_dom = openobject.dom.get('_terp_filter_domain');
	if(filter_table.style.display == '' || fil_dom && fil_dom.value != '[]') {
		
		if (filter_table.style.display == 'none'){
			filter_table.style.display = '';
		}		
		display_Customfilters(all_domains, group_by);
	}
	else {
		custom_domain = fil_dom ? fil_dom.value : '[]';		
		final_search_domain(custom_domain, all_domains, group_by);	
	}
}

var final_search_domain = function(custom_domain, all_domains, group_by_ctx) {
	var req = openobject.http.postJSON('/search/eval_domain_filter', 
		{source: '_terp_list',
		model: $('_terp_model').value, 
		custom_domain: custom_domain,
		all_domains: all_domains,
		group_by_ctx: group_by_ctx
	});
	
	req.addCallback(function(obj){
		if (obj.flag) {
			var params = {'domain': obj.sf_dom,
				'model': openobject.dom.get('_terp_model').value,
				'flag': obj.flag};
							
			if(group_by_ctx!=''){
				params['group_by'] = group_by_ctx;
			}				
			openobject.tools.openWindow(openobject.http.getURL('/search/save_filter', params), {
				width: 400,
				height: 250
			});
		}
		
		if (obj.action) { // For manage Filter
			action = serializeJSON(obj.action);
			window.location.href = openobject.http.getURL('/search/manage_filter', {action: action});
		}
		
		if (obj.domain) { // For direct search
			var in_req = eval_domain_context_request({
				source: '_terp_list', 
				domain: obj.domain, 
				context: obj.context
			});
			
			in_req.addCallback(function(in_obj){
		    	openobject.dom.get('_terp_search_domain').value = in_obj.domain;
		    	openobject.dom.get('_terp_search_data').value = obj.search_data;
		    	openobject.dom.get('_terp_context').value = in_obj.context;
		    	openobject.dom.get('_terp_filter_domain').value = obj.filter_domain;
		    	if (getElement('_terp_list') != null){
		    		new ListView('_terp_list').reload();
		    	}
			});	
		}
	});
}

/**
 * @event groupby-toggle triggered when changing the display state of the groupby options
 *  @target #search_filter_data the element holding the filter rows
 *  @argument 'the action performed ("expand" or "collapse")
 */
function expand_group_option(id, event) {
    var groupbyElement = getElement(id);
    var action;
    if (groupbyElement.style.display == '') {
        groupbyElement.style.display = 'none';
        event.target.className = 'group-expand';
        action = 'collapse';
    } else {
        groupbyElement.style.display = '';
        event.target.className = 'group-collapse';
        action = 'expand';
    }
    MochiKit.Signal.signal(
            $('search_filter_data'),
            'groupby-toggle',
            action);
}

MochiKit.DOM.addLoadEvent(function(evt){

	var filter_table = openobject.dom.get('filter_table');
	var fil_dom = openobject.dom.get('_terp_filter_domain');
	if (filter_table){
		if(filter_table.style.display == '' || fil_dom && fil_dom.value != '[]') {
			if(filter_table.style.display == 'none'){
				filter_table.style.display = '';
			}
		}
	}
	onKey_Event(evt);	
});
