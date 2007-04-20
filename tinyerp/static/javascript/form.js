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

var inlineEdit = function(id, o2m_name){

    form = $('view_form');

    act = '/form/edit';

    if (o2m_name) {
        n = o2m_name.replace('.', '/') + '/_terp_id';
        terp_id = document.getElementsByName(n)[0];
        terp_id.value = id;

        act = getURL(act, {_terp_one2many: o2m_name});

    } else {
        form._terp_id.value = id;
    }

    form.action = act;
    form.submit();
}

var inlineDelete = function(id, o2m_name){

    if (!confirm('Do you realy want to delete this record?')) {
        return false;
    }

    form = $('view_form');

    act = '/form/delete';

    if (o2m_name) {
        n = o2m_name.replace('.', '/') + '/_terp_id';
        terp_id = document.getElementsByName(n)[0];
        terp_id.value = id;

        act = getURL(act, {_terp_one2many: o2m_name});

    } else {
        form._terp_id.value = id;
    }

    form.action = act;
    form.submit();
}

var submit_form = function(action, o2m){

    form = $("view_form");

    if (action == 'delete' &&  !confirm('Do you realy want to delete this record?')) {
        return false;
    }

    act = '/form/' + action;

    if (o2m) {
        act = getURL(act, {_terp_one2many: o2m.name});
    }

    form.action = act;
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
    form.action = getURL('/form/save', params);
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

    req = doSimpleXMLHttpRequest(getURL('/form/on_change', vals));

    req.addCallback(function(xmlHttp){
        res = evalJSONRequest(xmlHttp);
        values = res['value'];

        for(var k in values){
            fld = $(prefix + k);

            if (fld) {
                value = values[k];
                value = value === false || value === null ? '' : value

                if (fld.value != value) {
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
        var req = doSimpleXMLHttpRequest(getURL('/many2one/get_name', {model: relation, id : value_field.value}));

        req.addCallback(function(xmlHttp){
            var res = evalJSONRequest(xmlHttp);
            text_field.value = res['name'];
        });
    }
}
