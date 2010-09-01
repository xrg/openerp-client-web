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
    
    var elem = getElement(name);
    if (elem._m2o) {
        return elem._m2o;
    }

    var cls = arguments.callee;
    if (!(this instanceof cls)) {
        return new cls(name);
    }

    this.__init__(name);
}

ManyToOne.prototype.__init__ = function(name){
    
    this.name = name;

    this.field = $(name);
    this.relation = getNodeAttribute(this.field, 'relation');
    this.editable = getElement('_terp_editable') ? getElement('_terp_editable').value : 'True';
    if (this.editable == 'True' && this.field.tagName.toLowerCase() != 'span'){
	    this.text = $(name + '_text');
	
	    this.select_img = $(name + '_select');    
	    this.open_img = $(name + '_open');
	    
	    this.reference = $(name + '_reference'); // reference widget
	
	    this.callback = getNodeAttribute(this.field, 'callback');    
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
	    
	    this.is_inline = name.indexOf('_terp_listfields/') == 0;
	
	    this.field._m2o = this;
	
	    this.change_icon();
    }
}

ManyToOne.prototype.select = function(evt){
	
	if (this.field.disabled) {
		return;
	}	
    if(this.field_class.indexOf('readonlyfield') == -1) {
        this.get_matched();
    }
}

ManyToOne.prototype.open_record = function(evt){
	var link = getNodeAttribute(this.field, 'link');
	this.field.value = this.field.value || getNodeAttribute(this.field, 'value');
	if(!(link==0)){
		if (this.field.value) {
			this.open(this.field.value);
		}
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
    var editable = this.editable || 'True';
    
    if (editable ==  'True' && this.field.tagName.toLowerCase() != 'span'){
	    // To open popup form in readonly mode.
	    if (this.field_class.indexOf('readonlyfield') != -1) {
	        var editable = 'False';
	    }
	}

    var req = eval_domain_context_request({source: source, domain: domain, context: context});
    var self = this;
    req.addCallback(function(obj){
		if (editable == 'True'){
		    var editable =  self.field.tagName.toLowerCase() != 'span'? 'False': 'True';
			openWindow(getURL('/openm2o/edit', {_terp_model: model, _terp_id: id,
	                                            _terp_domain: obj.domain, _terp_context: obj.context,
	                                            _terp_m2o: source, _terp_editable: editable}));
        }
        else{
        	window.location.href = getURL("/form/view",{'model': model, 'id': id, 'domain': obj.domain, 'context': obj.context})
		}
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
	form_hookAttrChange();
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

    var link = getNodeAttribute(this.field, 'link');
    if (link == 0){
    	this.open_img.src = '/static/images/stock-disabled/gtk-open.png';
    	this.open_img.style.cursor = '';
    }
    else{
    	this.open_img.src = '/static/images/stock' + (this.field.value ? '/gtk-open' : '-disabled/gtk-open') + '.png';
    }

    if (!this.field.value) {
        this.open_img.style.cursor = '';
    }
    
    if (this.is_inline) {
    
        if (this.field.value) {
            this.select_img.parentNode.style.display = 'none';
            this.open_img.parentNode.style.display = '';
        } else {
            this.select_img.parentNode.style.display = '';
            this.open_img.parentNode.style.display = 'none';
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

	var domain = getNodeAttribute(this.field, 'domain');
    var context = getNodeAttribute(this.field, 'context');

	var req = eval_domain_context_request({source: this.name, domain: domain, context: context});

    req.addCallback(function(obj){
        text = m2o.field.value ? '' : m2o.text.value;

        var req2 = Ajax.JSON.post('/search/get_matched', {model: m2o.relation, text: text,
                                                         _terp_domain: obj.domain,
                                                         _terp_context: obj.context});

        req2.addCallback(function(obj2){
            if (text && obj2.values.length == 1) {
                val = obj2.values[0];
                m2o.field.value = val[0];
                m2o.text.value = val[1];
                m2o.on_change();
            }else{
                open_search_window(m2o.relation, domain, obj.context, m2o.name, 1, text);
            }
        });
    });
}

ManyToOne.prototype.setReadonly = function(readonly) {

    this.field.readOnly = readonly;
    this.field.disabled = readonly;
    this.text.readOnly = readonly;
    this.text.disabled = readonly;

    if (readonly) {
        MochiKit.DOM.addElementClass(this.field, 'readonlyfield');
        MochiKit.DOM.addElementClass(this.text, 'readonlyfield');
    } else {
        MochiKit.DOM.removeElementClass(this.field, 'readonlyfield');
        MochiKit.DOM.removeElementClass(this.text, 'readonlyfield');
    }
}

// vim: ts=4 sts=4 sw=4 si et

