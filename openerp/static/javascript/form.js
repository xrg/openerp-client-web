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

function get_form_action(action, params){
    
    var act = typeof(form_controller) == 'undefined' ? '/form' : form_controller;
    act = action && action.indexOf('/') == 0 ? action : act + '/' + action;

    return getURL(act, params);
}

var openRecord = function(id, src, target, readonly){

    var kind = getNodeAttribute(src + '_set', 'kind');
    
    if (!kind && getElement('_o2m_' + src)) {
        kind = "one2many";
    }
        
    if (kind == "one2many") {
        return new One2Many(src).edit(id, readonly);
    }
    
    var prefix = src && src != '_terp_list' ? src + '/' : '';

    var model = $(prefix + '_terp_model').value;
    var view_ids = $(prefix + '_terp_view_ids').value;
    var view_mode = $(prefix + '_terp_view_mode').value;

    var ids = $(prefix + '_terp_ids').value;

    var offset = $(prefix + '_terp_offset').value;
    var limit = $(prefix + '_terp_limit').value;
    var count = $(prefix + '_terp_count').value;

    var domain = $(prefix + '_terp_domain').value;
    var context = $(prefix + '_terp_context').value;

    var search_domain = $('_terp_search_domain');
    search_domain = search_domain ? search_domain.value : null;

    var args = {'model': model,
                'id': id ? id : 'False',
                'ids': ids,
                'view_ids': view_ids,
                'view_mode': view_mode,
                'domain': domain,
                'context': context,
                'offset': offset,
                'limit': limit,
                'count': count,
                'search_domain': search_domain};
                
    var action = readonly ? 'view' : 'edit';
        
    if (target == '_blank') {
        return window.open(get_form_action(action, args));
    }
    
    if (kind == 'many2many') {
        args['source'] = src;
        return openWindow(get_form_action('/openm2m/edit', args));
    }

    window.location.href = get_form_action(action, args);
}

var editRecord = function(id, src, target){
    return openRecord(id, src, target, false);
}

var viewRecord = function(id, src){
    return openRecord(id, src, null, true);
}

var editSelectedRecord = function() {

    var lst = new ListView('_terp_list');
    var ids = lst.getSelectedRecords();
    
    if (ids && ids.length > 5) {
        var msg = _('You selected to open %(tabs)s tabs - do you want to continue?');
        msg = msg.replace('%(tabs)s', ids.length);
        if (!confirm(msg)) return;
    }

    forEach(ids, function(id){
        editRecord(id, '_terp_list', '_blank');
    });
}

var switchView = function(view_type, src){

    var prefix = src ? src + '/' : '';
    var form = document.forms['view_form'];

    var params = {
        '_terp_source': src,
        '_terp_source_view_type': view_type
    }

    if (getElement('_terp_list')){
        var ids = new ListView('_terp_list').getSelectedRecords();
        if (ids.length > 0) {
            $('_terp_id').value = ids[0];
        }
    }

    submit_form(get_form_action('switch', params));
}

var switch_O2M = function(view_type, src){
    
    if (Ajax.COUNT > 0){
        return;
    }
    
    var prefix = src ? src + '/' : '';
    var form = document.forms['view_form'];
	
    var params = getFormParams();
    
    params['_terp_source'] = src;
    params['_terp_source_view_type'] = view_type;
    params['_terp_editable'] = $(prefix + '_terp_editable').value
    
    if (getElement('_terp_list')){
        var ids = new ListView('_terp_list').getSelectedRecords();
        if (ids.length > 0) {
            $('_terp_id').value = ids[0];
        }
    }
    
    req = Ajax.post('/form/switch_o2m', params);
    req.addCallback(function(xmlHttp){
    
        var text = xmlHttp.responseText;
        if (text.indexOf('ERROR: ') == 0) {
            text = text.replace('ERROR: ', '');
            return alert(text);
        }

        var frm = getElement('_o2m_'+src);
        
        var d = DIV();
        d.innerHTML = text;
        
        var newo2m = d.getElementsByTagName('table')[0];
        
        swapDOM(frm, newo2m);

        var ua = navigator.userAgent.toLowerCase();

        if ((navigator.appName != 'Netscape') || (ua.indexOf('safari') != -1)) {
            // execute JavaScript
            var scripts = getElementsByTagAndClassName('script', null, newo2m);
            forEach(scripts, function(s){
                eval(s.innerHTML);
            });
        }
    });
}

var show_process_view = function() {
    var model = getElement('_terp_model').value;
    var id = getElement('_terp_id').value;

    if (getElement('_terp_list')) {
        var list = new ListView('_terp_list');
        var ids = list.getSelectedRecords();
        if (ids.length)
            id = ids[0];
    }

    id = parseInt(id) || null;

    window.open(getURL('/process', {res_model: model, res_id: id}));
}

var validate_required = function(form) {

    if (typeof form == 'string') {
       form = document.forms[form];
    }

    if (!form) return true;

    var elements = MochiKit.Base.filter(function(el) {
       return !el.disabled && el.id && el.name && el.id.indexOf('_terp_listfields/') == -1 && hasElementClass(el, 'requiredfield');
    }, form.elements);

    var result = true;

    for (var i=0; i<elements.length; i++){

        var elem = elem2 = elements[i];
        var value = elem.value;
        var kind = MochiKit.DOM.getNodeAttribute(elem, 'kind');

        if (kind == 'many2many') {
            elem2 = MochiKit.DOM.getElement(elem.name + '_set') || elem;
            value = value == '[]' ? '' : value;
        }

        if (kind == 'many2one' || kind == 'reference') {
            elem2 = MochiKit.DOM.getElement(elem.id + '_text') || elem;
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

var submit_form = function(action, src, target){
    
    if (Ajax.COUNT > 0) {
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
   
    if (target == "new" || target == "_blank"){
        setNodeAttribute(form, 'target', '_blank');
    }
    
    if (action == 'save_and_edit'){
        action = 'save';
        args['_terp_return_edit'] = 1;
    }

    action = get_form_action(action, args);

    if (/\/save(\?|\/)?/.test(action) && !validate_required(form)){
        return false;
    }
    
    form.attributes['action'].value = action;    
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

var clear_search_form = function() {

    if ($('search_view_notebook')) {

        var fields = [];

        fields = fields.concat(getElementsByTagAndClassName('input', null, 'search_view_notebook'));
        fields = fields.concat(getElementsByTagAndClassName('textarea', null, 'search_view_notebook'));
        fields = fields.concat(getElementsByTagAndClassName('select', null, 'search_view_notebook'));

        forEach(fields, function(fld){
            fld.value = '';
        });
    }
}

var pager_action = function(action, src) {
    return src ? new ListView(src).go(action) : submit_search_form(action);
}

var buttonClicked = function(name, btype, model, id, sure, target, context){

    if (sure && !confirm(sure)){
        return;
    }

    //var button = getElement(name);
    //var context = getNodeAttribute(button, "context");

    var params = {};

    params['_terp_button/name'] = name;
    params['_terp_button/btype'] = btype;
    params['_terp_button/model'] = model;
    params['_terp_button/id'] = id;

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

var onBooleanClicked = function(name) {

    var source = getElement(name + '_checkbox_');
    var target = getElement(name);

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
var getFormData = function(extended) {

    var parentNode = $('_terp_list') || document.forms['view_form'];

    var frm = {};
    var fields = [];
    
    var is_editable = $('_terp_editable').value == 'True';
    
    if (is_editable) {
	    fields = fields.concat(getElementsByTagAndClassName('input', null, parentNode));
	    fields = fields.concat(getElementsByTagAndClassName('select', null, parentNode));
	    fields = fields.concat(getElementsByTagAndClassName('textarea', null, parentNode));
    } else {
        fields = fields.concat(getElementsByAttribute('kind', 'value'));
        fields = fields.concat(getElementsByAttribute(['name', '$=/__id']));
    }
    
    fields = fields.concat(filter(function(e){
        return getNodeAttribute(e,'kind')=='picture';
    }, getElementsByTagAndClassName('img', null, parentNode)));
    
    for(var i=0; i<fields.length; i++) {
    
        var e = fields[i];
        var n = is_editable ? e.name : e.id;
        
        if (e.tagName.toLowerCase() != 'img' && !n)
            continue;

        var n = n.replace('_terp_listfields/', '');

        // don't include _terp_ fields except _terp_id
        if (/_terp_/.test(n) && ! /_terp_id$/.test(n))
            continue;

        // work arround to skip o2m values (list mode)
        if (n.indexOf('/__id') > 0) {
        
            n = n.replace('/__id', '');

            if ($(n + '/_terp_view_type').value == 'form') {
                frm[n+'/__id'] = $(n+'/__id').value;
                continue;
            }
            
            // skip if editable list's editors are visible
            if (getElementsByAttribute(['name', '^=_terp_listfields/' + n]).length) {
                continue;
            }
            
            var value = $(n + '/_terp_ids').value;

            if (extended) {
                value = {'value': value, 
                         'type': 'one2many', 
                         'relation': $(n + '/_terp_model').value};
                value = serializeJSON(value);
            }
            
            frm[n] = value;
            continue;
        }

        if (extended && n.indexOf('/__id') == -1) {

            var attrs = {};
            
            var value = (is_editable ? e.value : getNodeAttribute(e, 'value')) || "";
            var kind = getNodeAttribute(e, 'kind') || "char";

            //take care of _terp_id
            if (/_terp_id$/.test(n)) {

                //  only the resource id and all O2M
                n = n.replace(/_terp_id$/, '');
                if (n && !getElement(n + '__id')) {
                    continue; 
                }

                n = n + 'id';
                
                if (!getElement(n)) {
                    continue;    
                }
                
                kind = 'integer';
                value = value == 'False' ? '' : value;
            }

            attrs['value'] = typeof(value) == "undefined" ? '' : value;

            if (kind)
                attrs['type'] = kind;
                
            if (extended && (kind == 'many2one' || kind == 'many2many')){
                attrs['relation'] = getNodeAttribute(e, 'relation');
            }

            if (extended > 1 && hasElementClass(e, 'requiredfield'))
                attrs['required'] =  1;

            if (kind == "picture") {
                n = e.id;
            }
            
            if (kind == 'text_html') {
                if(tinyMCE.get(e.name))
                    attrs['value'] =  tinyMCE.get(e.name).getContent();
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
var getFormParams = function(name){

    var parentNode = document.forms['view_form'];

    var frm = {};
    var fields = getElementsByTagAndClassName('input', null, parentNode);

    forEach(fields, function(e){

        if (!e.name || e.name.indexOf('_terp_listfields/') > -1 || e.name.indexOf('_terp_') == -1)
            return

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

var onChange = function(name) {

    var caller = $(name);
    var callback = getNodeAttribute(caller, 'callback');
    var change_default = getNodeAttribute(caller, 'change_default');
    
    if (!(callback || change_default) || caller.__lock_onchange) {
        return;
    }
    
    var is_list = caller.id.indexOf('_terp_listfields') == 0;
    var prefix = caller.name || caller.id;
    prefix = prefix.slice(0, prefix.lastIndexOf('/')+1);

    var params = getFormData(1);
    var model = is_list ? $(prefix.slice(17) + '_terp_model').value : $(prefix + '_terp_model').value;
    var context = is_list ? $(prefix.slice(17) + '_terp_context').value : $(prefix + '_terp_context').value;
    var id = is_list ? $(prefix.slice(17) + '_terp_id').value : $(prefix + '_terp_id').value;

    params['_terp_caller'] = is_list ? caller.id.slice(17) : caller.id;
    params['_terp_callback'] = callback;
    params['_terp_model'] = model;
    params['_terp_context'] = context;
    params['_terp_value'] = caller.value;
    params['id'] = id;
    
    var req = Ajax.JSON.post(callback ? '/form/on_change' : '/form/change_default_get', params);

    req.addCallback(function(obj){

        if (obj.error) {
            return alert(obj.error);
        }
        
        values = obj['value'];
        domains = obj['domain'];

        domains = domains ? domains : {};

        for(var k in domains){
            fld = $(prefix + k);
            if (fld){
                setNodeAttribute(fld, 'domain', domains[k]);
            }
        }

        for(var k in values){
            
            flag = false;
            fld = $(prefix + k);

            if (!fld) continue;

            value = values[k];
            value = value === false || value === null ? '' : value;

            // prevent recursive onchange
            fld.__lock_onchange = true;

            if ($(prefix + k + '_id')){
                fld = $(prefix + k + '_id');
                flag = true;
            }

            if ((fld.value !== value) || flag) {
                fld.value = value;

                var kind = getNodeAttribute(fld, 'kind');
                
                if (kind == 'picture') {
                    fld.src = value;
                }

                if (kind == 'many2one'){
                    fld.value = value[0] || '';
                    try {
                        $(prefix + k + '_text').value = value[1] || '';
                    }catch(e){}
                }

                if (kind == 'boolean') {
                    $(prefix + k + '_checkbox_').checked = value || false;
                }
                
                
                if (kind=='text_html') {
                    if(tinyMCE.get(prefix+k))
                        tinyMCE.execInstanceCommand(prefix+k, 'mceSetContent', false, value || '')
                }
                
                if (kind=='selection') {                    
                    var opts = [];
                    opts.push(OPTION({'value': ''}))
                    
                    for (i in value) {                        
                        var item = value[i];                        
                        opts.push(OPTION({'value': item[0]}, item[1]));
                    } 
                    MochiKit.DOM.replaceChildNodes(fld, map(function(x){return x;}, opts));
                }  

                MochiKit.Signal.signal(fld, 'onchange');
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
function getName(name, relation){

    var value_field = $(name);
    var text_field = $(value_field.name + '_text');

    relation = relation ? relation : getNodeAttribute(value_field, 'relation');

    if (value_field.value == ''){
        text_field.value = ''
    }

    if (value_field.value){
        var req = Ajax.JSON.get('/search/get_name', {model: relation, id : value_field.value});
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
    if (prefix[0] == '_terp_listfields'){
        prefix.shift();
    }
    prefix = prefix.join('/');

    var params = getFormData(1);
    
    params['_terp_domain'] = options.domain;
    params['_terp_context'] = options.context;
    params['_terp_prefix'] = prefix;    
    params['_terp_active_id'] = prefix ? $(prefix + '/_terp_id').value : $('_terp_id').value;
    params['_terp_active_ids'] = prefix ? $(prefix + '/_terp_ids').value : $('_terp_ids').value;
    
    if (options.active_id) {
        params['_terp_active_id'] = options.active_id;
        params['_terp_active_ids'] = options.active_ids;
    }
        
    var parent_context = prefix ? $(prefix + '/_terp_context') : $('_terp_context');
    
    if (parent_context){
        params['_terp_parent_context'] = parent_context.value;
    }
    
    var req = Ajax.JSON.post('/search/eval_domain_and_context', params);
    return req.addCallback(function(obj){

        if (obj.error_field) {

            var fld = getElement(obj.error_field) || getElement('_terp_listfields/' + obj.error_field);

            if (fld && getNodeAttribute(fld, 'kind') == 'many2one')
            fld = getElement(fld.id + '_text');

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

    var req = eval_domain_context_request({source: source, 
                                           domain: domain, 
                                           context: context});

    if (kind == 2 && source.indexOf('_terp_listfields/') == 0) {
        text = "";
    }

    req.addCallback(function(obj){
        openWindow(getURL('/search/new', {model: relation, 
                                          domain: obj.domain, 
                                          context: obj.context, 
                                          source: source, 
                                          kind: kind, 
                                          text: text}));
    });
}

function makeContextMenu(id, kind, relation, val) {

    var form = document.forms['view_form'];
    var act = get_form_action('get_context_menu');

    var prefix = id.indexOf('/') > -1 ? id.slice(0, id.lastIndexOf('/')) + '/' : '';

    var model = prefix ? $(prefix + '_terp_model').value : $('_terp_model').value;

    var params = {'model': model, 'field': id, 'kind': kind, 'relation': relation, 'value': val};
    
    var req = Ajax.JSON.post(act, params);

    req.addCallback(function(obj) {

        var rows = [];

        for(var r in obj.defaults) {
            var o = obj.defaults[r];                        
            var a = SPAN({onclick: 'hideElement("contextmenu"); return ' + o.action}, o.text);
            rows = rows.concat(a);
        }

        if(obj.actions.length > 0) {
            rows = rows.concat(HR());

            for(var r in obj.actions) {
                var o = obj.actions[r];

                var a = SPAN({'class': o.action ? '' : 'disabled',
                           'onclick': o.action ? 'hideElement("contextmenu"); return ' + o.action : ''}, o.text);

                rows = rows.concat(a);
            }
        }

        if(obj.relates.length > 0) {
            rows = rows.concat(HR())

            for(var r in obj.relates) {
                var o = obj.relates[r];
                
                var a = SPAN({'class': o.action ? '' : 'disabled',
                              'onclick': o.action ? 'hideElement(\'contextmenu\'); return ' + o.action : '',
                              'domain': o.domain,
                              'context': o.context}, o.text);

                rows = rows.concat(a);
            }
        }

        $('contextmenu').innerHTML = '';

        var tbl = TABLE({'cellpadding': 0, 'cellspacing' : 0}, 
                    TBODY(null, map(function(r){return TR(null, TD(null, r));}, rows)));

        appendChildNodes('contextmenu', tbl);

        var vd = getViewportDimensions();
        var md = elementDimensions('contextmenu');

        var x = $('contextmenu').style.left.slice(0, -2);
        x = parseInt(x);

        if ((x + md.w) > vd.w) {
            x -= x + md.w - vd.w;
            $('contextmenu').style.left = x + 'px';
        }

        showContextMenu();
    });
}

var showContextMenu = function(){

    var menu = $('contextmenu');
    var ifrm = $('contextmenu_frm');

    showElement(menu);

    if (ifrm){

        ifrm.style.left = menu.offsetLeft + "px";
        ifrm.style.top = menu.offsetTop + "px";
        ifrm.style.width = menu.offsetWidth + "px";
        ifrm.style.height = menu.offsetHeight + "px";
        ifrm.style.zIndex = 6;

        showElement(ifrm);
    }
}

var hideContextMenu = function(){
    var menu = $('contextmenu');
    var ifrm = $('contextmenu_frm');

    if (ifrm){
        hideElement(ifrm);
    }

    hideElement(menu);
}

function set_to_default(field, model){

    var kind = getNodeAttribute($(field), 'kind');
    
    var act = get_form_action('get_default_value');
    var params = {'model': model, 'field': field};

    var req = Ajax.JSON.post(act, params);
    req.addCallback(function(obj) {

        $(field).value = obj.value;
        signal(field, "onchange");
    });
}

function set_as_default(field, model){

    var kind = getNodeAttribute($(field), 'kind');

    var args = getFormData(1);
    
    args['_terp_model'] = model;
    args['_terp_field'] = field;

    var req = Ajax.JSON.post('/fieldpref/get', args);

    req.addCallback(function(obj){
        var text = obj.text;
        var params = {'_terp_model': model, 
                      '_terp_field/name': field, 
                      '_terp_field/string': text, 
                      '_terp_field/value': $(field).value, 
                      '_terp_deps': obj.deps};
        
        openWindow(getURL('/fieldpref', params), {width: 500, height: 350});
    });
}

function do_report(id, relation) {

    id = $(id).value;

    var act = get_form_action('report');
    var params = {'_terp_model': relation, '_terp_id': id};

    window.open(getURL(act, params));
}

function do_action(action_id, field, relation, src, data) {

    var params = {};

    if ($('_terp_list')) {
        var list = new ListView('_terp_list');
        var ids = list.getSelectedRecords();

        if (ids.length == 0) {
           return alert(_('You must select at least one record.'));
        }

        params['_terp_selection'] = '[' + ids.join(',') + ']';
        var id = eval(params['_terp_selection'])[0]
    }
	else{
    	var id = $(field).value;}
    	
    var domain = getNodeAttribute(src, 'domain');
    var context = getNodeAttribute(src, 'context');
    
    var req = eval_domain_context_request({source: $(field).id,
                                           active_id: id,
                                           active_ids: params['_terp_selection'],
                                           domain: domain, 
                                           context: context});
                                           
    req.addCallback(function(obj){
          
        var act = get_form_action('action');
        MochiKit.Base.update(params, {
            '_terp_action': action_id,
            '_terp_domain': obj.domain,
            '_terp_context': obj.context,
            '_terp_id': id,
            '_terp_model': relation,
            'datas': data});

        window.open(getURL(act, params));

    });
}

function on_context_menu(evt) { 
    
    if(! evt.modifier().ctrl)
        return;
        
    var target = evt.target();
    var kind = getNodeAttribute(target, 'kind');
    
    if(! kind || target.disabled)
        return;

    var menu = $('contextmenu');

    if (!menu) {

        menu = DIV({'id': 'contextmenu', 
                    'class' : 'contextmenu', 
                    'onmouseout' : 'hideContextMenu()', 
                    'onmouseover' : 'showContextMenu()',
                    'style' : 'position: absolute; display: none;'});

        appendChildNodes(document.body, menu);

        if (/msie/.test(navigator.userAgent.toLowerCase())) {
            var ifrm = createDOM('IFRAME', {'id' : 'contextmenu_frm', 
                                            'src' : '#', 'frameborder': '0', 'scrolling' :'no', 
                                            'style':'position: absolute; display: none;'});

            appendChildNodes(document.body, ifrm);
        }
    }

    var src = target.id;
    
    if (kind == 'many2one') {
        src = src.slice(0, -5);
    }
    
    var val = $(src).value;
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
    
    if(isIE && site.indexOf('@') > -1) {
        site = site.split('@');
        site = site[1]
    }
    
    if(site.indexOf("://")== -1)
        web_site='http://'+site;
    else
        web_site = site;

    if(site.length > 0) {
        window.open(web_site);
    }
}

// vim: ts=4 sts=4 sw=4 si et

