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

var Many2Many = function(name) {
    this.__init__(name);
}

Many2Many.prototype = {

    __init__ : function(name) {

        this.name = name;

        this.id = getElement(name + '_id');
        this.text = getElement(name + '_set');
        this.btn = getElement(name + '_button');
        this.terp_ids = getElement(name + '/_terp_ids');
        this.element = getElement(name);

        this.model = getNodeAttribute(this.id, 'relation');

        this.hasList = getElement(name + '_container') ? true : false;

        this.id.onchange = bind(this.onChange, this);       
        this.text.onchange = bind(this.onClick, this);

        if (!this.hasList) {
            MochiKit.Signal.connect(this.text, 'onkeydown', bind(function(evt){
                var key = evt.event().keyCode;

                if (key == 8 || key == 46) {
                    evt.stop();
                    this.id.value = '';
                    this.onChange();
                }
                
                if (key == 113) {
                    evt.stop();
                    this.onClick();
                }

            }, this));
        }
    },
    
    onClick : function() {
    	this.btn.onclick();
    },

    onChange : function() {

        var self = this;
        var ids = this.id.value;

        if(this.hasList) {

            req = Ajax.post('/search/get_m2m', {model: this.model, ids : ids, list_id : this.name});
            req.addCallback(function(xmlHttp){
                var listview = getElement(self.name + '_container');
                listview.innerHTML = xmlHttp.responseText;
                
                // execute JavaScript
                var scripts = getElementsByTagAndClassName('script', null, listview);
                forEach(scripts, function(s){
                   eval(s.innerHTML);
                });
            });
            
            this.terp_ids = '[' + ids + ']';
            this.element.value = '[' + ids + ']';

        } else {
            ids = ids == '[]' ? '' : ids;
            ids = ids ? ids.split(',') : [];

            this.text.value = '(' + ids.length + ')';
            ids = '[' + ids + ']';
            this.element.value = ids;
        }
    },

    selectAll : function(){
        if (this.hasList) {
            new ListView(this.name).checkAll();
        }
    },

    setValue : function(ids){

        var self = this;

        if (this.hasList) {

            req = Ajax.post('/search/get_m2m', {model: this.model, ids : ids, list_id: this.name});

            req.addCallback(function(xmlHttp) {
                var listview = getElement(self.name + '_container');
                listview.innerHTML = xmlHttp.responseText;
                
                // execute JavaScript
                var scripts = getElementsByTagAndClassName('script', null, listview);
                forEach(scripts, function(s){
                   eval(s.innerHTML);
                });
            });
            
            this.terp_ids = '[' + ids + ']';
            this.element.value = '[' + ids + ']';

        } else {
            this.text.value = '(' + ids.length + ')';
            this.element.value = '[' + ids + ']';
        }
    }
}

function remove_m2m_rec(name) {

    var elem = MochiKit.DOM.getElement(name + '_id');
    var terp_ids =  MochiKit.DOM.getElement(name + '/_terp_ids');
    
    var ids = eval(terp_ids.value);
    var boxes = getElementsByTagAndClassName('input', 'grid-record-selector', name + '_grid');
    
    boxes = MochiKit.Base.filter(function(box) {
        return box && (box.checked);
    }, boxes);
    
    if(boxes.length <= 0)
        return;
    
    boxes = MochiKit.Base.map(function(box) {
        return parseInt(box.value);
    }, boxes);
    
    ids = MochiKit.Base.filter(function(id) {
        return MochiKit.Base.findIdentical(boxes, id) == -1;
    }, ids);
    
    terp_ids.value = '[' + ids.join(',') + ']';
    elem.value = '[' + ids.join(',') + ']';
    elem.onchange();

    return;
}

// vim: ts=4 sts=4 sw=4 si et

