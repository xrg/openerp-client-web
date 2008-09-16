////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
//
// $Id$
//
// Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
//
// WARNING: This program as such is intended to be used by professional
// programmers who take the whole responsibility of assessing all potential
// consequences resulting from its eventual inadequacies and bugs
// End users who are looking for a ready-to-use solution with commercial
// guarantees and support are strongly advised to contract a Free Software
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
// along with this program; if not, write to the 
// Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
// Boston, MA  02111-1307, USA.
//
////////////////////////////////////////////////////////////////////////////////

var ManyToOne = function(name){

    this.name = name;

    this.field = $(name);
    this.text =    $(name + '_text');

    this.select_img = $(name + '_select');
    this.reference = $(name + '_reference'); // reference widget

    this.callback = getNodeAttribute(this.field, 'callback');
    this.relation = getNodeAttribute(this.field, 'relation');

    connect(this.field, 'onchange', this, this.on_change);
    //connect(this.text, 'onchange', this, this.on_change_text);
    connect(this.text, 'onkeydown', this, this.on_keydown);
    connect(this.text, 'onkeypress', this, this.on_keypress);

    connect(this.select_img, 'onclick', this, this.select);
    
    if (this.reference) {
        connect(this.reference, 'onchange', this, this.on_reference_changed);
    }

    this.change_icon();
}

ManyToOne.prototype.select = function(evt){
    if (this.field.value) {
        this.open(this.field.value);
    } else if (!this.field.disabled){
        this.get_matched();
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

    var req = eval_domain_context_request({source: source, domain: domain, context: context});

    req.addCallback(function(obj){
        openWindow(getURL('/openm2o/edit', {_terp_model: model, _terp_id: id, 
                                            _terp_domain: obj.domain, _terp_context: obj.context,
                                            _terp_m2o: source}));
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
    this.select_img.src = '/static/images/stock/gtk-' + (this.field.value ? 'open' : 'find') + '.png';
}

ManyToOne.prototype.on_keydown = function(evt){
    var key = evt.event().keyCode;

    if (key == 8 || key == 46){
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
    }

    var domain = getNodeAttribute(this.field, 'domain');
    var context = getNodeAttribute(this.field, 'context');

    var req = eval_domain_context_request({source: this.name, domain: domain, context: context});

    req.addCallback(function(obj){
        do_get_matched(m2o.relation, m2o.text.value, obj.domain, obj.context);
    });
}

ManyToOne.change_icon = function(field) {
    var field = $(field);
    var img = $(field.id + '_select');
    
    img.src = '/static/images/stock/gtk-' + (field.value ? 'open' : 'find') + '.png';
}

// vim: ts=4 sts=4 sw=4 si et

