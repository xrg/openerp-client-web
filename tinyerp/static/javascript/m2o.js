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

var ManyToOne = function(name){

    this.name = name;

    this.field = $(name);
    this.text =    $(name + '_text');

    this.select_img = $(name + '_select');

    this.callback = getNodeAttribute(this.field, 'callback');
    this.relation = getNodeAttribute(this.field, 'relation');

    connect(this.field, 'onchange', this, this.on_change);
    //connect(this.text, 'onchange', this, this.on_change_text);
    connect(this.text, 'onkeydown', this, this.on_keydown);
    connect(this.text, 'onkeypress', this, this.on_keypress);

    connect(this.select_img, 'onclick', this, this.select);

    this.change_icon();
}

ManyToOne.prototype.select = function(evt){
    if (this.field.value) {
        this.open(this.field.value);
    } else {
        open_search_window(this.relation, 
                           getNodeAttribute(this.field, 'domain'), 
                           getNodeAttribute(this.field, 'context'), 
                           this.name, 1, this.text.value);
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
        openWindow(getURL('/openm2o/edit', {model: model, id: id, 
                                            domain: obj.domain, context: obj.context, 
                                            source: source}));
    });
}

ManyToOne.prototype.get_text = function(evt){

    if (this.field.value == ''){
        this.text.value = '';
    }

    if (this.field.value){
        var req = Ajax.JSON.get('/search/get_name', {model: this.relation, id : this.field.value});
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
    if (key == 113 || (key == 13 && !this.text.value)){
        this.select(evt);
        evt.stop();
    }
}

ManyToOne.prototype.on_keypress = function(evt){

    if (evt.event().keyCode == 9 ){
        return;
    }

    if ((this.field.value && evt.key().string) || evt.event().keyCode == 13){
        evt.stop();
    }
}

ManyToOne.prototype.get_matched = function(){

    var m2o = this;

    var do_get_matched = function(relation, text, domain, context){

        var req2 = Ajax.JSON.get('/search/get_matched', {model: relation, text: text, 
                                                         _terp_domain: domain, 
                                                         _terp_context: context});

        req2.addCallback(function(obj){
            if (obj.ids.length == 1) {
                m2o.field.value = obj.ids[0];
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

// vim: sts=4 st=4 et
