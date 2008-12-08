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

var ManyToOne = function(name){
    
    this.name = name;

    this.field = $(name);
    this.text = $(name + '_text');

    this.select_img = $(name + '_select');    
    this.open_img = $(name + '_open');
    
    this.reference = $(name + '_reference'); // reference widget

    this.callback = getNodeAttribute(this.field, 'callback');
    this.relation = getNodeAttribute(this.field, 'relation');
    this.field_class = getNodeAttribute(this.field, 'class');

    connect(this.field, 'onchange', this, this.on_change);
    //connect(this.text, 'onchange', this, this.on_change_text);
    connect(this.text, 'onkeydown', this, this.on_keydown);
    connect(this.text, 'onkeypress', this, this.on_keypress);

    if (this.select_img)
        connect(this.select_img, 'onclick', this, this.select);
    if (this.open_img)
        connect(this.open_img, 'onclick', this, this.open_record);
    
    if (this.reference) {
        connect(this.reference, 'onchange', this, this.on_reference_changed);
    }

    this.change_icon();
}

ManyToOne.prototype.select = function(evt){
    if(this.field_class.indexOf('readonlyfield') == -1) {
        this.get_matched();
    }
}

ManyToOne.prototype.open_record = function(evt){
    if (this.field.value) {
        this.open(this.field.value);
    }
}

ManyToOne.prototype.create = function(evt){
    this.open();
}

ManyToOne.prototype.open = function(id){

    var domain = getNodeAttribute(this.field, 'domain');
    var context = getNodeAttribute(this.field, 'context');

    var model = this.relation;
    var source = this.name;
    var editable = 'True';
    
    // To open popup form in readonly mode.
    if (this.field_class.indexOf('readonlyfield') != -1) {
        var editable = 'False';
    }

    var req = eval_domain_context_request({source: source, domain: domain, context: context});

    req.addCallback(function(obj){
        openWindow(getURL('/openm2o/edit', {_terp_model: model, _terp_id: id, 
                                            _terp_domain: obj.domain, _terp_context: obj.context,
                                            _terp_m2o: source, _terp_editable: editable}));
    });
}

ManyToOne.prototype.get_text = function(evt){

    if (this.field.value == ''){
        this.text.value = '';
    }

    if (this.field.value && ! this.text.value){
        var req = Ajax.JSON.post('/search/get_name', {model: this.relation, id : this.field.value});
        var text_field = this.text;

        req.addCallback(function(obj){
            text_field.value = obj.name;
        });
    }
}

ManyToOne.prototype.on_change = function(evt){

    this.get_text(evt);

    if (this.callback) {
        onChange(this.name);
    }

    this.change_icon();
}

ManyToOne.prototype.on_change_text = function(evt){
    if (this.text.value == ''){
        this.field.value = '';
        this.on_change(evt);
    }else{
        this.get_text();
    }
}

ManyToOne.prototype.on_reference_changed = function(evt) {
    
    this.text.value = '';
    this.field.value = '';
    
    this.relation = this.reference.value;
    
    MochiKit.DOM.setNodeAttribute(this.field, 'relation', this.relation);
    MochiKit.DOM.setNodeAttribute(this.text, 'relation', this.relation);
    
    this.change_icon();
}

ManyToOne.prototype.change_icon = function(evt){
    if (this.open_img) {
        this.open_img.src = '/static/images/stock' + (this.field.value ? '/gtk-open' : '-disabled/gtk-open') + '.png';
        if (!this.field.value) {
            this.open_img.style.cursor = '';
        } 
    }
}

ManyToOne.prototype.on_keydown = function(evt){
    var key = evt.event().keyCode;

    if ((key == 8 || key == 46) && this.field.value){
        this.text.value = '';
        this.field.value = '';
        this.on_change(evt);
    }

    if ((key == 13 || key == 9) && this.text.value && !this.field.value){
        this.get_matched();
    }

    // F1
    if (key == 112){
        this.create(evt);
        evt.stop();
    }

    // F2
    if (key == 113 || (key == 13 && !this.text.value && !hasElementClass(this.text, 'listfields'))){
        this.select(evt);
        evt.stop();
    }
}

ManyToOne.prototype.on_keypress = function(evt){

    if (evt.event().keyCode == 9 || evt.modifier().ctrl){
        return;
    }

    if ((this.field.value && evt.key().string) || evt.event().keyCode == 13){
        evt.stop();
    }
}

ManyToOne.prototype.get_matched = function(){
    
    if (Ajax.COUNT > 0) {
        return callLater(1, this.get_matched);
    }
    
    if (!this.relation) {
        return;
    }

    var m2o = this;

    var do_get_matched = function(relation, text, domain, context){

        var req2 = Ajax.JSON.post('/search/get_matched', {model: relation, text: text, 
                                                         _terp_domain: domain, 
                                                         _terp_context: context});
                                                         
        open_search_window(relation, domain, context, m2o.name, 1, '');
        
        /*     single word search...                                                    
        req2.addCallback(function(obj){
            if (obj.values.length == 1) {
                val = obj.values[0];
                m2o.field.value = val[0];
                m2o.text.value = val[1];
                m2o.on_change();
            }else{
                open_search_window(relation, domain, context, m2o.name, 1, text);
            }
        });
        */ 
    }

    var domain = getNodeAttribute(this.field, 'domain');
    var context = getNodeAttribute(this.field, 'context');

    var req = eval_domain_context_request({source: this.name, domain: domain, context: context});

    req.addCallback(function(obj){
        do_get_matched(m2o.relation, m2o.text.value, obj.domain, obj.context);
    });
}

ManyToOne.change_icon = function(field) {
    if(this.select_img)
        this.select_img.src = '/static/images/stock' + (this.field.value ? '/gtk-open' : '-disabled/gtk-open') + '.png';
}

// To set the widget and fields readonly based on flag.
ManyToOne.set_readonly = function(flag) {
    if(flag) {
        this.select_img.src = '/static/images/stock-disabled/gtk-find.png';
        this.open_img.src = '/static/images/stock-disabled/gtk-open.png';
        this.field_class = this.field_class + ' readonlyfield';
    }
    else {
        this.select_img.src = '/static/images/stock/gtk-find.png';
        this.open_img.src = '/static/images/stock/gtk-open.png';
    }
}

// vim: ts=4 sts=4 sw=4 si et

