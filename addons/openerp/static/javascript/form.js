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

function get_form_action(action, params) {

    var act = typeof(form_controller) == 'undefined' ? '/form' : form_controller;
    act = action && action.indexOf('/') == 0 ? action : act + '/' + action;
    return openobject.http.getURL(act, params);
}

function openRecord(id, src, target, readonly) {

    var kind = getNodeAttribute(src + '_set', 'kind');

    if (!kind && openobject.dom.get('_o2m_' + src)) {
        kind = "one2many";
    }

    if (kind == "one2many") {
        return new One2Many(src).edit(id, readonly);
    }

    var prefix = src && src != '_terp_list' ? src + '/' : '';

    var model = openobject.dom.get(prefix + '_terp_model').value;
    var view_ids = openobject.dom.get(prefix + '_terp_view_ids').value;
    var view_mode = openobject.dom.get(prefix + '_terp_view_mode').value;

    var ids = openobject.dom.get(prefix + '_terp_ids').value;

    var offset = openobject.dom.get(prefix + '_terp_offset').value;
    var limit = openobject.dom.get(prefix + '_terp_limit').value;
    var count = openobject.dom.get(prefix + '_terp_count').value;

    var domain = openobject.dom.get(prefix + '_terp_domain').value;
    var context = openobject.dom.get(prefix + '_terp_context').value;

    var search_domain = openobject.dom.get('_terp_search_domain');
    search_domain = search_domain ? search_domain.value : null;

    var search_data = openobject.dom.get('_terp_search_data');
    search_data = search_data ? search_data.value : null;

    var search_filter_domain = openobject.dom.get('_terp_filter_domain');
    search_filter_domain = search_filter_domain ? search_filter_domain.value : [];

    var args = {
        'model': model,
        'id': id ? id : 'False',
        'ids': ids,
        'view_ids': view_ids,
        'view_mode': view_mode,
        'domain': domain,
        'context': context,
        'offset': offset,
        'limit': limit,
        'count': count,
        'search_domain': search_domain,
        'search_data': search_data,
        'filter_domain' : search_filter_domain
    };

    var action = readonly ? 'view' : 'edit';

    if (target == '_blank') {
        return window.open(get_form_action(action, args));
    }

    if (kind == 'many2many') {
        args['source'] = src;
        return openobject.tools.openWindow(get_form_action('/openerp/openm2m/edit', args));
    }

    window.location.href = get_form_action(action, args);
}

function editRecord(id, src, target) {
    return openRecord(id, src, target, false);
}

function viewRecord(id, src) {
    return openRecord(id, src, null, true);
}

function editSelectedRecord() {

    var lst = new ListView('_terp_list');
    var ids = lst.getSelectedRecords();

    if (ids && ids.length > 5) {
        var msg = _('You selected to open %(tabs)s tabs - do you want to continue?');
        msg = msg.replace('%(tabs)s', ids.length);
        if (!confirm(msg)) {
            return;
        }
    }

    forEach(ids, function(id) {
        editRecord(id, '_terp_list', '_blank');
    });
}

function switchView(view_type, src) {

    var prefix = src ? src + '/' : '';
    var form = document.forms['view_form'];

    var params = {
        '_terp_source': src,
        '_terp_source_view_type': view_type
    };

    if (openobject.dom.get('_terp_list')) {
        var ids = new ListView('_terp_list').getSelectedRecords();
        if (ids.length > 0) {
            openobject.dom.get('_terp_id').value = ids[0];
        }
    }

    submit_form(get_form_action('switch', params));
}

function switch_O2M(view_type, src) {

    if (openobject.http.AJAX_COUNT > 0) {
        return;
    }

    var prefix = src ? src + '/' : '';
    var form = document.forms['view_form'];

    var params = getFormParams();

    params['_terp_source'] = src;
    params['_terp_source_view_type'] = view_type;
    params['_terp_editable'] = $(prefix + '_terp_editable').value

    if (openobject.dom.get('_terp_list')) {
        var ids = new ListView('_terp_list').getSelectedRecords();
        if (ids.length > 0) {
            openobject.dom.get('_terp_id').value = ids[0];
        }
    }

    req = openobject.http.post('/openerp/form/switch_o2m', params);
    req.addCallback(function(xmlHttp) {

        var text = xmlHttp.responseText;
        if (text.indexOf('ERROR: ') == 0) {
            text = text.replace('ERROR: ', '');
            return alert(text);
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
            forEach(scripts, function(s) {
                eval(s.innerHTML);
            });
        }
    });
}

function show_process_view() {
	var model = openobject.dom.get('_terp_model').value;
	var id = openobject.dom.get('_terp_id').value;
	
	if (openobject.dom.get('_terp_list')) {
		 var list = new ListView('_terp_list');
		 var ids = list.getSelectedRecords();
		 if (ids.length) {
			id = ids[0];
		 }
	}
	id = parseInt(id) || null;
	window.location.href = openobject.http.getURL('/view_diagram/process', {res_model: model, res_id: id})
}

function validate_required(form) {

    if (typeof form == 'string') {
        form = document.forms[form];
    }

    if (!form) {
        return true;
    }

    var elements = MochiKit.Base.filter(function(el) {
        return !el.disabled && el.id && el.name && el.id.indexOf('_terp_listfields/') == -1 && hasElementClass(el, 'requiredfield');
    }, form.elements);

    var result = true;

    for (var i = 0; i < elements.length; i++) {

        var elem = elem2 = elements[i];
        var value = elem.value;
        var kind = MochiKit.DOM.getNodeAttribute(elem, 'kind');

        if (kind == 'many2many') {
            elem2 = openobject.dom.get(elem.name + '_set') || elem;
            value = value == '[]' ? '' : value;
        }

        if (kind == 'many2one' || kind == 'reference') {
            elem2 = openobject.dom.get(elem.id + '_text') || elem;
        }

        if (!value) {
            addElementClass(elem2, 'errorfield');
            result = false;
        } else if (hasElementClass(elem2, 'errorfield')) {
            removeElementClass(elem2, 'errorfield');
        }
    }

    if (!result) {
        alert(_("Invalid form, correct red fields !"));
    }

    return result;
}

function submit_form(action, src, target) {

    if (openobject.http.AJAX_COUNT > 0) {
        return callLater(1, submit_form, action, src, target);
    }

    if (action == 'delete' && !confirm(_('Do you really want to delete this record?'))) {
        return false;
    }

    var form = document.forms['view_form'];
    setNodeAttribute(form, 'target', '');

    var source = src ? (typeof(src) == "string" ? src : src.name) : null;

    var args = {
        _terp_source: source
    };

    if (target == "new" || target == "_blank") {
        setNodeAttribute(form, 'target', '_blank');
    }

    if (action == 'save_and_edit') {
        action = 'save';
        args['_terp_return_edit'] = 1;
    }

    action = get_form_action(action, args);

    if (/\/save(\?|\/)?/.test(action) && !validate_required(form)) {
        return false;
    }

    form.attributes['action'].value = action;
    form.submit();
}

function pager_action(action, src) {
    return src ? new ListView(src).go(action) : submit_form(action ? action : 'find');
}

function buttonClicked(name, btype, model, id, sure, target) {

    if (sure && !confirm(sure)) {
        return;
    }

    var params = {
        '_terp_button/name': name,
        '_terp_button/btype': btype,
        '_terp_button/model': model,
        '_terp_button/id': id
    };
    
    if (!context || context == "{}") {
        var act = get_form_action(btype == 'cancel' ? 'cancel' : 'save', params);
        return submit_form(act, null, target);
    }
    
    var req = eval_domain_context_request({source: "", domain: "[]", context: context});
    req.addCallback(function(obj) {
        params['_terp_button/context'] = obj.context || 0;

        var act = get_form_action(btype == 'cancel' ? 'cancel' : 'save', params);
        submit_form(act, null, target);
     });
}

function onBooleanClicked(name) {

    var source = openobject.dom.get(name + '_checkbox_');
    var target = openobject.dom.get(name);

    target.value = source.checked ? 1 : '';
    MochiKit.Signal.signal(target, 'onchange');
}

/**
 * get key-pair object of the form data
 *
 * if extended is
 *    1 then give form data with type info
 *    2 then give form data with type info + required flag
 * else gives simple key-value pairs
 */
function getFormData(extended) {

    var parentNode = openobject.dom.get('_terp_list') || document.forms['view_form'];

    var frm = {};
    var fields = [];

    var is_editable = openobject.dom.get('_terp_editable').value == 'True';

    if (is_editable) {
        fields = openobject.dom.select("input, textarea, select", parentNode);
    } else {
        fields = fields.concat(openobject.dom.select('kind=value'));
        fields = fields.concat(openobject.dom.select('[name$=/__id]'));
    }

    fields = fields.concat(filter(function(e) {
        return getNodeAttribute(e, 'kind') == 'picture';
    }, openobject.dom.select('img', parentNode)));

    for (var i = 0; i < fields.length; i++) {

        var e = fields[i];
        var n = is_editable ? e.name : e.id;

        if (e.tagName.toLowerCase() != 'img' && !n) {
            continue;
        }

        n = n.replace('_terp_listfields/', '');

        // don't include _terp_ fields except _terp_id
        if (/_terp_/.test(n) && ! /_terp_id$/.test(n)) {
            continue;
        }

        // work around to skip o2m values (list mode)
        var value;
        if (n.indexOf('/__id') > 0) {

            n = n.replace('/__id', '');

            if (openobject.dom.get(n + '/_terp_view_type').value == 'form') {
                frm[n + '/__id'] = openobject.dom.get(n + '/__id').value;
                continue;
            }
            // skip if editable list's editors are visible
            if (openobject.dom.select("[name^=_terp_listfields/" + n + "]").length) {
                continue;
            }

            value = openobject.dom.get(n + '/_terp_ids').value;
            if (extended) {
                value = {'value': value,
                    'type': 'one2many',
                    'relation': openobject.dom.get(n + '/_terp_model').value};
                value = serializeJSON(value);
            }

            frm[n] = value;
            continue;
        }

        if (extended && n.indexOf('/__id') == -1) {

            var attrs = {};

            value = (is_editable ? e.value : getNodeAttribute(e, 'value')) || "";
            var kind = getNodeAttribute(e, 'kind') || "char";

            //take care of _terp_id
            if (/_terp_id$/.test(n)) {

                //  only the resource id and all O2M
                n = n.replace(/_terp_id$/, '');
                if (n && !openobject.dom.get(n + '__id')) {
                    continue;
                }

                n = n + 'id';

                if (!openobject.dom.get(n)) {
                    continue;
                }

                kind = 'integer';
                value = value == 'False' ? '' : value;
            }

            attrs['value'] = typeof(value) == "undefined" ? '' : value;

            if (kind) {
                attrs['type'] = kind;
            }

            if (extended && (kind == 'many2one' || kind == 'many2many')) {
                attrs['relation'] = getNodeAttribute(e, 'relation');
            }

            if (extended > 1 && hasElementClass(e, 'requiredfield')) {
                attrs['required'] = 1;
            }

            if (kind == "picture") {
                n = e.id;
            }

            if (kind == 'text_html') {
                if(tinyMCE.get(e.name)){
                    attrs['value'] =  tinyMCE.get(e.name).getContent();
                }
            }
            
            if (kind == 'reference' && value) { 
                attrs['value'] = "[" + value + ",'" + getNodeAttribute(e, 'relation') + "']";
            }

            // stringify the attr object
            frm[n] = serializeJSON(attrs);

        } else {
            frm[n] = e.value;
        }
    }

    return frm;
}

/*
 * get key-value pair of form params (_terp_)
 * @param name: only return values for given param
 */
function getFormParams(name) {

    var parentNode = document.forms['view_form'];

    var frm = {};
    var fields = openobject.dom.select('input', parentNode);

    forEach(fields, function(e) {

        if (!e.name || e.name.indexOf('_terp_listfields/') > -1 || e.name.indexOf('_terp_') == -1) {
            return
        }

        if (name && e.name != name) {
            return;
        }

        if (typeof(frm[e.name]) != "undefined") {
            frm[e.name] = MochiKit.Base.flattenArray([frm[e.name], e.value]);
        } else {
            frm[e.name] = e.value;
        }
    });

    return frm;
}

function onChange(name) {

    var caller = openobject.dom.get(name);
    var callback = getNodeAttribute(caller, 'callback');
    var change_default = getNodeAttribute(caller, 'change_default');

    if (!(callback || change_default) || caller.__lock_onchange) {
        return;
    }

    var is_list = caller.id.indexOf('_terp_listfields') == 0;
    var prefix = caller.name || caller.id;
    prefix = prefix.slice(0, prefix.lastIndexOf('/') + 1);

    var params = getFormData(1);
    var model = is_list ? openobject.dom.get(prefix.slice(17) + '_terp_model').value : openobject.dom.get(prefix + '_terp_model').value;
    var context = is_list ? openobject.dom.get(prefix.slice(17) + '_terp_context').value : openobject.dom.get(prefix + '_terp_context').value;
    var id = is_list ? openobject.dom.get(prefix.slice(17) + '_terp_id').value : openobject.dom.get(prefix + '_terp_id').value;

    params['_terp_caller'] = is_list ? caller.id.slice(17) : caller.id;
    params['_terp_callback'] = callback;
    params['_terp_model'] = model;
    params['_terp_context'] = context;
    params['_terp_value'] = caller.value;
    params['id'] = id;

    var req = openobject.http.postJSON(callback ? '/openerp/form/on_change' : '/openerp/form/change_default_get', params);

    req.addCallback(function(obj) {

        if (obj.error) {
            return alert(obj.error);
        }

        values = obj['value'];
        domains = obj['domain'];

        domains = domains ? domains : {};

        for (var domain in domains) {
            fld = openobject.dom.get(prefix + domain);
            if (fld) {
                setNodeAttribute(fld, 'domain', domains[domain]);
            }
        }

        for (var k in values) {

            flag = false;
            fld = openobject.dom.get(prefix + k);

            if (!fld) {
                continue;
            }

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

                var kind = getNodeAttribute(fld, 'kind');

                switch (kind) {
                    case 'picture':
                        fld.src = value;
                        break;
                    case 'many2one':
                        fld.value = value[0] || '';
                        try {
                            openobject.dom.get(prefix + k + '_text').value = value[1] || '';
                        } catch(e) {
                        }
                        break;
                    case 'boolean':
                        openobject.dom.get(prefix + k + '_checkbox_').checked = value || false;
                        break;
                    case 'text_html':
                        if(tinyMCE.get(prefix + k)){
                            tinyMCE.execInstanceCommand(prefix + k, 'mceSetContent', false, value || '')
                        }
                        break;
                    case 'selection':
                        var opts = [];
                        opts.push(OPTION({'value': ''}));

                        for (i in value) {
                            var item = value[i];
                            opts.push(OPTION({'value': item[0]}, item[1]));
                        }
                        MochiKit.DOM.replaceChildNodes(fld, map(function(x) {
                            return x;
                        }, opts));
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
            alert(obj.warning.message);
        }
    });
}

/**
 * This function will be used by many2one field to get display name.
 *
 * @param name: name/instance of the widget
 * @param relation: the OpenERP model
 *
 * @return string
 */
function getName(name, relation) {

    var value_field = openobject.dom.get(name);
    var text_field = openobject.dom.get(value_field.name + '_text');

    relation = relation ? relation : getNodeAttribute(value_field, 'relation');

    if (value_field.value == '') {
        text_field.value = ''
    }

    if (value_field.value) {
        var req = openobject.http.getJSON('/openerp/search/get_name', {model: relation, id : value_field.value});
        req.addCallback(function(obj) {
            text_field.value = obj.name;
        });
    }
}

function eval_domain_context_request(options) {

    if ((!options.domain || options.domain == '[]') && (!options.context || options.context == '{}')) {
        return new MochiKit.Async.succeed(-1);
    }

    var prefix = options.source.split("/");
    prefix.pop();

    // editable listview fields
    if (prefix[0] == '_terp_listfields') {
        prefix.shift();
    }
    prefix = prefix.join('/');

    var params = getFormData(1);

    params['_terp_domain'] = options.domain;
    params['_terp_context'] = options.context;
    params['_terp_prefix'] = prefix;
    params['_terp_active_id'] = prefix ? openobject.dom.get(prefix + '/_terp_id').value : openobject.dom.get('_terp_id').value;
    params['_terp_active_ids'] = prefix ? openobject.dom.get(prefix + '/_terp_ids').value : openobject.dom.get('_terp_ids').value;
    
    if(options.group_by_ctx.length > 0)
        params['_terp_group_by'] = options.group_by_ctx;
    else
        params['_terp_group_by'] = '[]';
    
    if (options.active_id) {
        params['_terp_active_id'] = options.active_id;
        params['_terp_active_ids'] = options.active_ids;
    }

    var parent_context = prefix ? openobject.dom.get(prefix + '/_terp_context') : openobject.dom.get('_terp_context');

    if (parent_context) {
        params['_terp_parent_context'] = parent_context.value;
    }

    var req = openobject.http.postJSON('/openerp/search/eval_domain_and_context', params);
    return req.addCallback(function(obj) {

        if (obj.error_field) {

            var fld = openobject.dom.get(obj.error_field) || openobject.dom.get('_terp_listfields/' + obj.error_field);

            if (fld && getNodeAttribute(fld, 'kind') == 'many2one') {
                fld = openobject.dom.get(fld.id + '_text');
            }

            if (fld) {
                fld.focus();
                fld.select();
            }
        }

        if (obj.error) {
            return alert(obj.error);
        }

        return obj;
    });
}

function open_search_window(relation, domain, context, source, kind, text) {

    var req = eval_domain_context_request({
        'source': source,
        'domain': domain,
        'context': context
    });

    if (kind == 2 && source.indexOf('_terp_listfields/') == 0) {
        text = "";
    }

    req.addCallback(function(obj) {
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

function showCustomizeMenu(src, elem) {
    var elem = openobject.dom.get(elem);

    var frame = window.frameElement ? window.frameElement : null;
    if (frame) {
        frame.style.height = elementDimensions(openobject.dom.get('main_form_body')).h + 70 + 'px';
    }

    MochiKit.Visual.appear(elem, {from: 0, duration: 0.4});
}

function makeContextMenu(id, kind, relation, val) {

    var form = document.forms['view_form'];
    var act = get_form_action('get_context_menu');

    var prefix = id.indexOf('/') > -1 ? id.slice(0, id.lastIndexOf('/')) + '/' : '';

    var model = prefix ? openobject.dom.get(prefix + '_terp_model').value : openobject.dom.get('_terp_model').value;

    var params = {'model': model, 'field': id, 'kind': kind, 'relation': relation, 'value': val};

    var req = openobject.http.postJSON(act, params);

    req.addCallback(function(obj) {

        var rows = [];

        for (var r in obj.defaults) {
            var o = obj.defaults[r];
            var a = SPAN({onclick: 'hideElement("contextmenu"); return ' + o.action}, o.text);
            rows = rows.concat(a);
        }

        if (obj.actions.length > 0) {
            rows = rows.concat(HR());

            for (var r in obj.actions) {
                var o = obj.actions[r];

                var a = SPAN({
                    'class': o.action ? '' : 'disabled',
                    'onclick': o.action ? 'hideElement("contextmenu"); return ' + o.action : ''
                }, o.text);

                rows = rows.concat(a);
            }
        }

        if (obj.relates.length > 0) {
            rows = rows.concat(HR());

            for (var r in obj.relates) {
                var o = obj.relates[r];

                var a = SPAN({
                    'class': o.action ? '' : 'disabled',
                    'onclick': o.action ? 'hideElement(\'contextmenu\'); return ' + o.action : '',
                    'domain': o.domain,
                    'context': o.context
                }, o.text);

                rows = rows.concat(a);
            }
        }

        openobject.dom.get('contextmenu').innerHTML = '';

        var tbl = TABLE({'cellpadding': 0, 'cellspacing' : 0},
                TBODY(null, map(function(r) {
                    return TR(null, TD(null, r));
                }, rows)));

        appendChildNodes('contextmenu', tbl);

        var vd = getViewportDimensions();
        var md = elementDimensions('contextmenu');

        var x = openobject.dom.get('contextmenu').style.left.slice(0, -2);
        var y = openobject.dom.get('contextmenu').style.top.slice(0, -2);
        x = parseInt(x);
        y = parseInt(y);

        if ((x + md.w) > vd.w) {
            x -= x + md.w - vd.w;
            openobject.dom.get('contextmenu').style.left = x + 'px';
        }

        if ((y + md.h) > vd.h) {
            y -= y + md.h - vd.h;
            openobject.dom.get('contextmenu').style.top = y + 'px';
        }

        showContextMenu();
    });
}

function showContextMenu() {

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

function hideContextMenu() {
    var menu = openobject.dom.get('contextmenu');
    var ifrm = openobject.dom.get('contextmenu_frm');

    if (ifrm) {
        hideElement(ifrm);
    }

    hideElement(menu);
}

function set_to_default(field, model) {

    var kind = getNodeAttribute(openobject.dom.get(field), 'kind');

    var act = get_form_action('get_default_value');
    var params = {'model': model, 'field': field};

    var req = openobject.http.postJSON(act, params);
    req.addCallback(function(obj) {

        openobject.dom.get(field).value = obj.value;
        signal(field, "onchange");
    });
}

function set_as_default(field, model) {

    var kind = getNodeAttribute(openobject.dom.get(field), 'kind');

    var args = getFormData(1);

    args['_terp_model'] = model;
    args['_terp_field'] = field;

    var req = openobject.http.postJSON('/openerp/fieldpref/get', args);

    req.addCallback(function(obj) {
        var text = obj.text;
        var params = {
            '_terp_model': model,
            '_terp_field/name': field,
            '_terp_field/string': text,
            '_terp_field/value': openobject.dom.get(field).value,
            '_terp_deps': obj.deps
        };

        openobject.tools.openWindow(openobject.http.getURL('/openerp/fieldpref', params), {width: 500, height: 350});
    });
}

function do_report(id, relation) {

    id = openobject.dom.get(id).value;

    var act = get_form_action('report');
    var params = {'_terp_model': relation, '_terp_id': id};

    window.open(openobject.http.getURL(act, params));
}

function do_action(action_id, field, relation, src) {

    var params = {};

    if (openobject.dom.get('_terp_list')) {
        var list = new ListView('_terp_list');
        var ids = list.getSelectedRecords();

        if (ids.length == 0) {
            return alert(_('You must select at least one record.'));
        }

        params['_terp_selection'] = '[' + ids.join(',') + ']';
    }

    var id = openobject.dom.get(field).value;
    var domain = getNodeAttribute(src, 'domain');
    var context = getNodeAttribute(src, 'context');

    var req = eval_domain_context_request({
        'source': openobject.dom.get(field).id,
        'active_id': id,
        'active_ids': params['_terp_selection'],
        'domain': domain,
        'context': context
    });

    req.addCallback(function(obj) {

        var act = get_form_action('action');
        MochiKit.Base.update(params, {
            '_terp_action': action_id,
            '_terp_domain': obj.domain,
            '_terp_context': obj.context,
            '_terp_id': id,
            '_terp_model': relation
        });

        window.open(openobject.http.getURL(act, params));

    });
}

function on_context_menu(evt) {

    if (! evt.modifier().ctrl) {
        return;
    }

    var target = evt.target();
    var kind = getNodeAttribute(target, 'kind');

    if (! kind || target.disabled) {
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
                'src': '#', 'frameborder': '0', 'scrolling' :'no',
                'style':'position: absolute; display: none;'
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

function open_url(site) {
    var web_site;

    isIE = /msie/.test(navigator.userAgent.toLowerCase());

    if (isIE && site.indexOf('@') > -1) {
        site = site.split('@');
        site = site[1]
    }

    if (site.indexOf("://") == -1) {
        web_site = 'http://' + site;
    } else {
        web_site = site;
    }

    if (site.length > 0) {
        window.open(web_site);
    }
}

function submenu_action(action_id, model) {
    window.location.href = openobject.http.getURL("/openerp/form/action_submenu", {
        _terp_action_id: action_id,
        _terp_model: model,
        _terp_id: $('_terp_id').value
    });
}

function show_wkf() {

    if ($('_terp_list')) {
        var lst = new ListView('_terp_list');
        var ids = lst.getSelectedRecords();

        if (ids.length < 1)
            return alert(_('You must select at least one record.'));
        id = ids[0]
    } else {
        id = $('_terp_id') && $('_terp_id').value!='False' ? $('_terp_id').value : null;        
    }
    
    openobject.tools.openWindow(openobject.http.getURL('/view_diagram/workflow', {model: $('_terp_model').value, rec_id:id}));
}

function removeAttachment(e, element, id) {
    var element = jQuery('#' + element);
	var parent = element.parent();
	
	// set the x and y offset of the poof animation from cursor position
	var xOffset = 100;
    var yOffset = 19;
	
	jQuery.ajax({
		url: '/attachment/removeAttachment/',
		type: 'POST',
		data: {'id': id},
		dataType: 'json',
		success: function(obj) {
			
            // remove clicked element from the document tree
            jQuery(element).fadeOut('fast');
            jQuery(element).remove();
            
            jQuery('.poof').css({
                left: e.pageX - xOffset + 'px',
                top: e.pageY - yOffset + 'px'
            }).show(); // display the poof
            
            animatePoof()
            
	       if(parent.children().length == 0) {
	       	   parent.remove();
	       	   jQuery('#sideheader-a').remove();
	       }
		}
	});
}

function animatePoof() {
	var bgTop = 0; // initial background-position for the poof sprit is '0 0'
    var frames = 5; // number of frames in the sprite animation
    var frameSize = 32; // size of poof <div> in pixels (32 x 32 px in this example)
    var frameRate = 80; // set length of time each frame in the animation will display (in milliseconds)

    // loop through amination frames
    // and display each frame by resetting the background-position of the poof <div>
    for(i=1; i<frames; i++) {
        jQuery('.poof').animate({
            backgroundPosition: '0 ' + (bgTop - frameSize) + 'px'
        }, frameRate);
        bgTop -= frameSize; // update bgPosition to reflect the new background-position of our poof <div>
    }
    
    // wait until the animation completes and then hide the poof <div>
    setTimeout("jQuery('.poof').hide()", frames * frameRate);
}
