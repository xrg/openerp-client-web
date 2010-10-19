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
var OR_LINE = '<tr id="or"><td colspan="5">' +
        '<div class="filter-lsep"></div><hr class="filter-hr">' +
        '<div class="filter-msep">Or</div>' +
        '<div class="filter-rsep"></div><hr class="filter-hr">' +
    '</td></tr>';

function add_filter_row(elem) {

    var $filter_table = jQuery('#filter_table');
    var $filter_opt_tbl = jQuery('#filter_option_table');
    var $cls_tbody = jQuery(elem).closest("tbody");
    var $element = jQuery(elem);
    var selected_txt = $element.find('option:selected').text();

    if ($filter_opt_tbl.find('tbody:visible').length == 1 &&
        $cls_tbody.siblings().length == 1) {
        if($filter_table.is(':hidden')) {
            var $filterlabel = jQuery('#filterlabel');
            if ($filterlabel.text() == '') {
                $filterlabel.text(selected_txt);
                $filterlabel.attr('value', $element.val());
            }
            $filter_table.show();
        }
    } else {
        var $position_tr = $cls_tbody.find('tr:last').prev();
        if ($cls_tbody.prev().attr('id') == 'filter_table') {
            $position_tr = $filter_table.find('tr:last');
        }
        var old_tr = $filter_opt_tbl.find('tbody:first').find('tr.filter_row_class:first');

        var new_tr = old_tr.clone();
        var new_tr_lbl = new_tr.find('#filterlabel');
        new_tr_lbl.text(selected_txt);
        new_tr_lbl.attr('value', $element.val());

        var new_tr_qstring = new_tr.find('input.qstring');
        new_tr_qstring.css('background', '#fff').val('');
        if (new_tr.is(':hidden')) {
            new_tr.show();
        }

        var index_row;
        var $curr_body = $position_tr.closest('tbody');
        $curr_body.find('#filterlabel').each(function(k, v) {

            if (jQuery(v).text() != selected_txt) { return; }
            index_row = k;
            new_tr.find('select.expr').hide();
            new_tr_lbl.hide();
            new_tr.find('label.and_or').remove();
            jQuery('<label>', {'class': 'and_or'}).text('OR').insertBefore(new_tr_qstring);
        });

        if(index_row >= 0) {
            $position_tr = $curr_body.find('tr.filter_row_class')[index_row];
        }
        jQuery($position_tr).after(new_tr);
    }
    
    var select_or = jQuery('select.filter_fields_or');
    if (!select_or.closest("tbody").siblings().length) {
        select_or.attr('disabled', true);
    }else{
        select_or.attr('disabled', false);
    }
}

function addOrBlock(elem){
    var $filter_option_table = jQuery('#filter_option_table');
    $filter_option_table.find('tr:last select.filter_fields_or').parent().hide();

    var $newtbody = jQuery('<tbody>' + OR_LINE + '</tbody>');
    $filter_option_table.append($newtbody);

    var $new_tr = $filter_option_table.find('tr:first').clone();
    $new_tr.find('#filterlabel').attr('value', jQuery(elem).val())
                                .text(jQuery('select.filter_fields_or option:selected').text());
    $new_tr.find('input.qstring').css('background', '#FFF').val('');
    $newtbody.append($new_tr);

    var $action_tr = jQuery('#filter_table').next('tbody.actions').find('tr.actions').clone();
    $action_tr.find('select.filter_fields_or').parent().show();
    $action_tr.find('select.filter_fields_or').attr('disabled', false);
    if ($action_tr.is(':hidden')) {
        $action_tr.show();
    }
    $newtbody.append($action_tr);
}

function collapse_expand(div_id, grp_id, id) {

    jQuery(div_id).toggleClass('group-collapse group-expand');
    jQuery(grp_id).toggle();
    if (id)
        jQuery(id).css('display', 'block');
}

function switch_searchView(d) {

    var domain = eval(d);
    var operators = [];
    var tbodys = [];
    var trs = 0;
    var $tbody = jQuery("<tbody/>");
    var prev_row_field = '';
    var $filter_opt_tbl = jQuery('#filter_option_table');
    var $old_tr = $filter_opt_tbl.find('tbody:first tr.filter_row_class:first');
    var $action_tbody = $filter_opt_tbl.find('tbody.actions');
    var $selection_options =  $action_tbody.find('tr.actions select.filter_fields_and:first');

    jQuery('#filter_table').hide();

    for (var i=0; i<domain.length; i++) {

        var item = domain[i];
        if (item.length==1) {
            operators.push(item);
        }
        else {
            var $new_tr = $old_tr.clone();
            var $new_tr_lbl = $new_tr.find('#filterlabel');
            $new_tr_lbl.attr('value', item[0]).text(
                    $selection_options.find('option[value='+ item[0] + ']').text());
            $new_tr.find('select.expr').val(item[1]);

            var $new_tr_qstr = $new_tr.find('input.qstring');
            $old_tr.find('input.qstring').css('background', '#FFF').val('');
            $new_tr_qstr.attr('value', item[2]);

            if (trs==0 || operators[operators.length-1]=='&') {
                $tbody.append($new_tr);
                if (trs>0)
                    operators.splice(operators.length-1, 1);
            }
            else if(prev_row_field!=item[0] && operators[operators.length-1]=='|') {
                tbodys.push($tbody);
                $tbody = jQuery("<tbody/>");
                $tbody.append($new_tr);
                trs = 1;
                operators.splice(operators.length-1, 1);
            }
            else if(prev_row_field==item[0] && operators[operators.length-1]=='|') {
                $new_tr_lbl.hide();
                $new_tr.find('select.expr').hide();
                jQuery('<label class="and_or">OR</label>').insertBefore($new_tr_qstr);
                $tbody.append($new_tr);
                operators.splice(operators.length-1, 1);
            }
            trs ++;
            prev_row_field = item[0];
        }
    }

    if (domain.length){
        tbodys.push($tbody);
        collapse_expand('#filters', '#filter_option_table');
        if ($action_tbody.is(':visible')){
            $action_tbody.hide();
        }
    }

    for (var j=0; j<tbodys.length; j++) {

        if (tbodys[j + 1]) {
            var $trOr = jQuery(OR_LINE);
            tbodys[j + 1].prepend($trOr);
        }
        if (tbodys[j - 1]) {
            tbodys[j - 1].find('tr.actions td#filter_column').hide();
        }

        var $actTr = $action_tbody.find('tr.actions').clone(true);
        $actTr.find('select#filter_fields_or').attr('disabled', false);
        tbodys[j].append($actTr);
        $filter_opt_tbl.append(tbodys[j]);
    }
}

function remove_filter_row(element) {
    var $node = jQuery(element).closest('tr');
    var $tby = $node.closest('tbody');
    var $filter_opt_tbl = jQuery('#filter_option_table');

    if ($tby.find('tr.filter_row_class').length <= 1 && $tby.attr('id')!='filter_table') {
        var $prev_body = $tby.prev();
        if(!($tby.next().length && $prev_body.length)) {
            $prev_body.find('td#filter_column').show();
        }

        $tby.remove();
        if ($filter_opt_tbl.find('tbody:visible').length == 2 ) {
            var $body_next = $filter_opt_tbl.find('tbody:first');
            $body_next.find('#or').remove();
        }
    }

    if($node.is(':only-child')) {
        var $filter_table = jQuery('#filter_table');
        if ($filter_opt_tbl.find('tbody:visible').length && $node.closest("tbody").siblings().length > 1){
            $filter_table.next().hide();
            $filter_opt_tbl.find('tr#or:first').hide();
        }

        $node.find('input.qstring').css('background', '#FFF').val('');
        jQuery('#filterlabel').attr('value', '').text('');
        jQuery('select#filter_fields_or').attr('disabled', true);
        $filter_table.hide();
    } else {
        if($node.is(':last-child')) {
            $node.prev().find('.and_or').remove();
        }

        if($node.next().find('label.and_or').is(':visible')){
             $node.next().remove();
        } else{
            if ($filter_opt_tbl.find('tbody:visible').length == 0) {
                jQuery('tbody.actions').show()
                                       .find('tr.actions td#filter_column').show();
            }

            if ($filter_opt_tbl.find('tbody:visible').length == 1){
                $filter_opt_tbl.find('tr#or:first').hide();
            }
            $node.remove();
        }
    }
}

/**
 * Checks if a type is considered order-able, so that we can setup the right search operators for the operand
 * @param type the field's type to consider for operator replacement
 */
function isOrderable(type) {
    return jQuery.inArray(type, ['integer', 'float', 'date', 'datetime', 'boolean']) != -1;
}

/**
 * To return the keys of an object. use jQuery.keys(obj).
*/
jQuery.extend({
    keys: function(obj){
        var a = [];
        $.each(obj, function(k){ a.push(k) });
        return a;
    }
});

function display_Customfilters(all_domains, group_by_ctx) {
    var Allrecords = {};
    jQuery('#filter_option_table > tbody').each(function () {
        var record = {};
        var pid = jQuery(this).index();

        jQuery(this).children('.filter_row_class').each(function () {
            var $constraint_value = jQuery(this).find('input.qstring');
            var $fieldname = jQuery(this).find('#filterlabel');
            var id = jQuery(this).parent().find('> .filter_row_class').index(this);

            if($constraint_value.val()) {
                var rec = {};
                rec[$fieldname.attr('value')] = $constraint_value.val();
                record[id] = rec;
            }
        });

        if (jQuery.keys(record).length != 0){
            Allrecords[pid] = record;
        }
    });

    openobject.http.postJSON('/openerp/search/get', {
        record: serializeJSON(Allrecords),
        _terp_model: jQuery('#_terp_model').val()
    }).addCallback(function(obj) {
        var custom_domain = [];
        if(obj.error) {
            jQuery('#filter_option_table tbody > .filter_row_class').each(function () {
                if(jQuery(this).find('#filterlabel').attr('value') == obj['error_field']) {
                    jQuery(this).find('input.qstring').css('background', '#f66').val(obj.error);
                }
            });
        }
        var form_result = obj.frm;
        var tbody_keys = jQuery.keys(form_result);

        if(form_result) {
            // By property, we get incorrect ordering
            for(var ind=0; ind<tbody_keys.length ;ind++){
                var All_domain = [];
                var group = [];
                var tbody_frm_ind = form_result[tbody_keys[ind]]; //tbody dictionary
                var trs_keys = jQuery.unique(jQuery.keys(tbody_frm_ind)); //sort trs

                for(var index = 0; index<trs_keys.length ; index++) {
                    var return_record = tbody_frm_ind[trs_keys[index]];
                    var $curr_body = jQuery('#filter_option_table > tbody').eq(tbody_keys[ind]);
                    var $row = $curr_body.find('> .filter_row_class').eq(trs_keys[index]);
                    var $next_row = [];

                    if ($row.next('tr.filter_row_class').find('input.qstring').val() != ''){
                        $next_row = jQuery($row.next());
                    }

                    var type = return_record.type;
                    var temp_domain = [];
                    var grouping = $next_row.length != 0 ? $next_row.find('label.and_or').text(): null;

                    if (group.length==0) {
                        var $new_grp = $curr_body.find('tr.filter_row_class:gt('+trs_keys[index]+')')
                                                 .find('td#filter_column:not(:has(label)) input.qstring[value]');
                        if ($new_grp.length){
                            group.push('&')
                        }
                    }
                    if(grouping) {
                        temp_domain.push(grouping == 'AND' ? '&' : '|');                        
                    }

	                var field = return_record['rec'];
	                var comparison = $row.find('select.expr').val();	                
	                var value = return_record['rec_val'];

	                switch (comparison) {
	                    case 'ilike':
	                    case 'not ilike':
	                        if(isOrderable(type)) {
	                            comparison = (comparison == 'ilike' ? '=' : '!=');
	                        }
	                        break;
	                    case '<':
	                    case '>':
	                        if(!isOrderable(type)) {
	                            comparison = '=';
	                        }
	                        break;
	                    case 'in':
	                    case 'not in':
	                        if(typeof value == 'string') {
	                            value = value.split(',');
	                        } else {
	                            /* very weird array-type construct
	                               looks a bit like [[6, 0, [list of ids here]]]
	                             */
	                            value = value[value.length - 1][value[value.length - 1].length - 1]
	                        }
	                        break;
	                }
	                
	                if ($row.find('label.and_or').length>0 || grouping){                       
                        temp_domain.push(field, comparison, value);
                        group.push(temp_domain);
                    }
                    else{
                        group.push(field, comparison, value)
                    }

                    if (!grouping) {             
                        All_domain.push(group);                        
                        group = [];
                    }     	                
	            }

	            if (All_domain.length) {
	               custom_domain.push(All_domain);
                }
            }
        }
        final_search_domain(serializeJSON(custom_domain), all_domains, group_by_ctx);
    });
}

var group_by = new Array();
var filter_context = [];
var previous_filter = 0;
function parse_filters(src, id) {
    var all_domains = {};
    var check_domain = 'None';
    var domains = {};
    var search_context = {};
    var all_boxes = [];
    var $filter_list = jQuery('#filter_list');
    var domain = 'None';
    if (jQuery('div.group-data').length) {
        jQuery('div.group-data:first').find('button').each(function(){
            if (jQuery(this).hasClass('active')) {
                var _grp = jQuery(this).next('input').attr('group_by_ctx');
                if (jQuery.inArray(_grp, group_by) < 0) {
                    group_by.push(_grp)
                }
            }
        })
    }
    if ($filter_list) {
        all_domains['selection_domain'] = $filter_list.val();
        var selected_index = $filter_list.attr('selectedIndex');
        var filter_grps = jQuery('#filter_list option:selected').attr('group_by');
        if(selected_index > 0) {
            if(filter_grps && filter_grps!='[]') {
                group_by = eval(filter_grps);
            } else {
                if(selected_index != previous_filter && group_by.length)
                    group_by = [];
            }
        } else {
            if (previous_filter > 0) {
                group_by = [];
            }
        }
        previous_filter = selected_index;
    }
    if(src) {
        var $source = jQuery(src);
        if(jQuery(id).hasClass('inactive')) {
            $source.closest('td').addClass('grop_box_active');
            jQuery(src).attr('checked', true);
            if($source.attr('group_by_ctx') &&
               $source.attr('group_by_ctx') != 'False') {
                group_by.push($source.attr('group_by_ctx'));
            }

            if($source.attr('filter_context') &&
               $source.attr('filter_context') != '{}') {
                filter_context.push($source.attr('filter_context'));
            }
        } else {
            $source.closest('td').removeClass('grop_box_active');
    		$source.attr('checked', false);
    		
    		group_by = jQuery.grep(group_by, function(grp) {
                return grp != $source.attr('group_by_ctx');
            });
            
            if($source.attr('filter_context') &&
               $source.attr('filter_context')!='{}') {
                var filter_index = jQuery.inArray(
                    $source.attr('filter_context'), filter_context);
                if(filter_index >= 0) {
                    filter_context.splice(filter_index, 1);
                }
            }
    	}
        jQuery(id).toggleClass('active inactive');
    }
    var $all_search_fields = jQuery('#search_filter_data').find("input[name]:not([type=checkbox]):not([value='']), select[name]");
    jQuery('#_terp_filters_context').val(filter_context);
    $all_search_fields.each(function(fld_index, fld){
        var $fld = jQuery(fld);
        var kind = $fld.attr('kind');
        var fld_value = $fld.val();
        if(kind == 'selection') {
            if ($fld.val() != '') {
                fld_value = 'selection_'+$fld.val();

                if ($fld.attr('search_context')) {
                    search_context['context'] = $fld.attr('search_context');
                    search_context['value'] = fld_value;
                }
            }
        } else if(kind == 'many2one') {
            var m2o = $fld.attr('name');
            fld_value = jQuery('[id="'+m2o+'_text'+'"]').val() || fld_value;
            if($fld.attr('m2o_filter_domain')){
                fld_value = 'm2o_'+ fld_value;
            }
        }
        
        if(fld_value && fld_value!='')
            domains[$fld.attr('name')] = fld_value;
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

    if(checked_button.length) {
        check_domain = checked_button.length > 0? checked_button.replace(/(],\[)/g, ', ') : 'None';
        all_domains['check_domain'] = check_domain;
    }
    all_domains = serializeJSON(all_domains);
    return all_domains;
}

function search_filter(src, id) {
    var all_domains = parse_filters(src, id);
    if(jQuery('#filter_table').is(':visible') || jQuery('#_terp_filter_domain').val() != '[]') {
        display_Customfilters(all_domains, group_by);
    } else {
        var custom_domain = jQuery('#_terp_filter_domain').val() || '[]';
        final_search_domain(custom_domain, all_domains, group_by);
    }
}

function save_filter() {
    var domain_list = parse_filters();
    var grps = group_by;
    var selectedFilter = jQuery('#filter_list option:selected');
    var selected_filter = selectedFilter.index() > 0 ? selectedFilter.text(): '';

    if(group_by.length)
        grps = group_by.join(',');

    var custom_domain = jQuery('#_terp_filter_domain').val() || '[]';
    openobject.http.postJSON('/openerp/search/eval_domain_filter', {
        'all_domains': domain_list,
        'source': '_terp_list',
        'group_by_ctx': grps}).addCallback(function(obj) {
        var sf_params = {'model': jQuery('#_terp_model').val(), 'domain': obj.domain, 'group_by': grps, 'flag': 'sf',
                         'custom_filter':custom_domain, 'selected_filter': selected_filter};

        jQuery.ajax({
            url:'/openerp/search/save_filter',
            dataType: 'html',
            type: 'POST',
            data: sf_params,
            success: function(xhr) {
                jQuery.fancybox(xhr, {showCloseButton: false})
            }
        });
    });
}

function manage_filters() {
    openLink(openobject.http.getURL('/openerp/search/manage_filter', {
        'model': jQuery('#_terp_model').val()}));
}

function final_search_domain(custom_domain, all_domains, group_by_ctx) {
	var waitBox = new openerp.ui.WaitBox();
    if(group_by_ctx.length)
        group_by_ctx = group_by_ctx.join(',');
	waitBox.showAfter(500);
	jQuery.ajax({
		url: '/openerp/search/eval_domain_filter',
		type: 'POST',
		dataType: 'json',
		data:{source: '_terp_list',
			model: jQuery('#_terp_model').val(),
			custom_domain: custom_domain,
			all_domains: all_domains,
			group_by_ctx: group_by_ctx
			},
		complete: jQuery.proxy(waitBox, 'hide'),
		success: function(obj) {
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
			    	jQuery('#_terp_group_by_ctx').val(in_obj.group_by);
                    
                    var $search_callback = jQuery('#_terp_search_callback');
                    
                    if($search_callback.length) {
                        window[$search_callback.val()]();
                    } else {
                        new ListView('_terp_list').reload();
                    }
				});
			 }
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
