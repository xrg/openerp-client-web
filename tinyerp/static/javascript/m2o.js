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
	this.text =	$(name + '_text');
	
	this.create_button = $(name + '_create');
	this.select_button = $(name + '_select');
		
	this.callback = getNodeAttribute(this.field, 'callback');
	this.relation = getNodeAttribute(this.field, 'relation');
	this.domain = getNodeAttribute(this.field, 'domain');
	this.context = getNodeAttribute(this.field, 'context');
	
	connect(this.field, 'onchange', this, this.on_change);
	//connect(this.text, 'onchange', this, this.on_change_text);
	connect(this.text, 'onkeydown', this, this.on_keydown);
	
	connect(this.create_button, 'onclick', this, this.create);
	connect(this.select_button, 'onclick', this, this.select);
}

ManyToOne.prototype.select = function(evt){
	if (this.field.value)
		this.open(this.field.value);
	else
		open_search_window(this.relation, this.domain, this.context, this.name, 1, this.text.value);
}

ManyToOne.prototype.create = function(evt){
	this.open();
}

ManyToOne.prototype.open = function(id){

	act = getURL('/openm2o/edit', {_terp_model: this.relation, _terp_view_mode: '[form,tree]', _terp_m2o: this.name, _terp_id: id});
	
	// generate unique popup window name
    wname = 'select_' + this.relation.replace('.', '_');
    if (window.opener){
        if (typeof window.popup_counter == "undefined")
            window.popup_counter = 0;

        window.popup_counter += 1;
        wname += window.popup_counter;
    }

	wopen(act, wname, 800, 600);
}

ManyToOne.prototype.get_text = function(evt){

    if (this.field.value == ''){
        this.text.value = '';
	}

    if (this.field.value){
        var req = Ajax.get('/search/get_name', {model: this.relation, id : this.field.value});
        var text_field = this.text;
        
        req.addCallback(function(xmlHttp){
            var res = evalJSONRequest(xmlHttp);
            text_field.value = res['name'];
        });
    }
}

ManyToOne.prototype.on_change = function(evt){

	this.get_text(evt);
	
	if (this.callback) {
		onChange(this.name);
	}
}

ManyToOne.prototype.on_change_text = function(evt){
	if (this.text.value == ''){
		this.field.value = '';
		this.on_change(evt);
	}else{
		this.get_text();
	}
}

ManyToOne.prototype.on_keydown = function(evt){

	var key = evt.event().keyCode;

	if (key == 8 || key == 46){
		this.text.value = '';
		this.field.value = '';
		this.on_change(evt);
	}

	if (key == 13 && this.text.value && !this.field.value){
		this.get_matched();
	}
}

ManyToOne.prototype.get_matched = function(){

	var m2o = this;
	
	var do_get_matched = function(relation, text, domain, context){

		req2 = Ajax.get('/search/get_matched', {model: relation, text: text, _terp_domain: domain, _terp_context: context});
						
		req2.addCallback(function(xmlHttp){
			var ids = evalJSONRequest(xmlHttp)['ids'];
				
			if (ids.length == 1) {
				m2o.field.value = ids[0];
				m2o.on_change();
			}else{
				open_search_window(relation, domain, context, m2o.name, 1, text);
			}
		});
	}

	var req = eval_domain_context_request({source: this.name, domain: this.domain, context: this.context});
	
	req.addCallback(function(xmlHttp){
		res = evalJSONRequest(xmlHttp);
		do_get_matched(m2o.relation, m2o.text.value, res.domain, res.context);
	});
}
