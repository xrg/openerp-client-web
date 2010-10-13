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
// -   All names, links and logos of Tiny, OpenERP and Axelor must be
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

var form_controller;
function get_form_action(action, params){
    var act = typeof(form_controller) == 'undefined' ? '/openerp/form' : form_controller;
    act = action && action.indexOf('/') == 0 ? action : act + '/' + action;
    return openobject.http.getURL(act, params);
}

function openRecord(id, src, target, readonly){

    var kind = getNodeAttribute(src + '_set', 'kind');

    if (!kind && openobject.dom.get('_o2m_' + src)) {
        kind = "one2many";
    }

    if (kind == "one2many") {
        new One2Many(src).edit(id, readonly);
        return;
    }

    var prefix = src && src != '_terp_list' ? src + '/' : '';

    var args = {
        'model': openobject.dom.get(prefix + '_terp_model').value,
        'id': id || 'False',
        'ids': openobject.dom.get(prefix + '_terp_ids').value,
        'view_ids': openobject.dom.get(prefix + '_terp_view_ids').value,
        'view_mode': openobject.dom.get(prefix + '_terp_view_mode').value,
        'domain': openobject.dom.get(prefix + '_terp_domain').value,
        'context': openobject.dom.get(prefix + '_terp_context').value,
        'offset': openobject.dom.get(prefix + '_terp_offset').value,
        'limit': openobject.dom.get(prefix + '_terp_limit').value,
        'count': openobject.dom.get(prefix + '_terp_count').value,
        'search_domain': jQuery('#_terp_search_domain').val() || null,
        'search_data': jQuery('#_terp_search_data').val() || null,
        'filter_domain': jQuery('#_terp_filter_domain').val() || [],
        'notebook_tab': jQuery('#_terp_notebook_tab').val() || 0
    };

    var action = readonly ? 'view' : 'edit';

    if (target == '_blank') {
        window.open(get_form_action(action, args));
        return;
    }

    if (kind == 'many2many') {
        args['source'] = src;
        openobject.tools.openWindow(get_form_action('/openerp/openm2m/edit', args));
        return;
    }

    openLink(get_form_action(action, args));
}

function editRecord(id, src, target){
    return openRecord(id, src, target, false);
}

function viewRecord(id, src){
    return openRecord(id, src, null, true);
}

function editSelectedRecord(){

    var lst = new ListView('_terp_list');
    var ids = lst.getSelectedRecords();

    if (ids && ids.length > 5) {
        var msg = _('You selected to open %(tabs)s tabs - do you want to continue?');
        msg = msg.replace('%(tabs)s', ids.length);
        if (!confirm(msg)) {
            return;
        }
    }

    forEach(ids, function(id){
        editRecord(id, '_terp_list', '_blank');
    });
}

function switchView(view_type, src){
	if (view_type=='diagram' && !jQuery('#_terp_ids').val()) {
    	alert('There are no records to display diagram view.')
    	return;
    }

    var args = {
        '_terp_source': src,
        '_terp_source_view_type': view_type
    }

    if (openobject.dom.get('_terp_list')) {
        var ids = new ListView('_terp_list').getSelectedRecords();
        if (ids.length > 0) {
            openobject.dom.get('_terp_id').value = ids[0];
        }
    }
    var get_action = validate_action('switch', args);
    submit_form(get_action);
}

function switch_O2M(view_type, src){

    if (openobject.http.AJAX_COUNT > 0) {
        return;
    }

    var prefix = src ? src + '/' : '';
    var form = document.forms['view_form'];

    var params = getFormParams();

    params['_terp_source'] = src;
    params['_terp_source_view_type'] = view_type;
    params['_terp_editable'] = $(prefix + '_terp_editable').value;

    if (openobject.dom.get('_terp_list')) {
        var ids = new ListView('_terp_list').getSelectedRecords();
        if (ids.length > 0) {
            openobject.dom.get('_terp_id').value = ids[0];
        }
    }

    var req = openobject.http.post('/openerp/form/switch_o2m', params);
    req.addCallback(function(xmlHttp){

        var text = xmlHttp.responseText;
        if (text.indexOf('ERROR: ') == 0) {
            text = text.replace('ERROR: ', '');
            return error_display(text);
        }

        var frm = openobject.dom.get('_o2m_' + src);

        var d = DIV();
        d.innerHTML = text;

        var newo2m = d.getElementsByTagName('table')[0];

        swapDOM(frm, newo2m);

        var ua = navigator.userAgent.toLowerCase();

        if ((navigator.appName != 'Netscape') || (ua.indexOf('safari') != -1)) {
            // execute JavaScript
            var scripts = openobject.dom.select('script', newo2m);
            forEach(scripts, function(s){
                eval(s.innerHTML);
            });
        }
    });
}

function validate_required(form){

    if (typeof form == 'string') {
        form = jQuery('#' + form).get(0);
    }

    if (!form) {
        return true;
    }

    var elements = MochiKit.Base.filter(function(el){
        return !el.disabled && el.id && el.name && el.id.indexOf('_terp_listfields/') == -1 && hasElementClass(el, 'requiredfield');
    }, form.elements);

    var result = true;

    for (var i = 0; i < elements.length; i++) {
        var elem = elements[i];
        var elem2 = elem;
        var value = elem.value;
        var kind = jQuery(elem).attr('kind');

        if (kind == 'many2many') {
            elem2 = openobject.dom.get(elem.name + '_set') || elem;
            value = value == '[]' ? '' : value;
        }

        if (kind == 'many2one' || kind == 'reference') {
            elem2 = openobject.dom.get(elem.id + '_text') || elem;
        }

        if (!value) {
            jQuery(elem2).addClass('errorfield');
            result = false;
        }
        else
            if (jQuery(elem2).hasClass('errorfield')) {
                jQuery(elem2).removeClass('errorfield');
            }
    }

    if (!result) {
        error_display(_("Invalid form, correct red fields."));
    }
    return result;
}

function error_display(msg) {
    var error = jQuery("<table>",{'width': '100%', 'height': '100%'}
                ).append(
                    jQuery("<tr>").append(
                        jQuery("<td>", {'colspan': 2, 'class': 'error_message_header'}).text('Warning Message')
                    ),
                    jQuery("<tr>").append(
                        jQuery("<td>", {'css': 'padding: 4px 2px;'}).append(
                            jQuery("<img>", {'src': '/openerp/static/images/warning.png'})
                        ),
                        jQuery("<td>", {'class': 'error_message_content'}).text(msg)
                    ),
                    jQuery("<tr>").append(
                        jQuery("<td>", {'colspan': 2, align: 'right'}).append(
                            jQuery("<a>", {'class': 'button-a', 'href': 'javascript: void(0)'})
                            .click(function(){jQuery.fancybox.close();})
                            .text('OK')
                        )
                ));
    jQuery.fancybox(error, {scrolling: 'no'});
}

function o2m_pager_action(action, src){
    var source = src ? (typeof(src) == "string" ? src : src.name) : null;
    var args = {
        _terp_source: source
    }
    var get_action = validate_action(action, args)
    submit_form(get_action);
}

function submit_form(action, src, target){

    if (openobject.http.AJAX_COUNT > 0) {
        callLater(1, submit_form, action, src, target);
        return;
    }

    if (action == 'delete' && !confirm(_('Do you really want to delete this record?'))) {
        return;
    }


    var source = src ? (typeof(src) == "string" ? src : src.name) : null;

    var args = {
        _terp_source: source
    };

    var $form = jQuery('#view_form');
    if (target == "new" || target == "_blank") {
        $form.attr('target', '_blank');
    }
    else {
        $form.attr('target', '');
    }

    if (action == 'save_and_edit') {
        action = 'save';
        args['_terp_return_edit'] = 1;
    }

    action = get_form_action(action, args);

    if (/\/save(\?|\/)?/.test(action) && !validate_required($form.get(0))) {
        return;
    }

    // Cant use $form.attr due to http://dev.jquery.com/ticket/3113 as there is a form with a field called
    // action when creating an activity
    $form.get(0).setAttribute('action', action);
    $form.submit();
}

function pager_action(action, src){
    var get_action = validate_action(action ? action : 'find', {})
    return src ? new ListView(src).go(action) : submit_form(get_action);
}

function buttonClicked(name, btype, model, id, sure, target, context){
    if (sure && !confirm(sure)) {
        return;
    }

    var params = {
        '_terp_button/name': name,
        '_terp_button/btype': btype,
        '_terp_button/model': model,
        '_terp_button/id': id
    };
    var context = jQuery(document.getElementById(name)).attr('context');

    if (!context || context == "{}") {
        var act = get_form_action(btype == 'cancel' ? 'cancel' : 'save', params);
        submit_form(act, null, target);
        return;
    }

    var req = eval_domain_context_request({
        source: "",
        domain: "[]",
        context: context
    });
    req.addCallback(function(obj){
        params['_terp_button/context'] = obj.context || 0;

        var act = get_form_action(btype == 'cancel' ? 'cancel' : 'save', params);
        submit_form(act, null, target);
    });
}

/**
 * Transpose status of a clicked boolean widget (checkbox) to the associated hidden input
 * @param name the identifier of the hidden input (postfixed by `_checkbox_` on the checkbox)
 */
function onBooleanClicked(name){
    var $source = jQuery(openobject.dom.get(name + '_checkbox_'));
    var $target = jQuery(openobject.dom.get(name));
    $target.val($source.is(':checked') ? 1 : '').change();
}

/**
 * get key-pair object of the form data
 *
 * if extended is
 *    1 then give form data with type info
 *    2 then give form data with type info + required flag
 * else gives simple key-value pairs
 */
function getFormData(extended){

    var parentNode = openobject.dom.get('_terp_list') || document.forms['view_form'];

    var frm = {};

    var is_editable = jQuery('#_terp_editable').val() == 'True';

    var $fields = jQuery(parentNode).find('img[kind=picture]');
    if (is_editable) {
        $fields = $fields.add('input, textarea, select', parentNode);
    }
    else {
        $fields = $fields.add('[kind=value], [name$=/__id]');
    }

    $fields.each(function(){
        var $this = jQuery(this);
        var name = is_editable ? this.name : this.id;

        if (this.tagName.toLowerCase() != 'img' && !name) {
            return;
        }

        name = name.replace('_terp_listfields/', '');

        // don't include _terp_ fields except _terp_id
        if (/_terp_/.test(name) && !/_terp_id$/.test(name)) {
            return;
        }

        // work around to skip o2m values (list mode)
        var value;
        if (name.indexOf('/__id') > 0) {

            name = name.replace('/__id', '');

            if (openobject.dom.get(name + '/_terp_view_type').value == 'form') {
                frm[name + '/__id'] = openobject.dom.get(name + '/__id').value;
                return;
            }
            // skip if editable list's editors are visible
            if (openobject.dom.select("[name^=_terp_listfields/" + name + "]").length) {
                return;
            }

            value = openobject.dom.get(name + '/_terp_ids').value;
            if (extended) {
                value = serializeJSON({
                    'value': value,
                    'type': 'one2many',
                    'relation': openobject.dom.get(name + '/_terp_model').value
                });
            }

            frm[name] = value;
            return;
        }

        if (extended && name.indexOf('/__id') == -1) {
            var attrs = {};

            value = (is_editable ? this.value : $this.attr('value')) || "";
            var kind = $this.attr('kind') || "char";

            //take care of _terp_id
            if (/_terp_id$/.test(name)) {

                //  only the resource id and all O2M
                name = name.replace(/_terp_id$/, '');
                if (name && !openobject.dom.get(name + '__id')) {
                    return;
                }

                name = name + 'id';

                if (!openobject.dom.get(name)) {
                    return;
                }

                kind = 'integer';
                value = value == 'False' ? '' : value;
            }

            attrs['value'] = typeof(value) == "undefined" ? '' : value;

            if (kind) {
                attrs['type'] = kind;
            }

            if (extended && (kind == 'many2one' || kind == 'many2many')) {
                attrs['relation'] = $this.attr('relation');
            }

            if (extended > 1 && $this.hasClass('requiredfield')) {
                attrs['required'] = 1;
            }

            switch (kind) {
                case "picture":
                    name = this.id;
                    break;
                case 'text_html':
                    if (!tinyMCE.get(this.name)) {
                        break;
                    }
                    attrs['value'] = tinyMCE.get(this.name).getContent();
                    break;
                case 'reference':
                    if (!value) {
                        break;
                    }
                    attrs['value'] = "[" + value + ",'" + $this.attr('relation') + "']";
                    break;
            }

            // stringify the attr object
            frm[name] = serializeJSON(attrs);

        }
        else {
            frm[name] = this.value;
        }
    });

    return frm;
}

/*
 * get key-value pair of form params (_terp_)
 * @param name: only return values for given param
 */
function getFormParams(name){

    var parentNode = document.forms['view_form'];

    var frm = {};
    var fields = openobject.dom.select('input', parentNode);

    forEach(fields, function(e){

        if (!e.name || e.name.indexOf('_terp_listfields/') > -1 || e.name.indexOf('_terp_') == -1) {
            return
        }

        if (name && e.name != name) {
            return;
        }

        if (typeof(frm[e.name]) != "undefined") {
            frm[e.name] = MochiKit.Base.flattenArray([frm[e.name], e.value]);
        }
        else {
            frm[e.name] = e.value;
        }
    });

    return frm;
}

function onChange(caller){
    caller = openobject.dom.get(caller);
    var callback = jQuery(caller).attr('callback');
    var change_default = jQuery(caller).attr('change_default');

    if (!(callback || change_default) || caller.__lock_onchange) {
        return;
    }

    var is_list = caller.id.indexOf('_terp_listfields') == 0;
    var prefix = caller.name || caller.id;
    prefix = prefix.slice(0, prefix.lastIndexOf('/') + 1);

    var model = is_list ? openobject.dom.get(prefix.slice(17) + '_terp_model').value : openobject.dom.get(prefix + '_terp_model').value;
    var context = is_list ? openobject.dom.get(prefix.slice(17) + '_terp_context').value : openobject.dom.get(prefix + '_terp_context').value;
    var id = is_list ? openobject.dom.get(prefix.slice(17) + '_terp_id').value : openobject.dom.get(prefix + '_terp_id').value;

    var req = openobject.http.postJSON(callback ? '/openerp/form/on_change' : '/openerp/form/change_default_get', jQuery.extend({}, getFormData(1), {
        _terp_caller: is_list ? caller.id.slice(17) : caller.id,
        _terp_callback: callback,
        _terp_model: model,
        _terp_context: context,
        _terp_value: caller.value,
        id: id
    }));

    req.addCallback(function(obj){

        if (obj.error) {
            return error_popup(obj)
        }

        var values = obj['value'];
        var domains = obj['domain'];

        domains = domains ? domains : {};
        var fld;
        for (var domain in domains) {
            fld = openobject.dom.get(prefix + domain);
            if (fld) {
                jQuery(fld).attr('domain', domains[domain]);
            }
        }

        var flag;
        var value;
        for (var k in values) {
            flag = false;
            fld = openobject.dom.get(prefix + k);

            value = values[k];
            value = value === false || value === null ? '' : value;

            // prevent recursive onchange
            fld.__lock_onchange = true;

            if (openobject.dom.get(prefix + k + '_id')) {
                fld = openobject.dom.get(prefix + k + '_id');
                flag = true;
            }

            if ((fld.value !== value) || flag) {
                fld.value = value;

                var kind = jQuery(fld).attr('kind');

                switch (kind) {
                    case 'picture':
                        fld.src = value;
                        break;
                    case 'many2one':
                        fld.value = value[0] || '';
                        try {
                            openobject.dom.get(prefix + k + '_text').value = value[1] || '';
                        }
                        catch (e) {
                        }
                        break;
                    case 'boolean':
                        openobject.dom.get(prefix + k + '_checkbox_').checked = value || false;
                        break;
                    case 'text_html':
                        if (tinyMCE.get(prefix + k)) {
                            tinyMCE.execInstanceCommand(prefix + k, 'mceSetContent', false, value || '')
                        }
                        break;
                    case 'selection':
                        if (isArrayLike(value)) {
                            var opts = [];
                            opts.push(OPTION({
                                'value': ''
                            }));

                            for (i in value) {
                                var item = value[i];
                                opts.push(OPTION({
                                    'value': item[0]
                                }, item[1]));
                            }
                            MochiKit.DOM.replaceChildNodes(fld, map(function(x){
                                return x;
                            }, opts));
                        }
                        else {
                            fld.value = value;
                        }
                        break;
                    case 'progress':
                        var progress = values['progress'].toString() + '%';
                        jQuery('#progress').text(progress).append(jQuery('<div>', {
                            'width': progress
                        }));
                        break;
                    default:
                    // do nothing on default
                }

                MochiKit.Signal.signal(fld, 'onchange');
                MochiKit.Signal.signal(window.document, 'onfieldchange', fld);
            }

            fld.__lock_onchange = false;
        }

        if (obj.warning && obj.warning.message) {
            error_display(obj.warning.message);
        }
    });
}

/**
 * This function will be used by many2one field to get display name.
 *
 * @param name name/instance of the widget
 * @param relation the OpenERP model
 */
function getName(name, relation){
    var value_field = openobject.dom.get(name);
    var text_field = openobject.dom.get(value_field.name + '_text');

    relation = relation ? relation : jQuery(value_field).attr('relation');

    if (value_field.value == '') {
        text_field.value = ''
    }

    if (value_field.value) {
        var req = openobject.http.getJSON('/openerp/search/get_name', {
            model: relation,
            id: value_field.value
        });
        req.addCallback(function(obj){
            text_field.value = obj.name;
        });
    }
}

function eval_domain_context_request(options){

    if ((!options.domain || options.domain == '[]') && (!options.context || options.context == '{}')) {
        return new MochiKit.Async.succeed(-1);
    }

    var prefix = options.source.split("/");
    prefix.pop();

    // editable listview fields
    if (prefix[0] == '_terp_listfields') {
        prefix.shift();
    }
    var params = jQuery.extend(getFormData(1), {
        '_terp_domain': options.domain,
        '_terp_context': options.context,
        '_terp_prefix': prefix.join('/'),
        '_terp_active_id': openobject.dom.get(prefix.concat('_terp_id').join('/')).value,
        '_terp_active_ids': openobject.dom.get(prefix.concat('_terp_ids').join('/')).value
    });

    if (options.group_by_ctx && options.group_by_ctx.length > 0)
        params['_terp_group_by'] = options.group_by_ctx;
    else
        params['_terp_group_by'] = '[]';

    if (options.active_id) {
        params['_terp_active_id'] = options.active_id;
        params['_terp_active_ids'] = options.active_ids;
    }

    var parent_context = openobject.dom.get(prefix.concat('_terp_context').join('/'));

    if (parent_context) {
        params['_terp_parent_context'] = parent_context.value;
    }

    var req = openobject.http.postJSON('/openerp/search/eval_domain_and_context', params);
    return req.addCallback(function(obj){

        if (obj.error_field) {

            var fld = openobject.dom.get(obj.error_field) || openobject.dom.get('_terp_listfields/' + obj.error_field);

            if (fld && jQuery(fld).attr('kind') == 'many2one') {
                fld = openobject.dom.get(fld.id + '_text');
            }

            if (fld) {
                fld.focus();
                fld.select();
            }
        }

        if (obj.error) {
            return error_popup(obj.error)
        }

        return obj;
    });
}

function open_search_window(relation, domain, context, source, kind, text){

    var req = eval_domain_context_request({
        'source': source,
        'domain': domain,
        'context': context
    });

    if (kind == 2 && source.indexOf('_terp_listfields/') == 0) {
        text = "";
    }

    req.addCallback(function(obj){
        openobject.tools.openWindow(openobject.http.getURL('/openerp/search/new', {
            'model': relation,
            'domain': obj.domain,
            'context': obj.context,
            'source': source,
            'kind': kind,
            'text': text
        }));
    });
}

function makeContextMenu(id, kind, relation, val){
    var act = get_form_action('get_context_menu');

    var prefix = id.indexOf('/') > -1 ? id.slice(0, id.lastIndexOf('/')) + '/' : '';

    var model = prefix ? openobject.dom.get(prefix + '_terp_model').value : openobject.dom.get('_terp_model').value;

    var params = {
        'model': model,
        'field': id,
        'kind': kind,
        'relation': relation,
        'value': val
    };

    var req = openobject.http.postJSON(act, params);

    req.addCallback(function(obj){
        var r, o, a;
        var rows = [];

        for (r in obj.defaults) {
            o = obj.defaults[r];
            a = SPAN({
                onclick: 'hideElement("contextmenu"); return ' + o.action
            }, o.text);
            rows = rows.concat(a);
        }
        if (obj.actions.length > 0) {
            rows = rows.concat(HR());

            for (r in obj.actions) {
                o = obj.actions[r];

                a = SPAN({
                    'class': o.action ? '' : 'disabled',
                    'onclick': o.action ? 'hideElement("contextmenu"); return ' + o.action : ''
                }, o.text);

                rows = rows.concat(a);
            }
        }

        if (obj.relates.length > 0) {
            rows = rows.concat(HR());

            for (r in obj.relates) {
                o = obj.relates[r];

                a = SPAN({
                    'class': o.action ? '' : 'disabled',
                    'onclick': o.action ? 'hideElement(\'contextmenu\'); return ' + o.action : '',
                    'domain': o.domain,
                    'context': o.context
                }, o.text);

                rows = rows.concat(a);
            }
        }

        openobject.dom.get('contextmenu').innerHTML = '';

        var tbl = TABLE({
            'cellpadding': 0,
            'cellspacing': 0
        }, TBODY(null, map(function(r){
            return TR(null, TD(null, r));
        }, rows)));

        appendChildNodes('contextmenu', tbl);

        var ctx_menu = openobject.dom.get('contextmenu');
        ctx_menu.style.left = ctx_menu.pageX + 'px';
        ctx_menu.style.top = ctx_menu.pageY + 'px';

        showContextMenu();
    });
}

function showContextMenu(){

    var menu = openobject.dom.get('contextmenu');
    var ifrm = openobject.dom.get('contextmenu_frm');

    showElement(menu);

    if (ifrm) {

        ifrm.style.left = menu.offsetLeft + "px";
        ifrm.style.top = menu.offsetTop + "px";
        ifrm.style.width = menu.offsetWidth + "px";
        ifrm.style.height = menu.offsetHeight + "px";
        ifrm.style.zIndex = 6;

        showElement(ifrm);
    }
}

function hideContextMenu(){
    var menu = openobject.dom.get('contextmenu');
    var ifrm = openobject.dom.get('contextmenu_frm');

    if (ifrm) {
        hideElement(ifrm);
    }

    hideElement(menu);
}

function set_to_default(field, model){

    var kind = getNodeAttribute(openobject.dom.get(field), 'kind');

    var act = get_form_action('get_default_value');
    var params = {
        'model': model,
        'field': field
    };

    var req = openobject.http.postJSON(act, params);
    req.addCallback(function(obj){

        openobject.dom.get(field).value = obj.value;
        signal(field, "onchange");
    });
}

function set_as_default(field, model){

    var kind = getNodeAttribute(openobject.dom.get(field), 'kind');

    var args = getFormData(1);

    args['_terp_model'] = model;
    args['_terp_field'] = field;

    var req = openobject.http.postJSON('/openerp/fieldpref/get', args);

    req.addCallback(function(obj){
        var text = obj.text;
        var params = {
            '_terp_model': model,
            '_terp_field/name': field,
            '_terp_field/string': text,
            '_terp_field/value': openobject.dom.get(field).value,
            '_terp_deps': obj.deps
        };

        openobject.tools.openWindow(openobject.http.getURL('/openerp/fieldpref', params), {
            width: 500,
            height: 350
        });
    });
}

function do_report(id, relation){

    id = openobject.dom.get(id).value;

    var act = get_form_action('report');
    var params = {
        '_terp_model': relation,
        '_terp_id': id
    };

    window.open(openobject.http.getURL(act, params));
}

function do_action(action_id, field, relation, src, data, context_menu){

    var params = {};

    if (openobject.dom.get('_terp_list')) {
        var list = new ListView('_terp_list');
        var ids = list.getSelectedRecords();

        if (ids.length == 0) {
            return error_display(_('You must select at least one record.'));
        }

        params['_terp_selection'] = '[' + ids.join(',') + ']';
    }

    var id = openobject.dom.get(field).value;
    var domain = getNodeAttribute(src, 'domain');
    var context = getNodeAttribute(src, 'context');
    var context_menu = context_menu ? true: null;

    var req = eval_domain_context_request({
        'source': openobject.dom.get(field).id,
        'active_id': id,
        'active_ids': params['_terp_selection'],
        'domain': domain,
        'context': context
    });

    req.addCallback(function(obj){

        var act = get_form_action('action');
        MochiKit.Base.update(params, {
            '_terp_action': action_id,
            '_terp_domain': obj.domain,
            '_terp_context': obj.context,
            '_terp_id': id,
            '_terp_model': relation,
            'datas': data,
            'context_menu': context_menu
        });

        window.open(openobject.http.getURL(act, params));

    });
}

function translate_fields(src){
	var $src = jQuery(src);
	var relation = $src.attr('relation');
	var id = $src.attr('id');
	var ctx = $src.attr('data');

	openobject.tools.openWindow(openobject.http.getURL('/openerp/translator',{
        _terp_model: relation,
        _terp_id: id,
        _terp_context: ctx
    }));
}

function on_context_menu(evt){

    if (!evt.modifier()) {
        return;
    }

    var target = evt.target();
    var kind = getNodeAttribute(target, 'kind');

    if (!kind || target.disabled) {
        return;
    }

    var menu = openobject.dom.get('contextmenu');

    if (!menu) {

        menu = DIV({
            'id': 'contextmenu',
            'class': 'contextmenu',
            'onmouseout': 'hideContextMenu()',
            'onmouseover': 'showContextMenu()',
            'style': 'position: absolute; display: none;'
        });

        appendChildNodes(document.body, menu);

        if (/msie/.test(navigator.userAgent.toLowerCase())) {
            var ifrm = createDOM('IFRAME', {
                'id': 'contextmenu_frm',
                'src': '#',
                'frameborder': '0',
                'scrolling': 'no',
                'style': 'position: absolute; display: none;'
            });

            appendChildNodes(document.body, ifrm);
        }
    }

    var src = target.id;

    if (kind == 'many2one') {
        src = src.slice(0, -5);
    }

    var val = openobject.dom.get(src).value;
    var relation = getNodeAttribute(src, 'relation');

    hideElement(menu);

    var p = evt.mouse().page;

    setElementPosition(menu, p);

    makeContextMenu(src, kind, relation, val);

    evt.stop();
}

function open_url(site){
    var web_site;

    isIE = /msie/.test(navigator.userAgent.toLowerCase());

    if (isIE && site.indexOf('@') > -1) {
        site = site.split('@');
        site = site[1]
    }

    if (site.indexOf("://") == -1) {
        web_site = 'http://' + site;
    }
    else {
        web_site = site;
    }

    if (site.length > 0) {
        window.open(web_site);
    }
}

function submenu_action(action_id, model){
    openLink(openobject.http.getURL("/openerp/form/action_submenu", {
        _terp_action_id: action_id,
        _terp_model: model,
        _terp_id: $('_terp_id').value
    }));
}

function show_wkf(){
    var id;

    if (jQuery('#_terp_list').length) {
        var lst = new ListView('_terp_list');
        var ids = lst.getSelectedRecords();

        if (ids.length < 1) {
            error_display(_('You must select at least one record.'));
            return;
        }
        id = ids[0];
    }
    else {
        var element = jQuery('#_terp_id');
        id = element && element.val() != 'False' ? element.val() : null;
    }

    openobject.tools.openWindow(openobject.http.getURL('/view_diagram/workflow', {
        model: jQuery('#_terp_model').val(),
        rec_id: id
    }));
}

/**
 * @event click
 *
 * Requests the deletion of an attachment based on data provided by the trigger's parent's @data-id
 */
function removeAttachment(){
    var attachment_line = jQuery(this).parent();
    var id = attachment_line.attr('data-id');
    if (confirm('Do you really want to delete the attachment {' +
    jQuery.trim(attachment_line.find('> a.attachment-file').text()) +
    '} ?')) {
        jQuery.ajax({
            url: '/openerp/attachment/remove/',
            type: 'POST',
            data: {
                'id': id
            },
            dataType: 'json',
            success: function(obj){
                if (obj.error) {
                    error_popup(obj.error);
                }

                jQuery(attachment_line).remove();
            }
        });
    }

    return false;
}

/**
 * @event form submission
 *
 * Used by the sidebar to create a new attachment.
 *
 * Creates a new line in #attachments if the creation succeeds.
 */
function createAttachment(){
    if (!jQuery('#sidebar_attachments_datas').val()) {
        return false;
    }
    var form = jQuery(this);
    form.ajaxSubmit({
        dataType: 'json',
        success: function(data){
            var attachment_line = jQuery('<li>', {
                'id': 'attachment_item_' + data['id'],
                'data-id': data['id']
            });

            jQuery([jQuery('<a>', {
                'rel': 'external',
                'href': openobject.http.getURL('/openerp/attachment/get', {
                    'record': data['id']
                }),
                'class': 'attachment-file'
            }).text(data['name']), jQuery('<span>|</span>'), jQuery("<a href='#' class='close'>Close</a>")]).appendTo(attachment_line);

            jQuery('#attachments').append(attachment_line);
            form.resetForm();
            form.hide();
        }
    });
    return false;
}

function setupAttachments(){
    jQuery('#attachments').delegate('li a.close', 'click', removeAttachment);

    var attachmentsForm = jQuery('#attachment-box').hide();
    jQuery('#add-attachment').click(function(e){
        attachmentsForm.show();
        e.preventDefault();
    });
    attachmentsForm.bind({
        change: createAttachment,
        // leave that one just in case, but should generally not activate
        submit: createAttachment
    });
}

function error_popup(obj){
    try {
        var error_window = window.open("", "error", "status=1, scrollbars=yes, width=550, height=400");
        error_window.document.write(obj.error);
        error_window.document.title += "OpenERP - Error"
        error_window.document.close();
    }
    catch (e) {
        error_display(e)
    }
}

// Setup by the view, the id of the current object
var RESOURCE_ID;
/**
 * Create a shortcut bar item for the provided menu ID
 */
function add_shortcut_to_bar(id){
    jQuery.getJSON('/openerp/shortcuts/by_resource', function(data){
        var $shortcuts = jQuery('#shortcuts');
        var $shortcuts_list = $shortcuts.children('ul');
        $shortcuts_list.append(jQuery('<li>', {
            'class': $shortcuts_list.children().length ? '' : 'first'
        }).append(jQuery('<a>', {
            'id': 'shortcut_' + id,
            'href': openobject.http.getURL('/openerp/tree/open', {
                'id': id,
                'model': 'ir.ui.menu'
            })
        }).append(jQuery('<span>').text(data[id]['name']))));
        $shortcuts.trigger('altered');
    });
}

/**
 * Toggle the shortcut for the current resource (create or delete it depending on current status)
 */
function toggle_shortcut(){
    var adding = jQuery(this).hasClass('shortcut-add');
    jQuery.ajax({
        url: adding ? '/openerp/shortcuts/add' : '/openerp/shortcuts/delete',
        context: this,
        type: 'POST',
        data: {
            'id': RESOURCE_ID
        },
        success: function(){
            jQuery(this).toggleClass('shortcut-add shortcut-remove');
            if (adding) {
                add_shortcut_to_bar(RESOURCE_ID);
            } else {
                jQuery('#shortcut_' + RESOURCE_ID).parent().remove();
                jQuery('#shortcuts').trigger('altered');
            }
        }
    });
}


var is_form_changed = false;
function validateForm(){
    is_form_changed = false;
    jQuery('#view_form table tr td:first').find('input:not([type=hidden]), select').change(function(){
        is_form_changed = true;
    });
}

function validate_action(action, args){
    var args = args;

    if (is_form_changed) {
        if (confirm('The record has been modified \n Do you want to save it ?')) {
            args['_terp_save_current_id'] = 1;
        }
    }
    return get_form_action(action, args)
}
