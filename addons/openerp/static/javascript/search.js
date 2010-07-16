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
 *  @target #filter_table the element holding the filter rows
 *  @argument 'the newly added (or showed for first row?) filter row'
 */
function reset_id(element, current_row_id) {
    element = jQuery(element);
    return element.attr('id', element.attr('id').split('/')[0] + '/' + current_row_id);
}
function row_sequence(element) {
    return parseInt(element.attr('id').split('/')[1], 10);
}
function add_filter_row() {
    var filter_table = jQuery('#filter_table');
    var vals = ['AND', 'OR'];

    if(filter_table.is(':hidden')) {
        filter_table.show();
    } else {
        var old_tr = filter_table.find('tr:last');
        old_tr.find('input.qstring').css('background', '#FFF');

        var new_tr = old_tr.clone();
        var old_sequence = row_sequence(new_tr);
        // create id for new row
        var current_row_sequence = old_sequence + 1;
        reset_id(new_tr, current_row_sequence);

        var qstring = new_tr.find('input.qstring').css('background', '#fff').val('');
        jQuery('td.filter_column, select.filter_fields, select.expr, td.image_col', new_tr).add(qstring).each(
                function (index, element) {
                    reset_id(element, current_row_sequence);
                });

        var and_or = jQuery('<td>', {'id': 'and_or/' + old_sequence, 'class': 'and_or'}).appendTo(old_tr);

        var select_andor = jQuery('<select>', {
            'id': 'select_andor/' + old_sequence,
            'class': 'select_andor'
        }).appendTo(and_or);
        jQuery.each(vals, function (index, label) {
            select_andor.append(jQuery('<option>').val(label).text(label));
        });

        old_tr.after(new_tr);
    }
}

/**
 *  @target #filter_table the element holding the filter rows
 *  @argument 'the removed (or hidden) filter row'
 */
function remove_filter_row(element) {
    var node = jQuery(element).closest('tr');
    if(node.is(':only-child')) {
        node.find('[id^=qstring]').css('background', '#FFF').val('');
        jQuery('#filter_table').hide();
    } else {
        if(node.is(':last-child')) {
            node.prev().find('[id^=and_or]').remove();
        }
        node.remove();
    }
}

function display_Customfilters(all_domains, group_by_ctx){

    var params = {};
	var record = {};

    jQuery('#filter_table tr.filter_row_class').each(function () {
		var ids = this.id;	// row id...
		var id = ids.split('/')[1];
		var qid = 'qstring/' + id;
		var fid = 'filter_fields/' + id;

        var rec = null;
		if ($(qid) && $(qid).value) {
			rec = {};
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
	var search_req = openobject.http.postJSON('/openerp/search/get', params);
	search_req.addCallback(function(obj){
		if (obj.error) {
			forEach(children, function(child){
				var cids = child['id'];
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

var group_by = new Array();
var filter_context = [];

function parse_filters(src, id) {
    var all_domains = {};
    var check_domain = 'None';
    var domains = {};
    var search_context = {};
    var all_boxes = [];
    var domain = 'None';
    
    var check_groups = jQuery('#_terp_group_by_ctx').val();
    if(check_groups!='[]') {
        check_groups = eval(check_groups);
        for(i in check_groups) {
            if(jQuery.inArray(check_groups[i], group_by) < 0) {
                group_by.push(check_groups[i])
            }
        }   
    }
    if(src) {
        var source = jQuery(src);
        if(jQuery(id).hasClass('inactive')) {
            source.closest('td').addClass('grop_box_active');
            jQuery(src).attr('checked', true);
            if(source.attr('group_by_ctx') && source.attr('group_by_ctx') != 'False') {
                group_by.push(source.attr('group_by_ctx'));
            }

            if(source.attr('filter_context') && source.attr('filter_context') != '{}') {
                filter_context.push(source.attr('filter_context'));
            }
        } else {
            source.closest('td').removeClass('grop_box_active');
    		jQuery(src).attr('checked', false);
    		
    		group_by = jQuery.grep(group_by, function(grp) {
                return grp != source.attr('group_by_ctx');
            });
            
            if(source.attr('filter_context') && source.attr('filter_context')!='{}') {
                var filter_index = jQuery.inArray(source.attr('filter_context'), filter_context);
                if(filter_index >= 0) {
                    filter_context.splice(filter_index, 1);
                }
            }
    	}
        jQuery(id).toggleClass('active inactive');
    }
    
    jQuery('#_terp_filters_context').val(filter_context);
    
    var filter_table = getElement('filter_table');
    forEach($$('[name]', 'search_filter_data'), function(d) {
        var value;
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
    var selected_boxes = getElementsByTagAndClassName('input', 'grid-domain-selector');
    
    forEach(selected_boxes, function(box){
        if (box.id && box.checked && box.value != '[]') {
            all_boxes = all_boxes.concat(box.value);
        }
    });
    
    var checked_button = all_boxes.toString();
    check_domain = checked_button.length > 0? checked_button.replace(/(]\,\[)/g, ', ') : 'None';
    all_domains['check_domain'] = check_domain;
    
    if (openobject.dom.get('filter_list')) {
        all_domains['selection_domain'] = jQuery('#filter_list').val();
    }
    
    all_domains = serializeJSON(all_domains);
    return all_domains;
}

function search_filter(src, id) {
    var all_domains = parse_filters(src, id);
    var filters = jQuery('#filter_table');
    if(filters.is(':visible') || jQuery('#_terp_filter_domain').val() != '[]') {
        if (filters.is(':hidden')){
            filters.show();
        }
        display_Customfilters(all_domains, group_by);
    } else {
        var custom_domain = jQuery('#_terp_filter_domain').val() || '[]';
        final_search_domain(custom_domain, all_domains, group_by);
    }
}

function save_filter() {
    var domain_list = parse_filters();
    var custom_domain = jQuery('#_terp_filter_domain').val() || '[]';
    var req = openobject.http.postJSON('/openerp/search/eval_domain_filter', {
        'all_domains': domain_list,
        'source': '_terp_list',
        'custom_domain': custom_domain,
        'group_by_ctx': group_by});
    req.addCallback(function(obj) {
        var sf_params = {'model': jQuery('#_terp_model').val(), 'domain': obj.domain, 'group_by': group_by, 'flag': 'sf'};
        openobject.tools.openWindow(openobject.http.getURL('/openerp/search/save_filter', sf_params), {
                width: 500,
                height: 240
            });
    });
    
}

function manage_filters() {
    openLink(openobject.http.getURL('/openerp/search/manage_filter', {
        'model': jQuery('#_terp_model').val()}));
}

function final_search_domain(custom_domain, all_domains, group_by_ctx) {
	var req = openobject.http.postJSON('/openerp/search/eval_domain_filter', 
		{source: '_terp_list',
		model: jQuery('#_terp_model').val(), 
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
			openobject.tools.openWindow(openobject.http.getURL('/openerp/search/save_filter', params), {
				width: 400,
				height: 250
			});
		}
		
        if (obj.action) { // For manage Filter
            openLink(openobject.http.getURL('/openerp/search/manage_filter', {
                action: serializeJSON(obj.action)}));
        }
		
		if (obj.domain) { // For direct search
			var in_req = eval_domain_context_request({
				source: '_terp_list', 
				domain: obj.domain, 
				context: obj.context,
				group_by_ctx: group_by_ctx
			});
			
			in_req.addCallback(function(in_obj){
		    	openobject.dom.get('_terp_search_domain').value = in_obj.domain;
		    	openobject.dom.get('_terp_search_data').value = obj.search_data;
		    	openobject.dom.get('_terp_context').value = in_obj.context;
		    	openobject.dom.get('_terp_filter_domain').value = obj.filter_domain;
		    	jQuery('#_terp_group_by_ctx').val(in_obj.group_by)
		    	if (getElement('_terp_list') != null){
		    		new ListView('_terp_list').reload();
		    	}
			});	
		}
	});
}

var ENTER_KEY = 13;
function search_on_return(e) {
    if (e.which == ENTER_KEY){
        // Avoid submitting form when using RETURN on a random form element
        if(!jQuery(e.target).is('button')) {
            e.preventDefault();
        }
    	search_filter();
    }
}
function initialize_search() {
    var filter_table = jQuery('#filter_table');
    var fil_dom = jQuery('#_terp_filter_domain');

    if((filter_table.length && filter_table.is(':hidden')) &&
            (fil_dom.length && fil_dom.val() != '[]')) {
        filter_table.show();
    }
    jQuery('#search_filter_data').keydown(search_on_return);
}
jQuery(document).ready(initialize_search);
