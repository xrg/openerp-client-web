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

function get_form_action(action, params){
	var act = typeof(form_controller) == 'undefined' ? '/form' : form_controller;
	return getURL(act + '/' + action, params);
}

var inlineEdit = function(id, src){

    form = $('view_form');

    act = get_form_action('edit');

    if (src) {
        n = src.replace('.', '/') + '/_terp_id';
        terp_id = document.getElementsByName(n)[0];
        terp_id.value = id;

        act = get_form_action('edit', {_terp_source: src, _terp_inline: 1});

    } else {
        form._terp_id.value = id;
    }

    form.action = act;
    form.submit();
}

var inlineDelete = function(id, src){

    if (!confirm('Do you realy want to delete this record?')) {
        return false;
    }

    form = $('view_form');

    act = get_form_action('delete');

    if (src) {
        n = src.replace('.', '/') + '/_terp_id';
        terp_id = document.getElementsByName(n)[0];
        terp_id.value = id;

        act = get_form_action('delete', {_terp_source: src});

    } else {
        form._terp_id.value = id;
    }

    form.action = act;
    form.submit();
}

var submit_form = function(action, src, data){

    if (action == 'delete' &&  !confirm('Do you realy want to delete this record?')) {
        return false;
    }

    form = $("view_form");
    source = src ? (typeof(src) == "string" ? src : src.name) : null;

    if (action == 'action' && $('_terp_list')){
    	var list = new ListView('_terp_list');
    	var boxes = list.getSelected();

    	form._terp_id.value = map(function(b){return b.value}, boxes);
    }

    form.action = get_form_action(action, {_terp_source: source, _terp_data: data ? data : null});
    form.submit();
}

var submit_search_form = function(action) {

	if ($('search_view_notebook')) {

	    // disable fields of hidden tab

	    var hidden_tab = getElementsByTagAndClassName('div', 'tabbertabhide', 'search_view_notebook')[0];
	    var disabled = [];

	    disabled = disabled.concat(getElementsByTagAndClassName('input', null, hidden_tab));
	    disabled = disabled.concat(getElementsByTagAndClassName('textarea', null, hidden_tab));
	    disabled = disabled.concat(getElementsByTagAndClassName('select', null, hidden_tab));

	    forEach(disabled, function(fld){
	        fld.disabled = true;
	    });
	}

	submit_form(action ? action : 'find');
}

var submit_value = function(action, src, data){

    form = $("view_form");
    source = src ? (typeof(src) == "string" ? src : src.name) : null;

    form.action = '/openm2o/save';
    form.submit();
}

var buttonClicked = function(name, btype, model, id, sure){

    if (sure && !confirm(sure)){
        return;
    }

    params = {};

    params['_terp_button/name'] = name;
    params['_terp_button/btype'] = btype;
    params['_terp_button/model'] = model;
    params['_terp_button/id'] = id;

    form = $("view_form");
    form.action = get_form_action('save', params);
    form.submit();
}

/**
 * This function will be used by widgets that has `onchange` trigger is defined.
 *
 * @param name: name/instance of the widget
 */
var onChange = function(name) {

    var caller = $(name);
    var callback = getNodeAttribute(caller, 'callback');

    var prefix = caller.name.split("/");
    prefix.pop();
    prefix = prefix.join("/");
    prefix = prefix ? prefix + '/' : '';

    var model = document.getElementsByName(prefix + '_terp_model')[0].value;

    form = $("view_form");

    vals = {};
    forEach(form.elements, function(e){
        if (e.name && e.name.indexOf('_terp_') == -1 && e.type != 'button'){
            vals['_terp_parent_form/' + e.name] = e.value;
            if (e.attributes['kind']){
                vals['_terp_parent_types/' + e.name] = getNodeAttribute(e, 'kind');
            }
        }
    });

    if (!callback)
        return;

    vals['_terp_caller'] = caller.id;
    vals['_terp_callback'] = callback;
    vals['_terp_model'] = model;

    req = Ajax.post('/form/on_change', vals);

    req.addCallback(function(xmlHttp){
        res = evalJSONRequest(xmlHttp);
        values = res['value'];
		for(var k in values){
			flag = false;
            fld = $(prefix + k);
            if (fld) {
                value = values[k];
                value = value === false || value === null ? '' : value

				if ($(prefix + k + '_id')){
                	fld = $(prefix + k + '_id');
                	flag = true;
                }

                if ((fld.value != value) || flag) {
                	fld.value = value;
                    if (typeof fld.onchange != 'undefined'){
                        fld.onchange();
            	     }
               	}
            }
        }
    });
}

/**
 * This function will be used by many2one field to get display name.
 *
 * @param name: name/instance of the widget
 * @param relation: the TinyERP model
 *
 * @return string
 */
function getName(name, relation){

    var value_field = $(name);
    var text_field = $(value_field.name + '_text');

    if (value_field.value == ''){
        text_field.value = ''
    }

    if (value_field.value){
        var req = Ajax.get('/search/get_name', {model: relation, id : value_field.value});

        req.addCallback(function(xmlHttp){
            var res = evalJSONRequest(xmlHttp);
            text_field.value = res['name'];
        });
    }
}

function eval_domain_context_request(options){

	var prefix = options.source.split("/");
    prefix.pop();
    
	var form = $('view_form');
	var params = {'_terp_domain': options.domain, '_terp_context': options.context, '_terp_prefix': prefix};
	
    forEach(form.elements, function(e){

        if (e.name && e.name.indexOf('_terp_') == -1 && e.type != 'button') {

           	var n = n = '_terp_parent_form/' + e.name;
           	var v = e.value;

            params[n] = v;

            if (e.attributes['kind']){

                n = '_terp_parent_types/' + e.name;
                v = e.attributes['kind'].value;

                params[n] = v;
          	}
    	}
    });
    
    return Ajax.post('/search/eval_domain_and_context', params);	
}

function open_search_window(relation, domain, context, source, kind, text) {

	if (text || (domain == '' || domain == '[]') && (context == '' || context == '{}')){
		return wopen(getURL('/search/new', {model: relation, domain: '[]', context: '{}', source: source, kind: kind, text: text}), 'search_window', 800, 600);
	}
	
	var req = eval_domain_context_request({source: source, domain: domain, context: context});
	
	req.addCallback(function(xmlHttp){
    	var res = evalJSONRequest(xmlHttp);
		wopen(getURL('/search/new', {model: relation, domain: res.domain, context: res.context, source: source, kind: kind, text: text}), 'search_window', 800, 600);
    });
}
