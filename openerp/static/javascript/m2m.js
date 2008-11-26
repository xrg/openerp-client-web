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

