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
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
////////////////////////////////////////////////////////////////////////////////

var ModalBox = function(options) {
    this.__init__(options);
}

ModalBox.prototype = {

    __init__ : function(options) {
        
        this.options = MochiKit.Base.update({
            title: 'Modalbox',  // title
            content: null,      // content
            buttons: [],        // buttons
        }, options || {});

        if (MochiKit.DOM.getElement('modalbox_overlay')){
            throw "Only one Modalbox instance is allowed per page.";
        }

        this.title = DIV({'class': 'modalbox-title'}, this.options.title);
        this.content = DIV({'class': 'modalbox-content'}, this.options.content || '');
        
        var btnCancel = BUTTON({'class': 'button', 'type': 'button'}, 'Cancel');
        MochiKit.Signal.connect(btnCancel, 'onclick', this, this.hide);

        var buttons = MochiKit.Base.map(function(btn){
            var b = MochiKit.DOM.BUTTON({'class': 'button', 'type': 'button'}, btn.text);
            MochiKit.Signal.connect(b, 'onclick', btn.onclick || MochiKit.Base.noop);
            return b;
        }, this.options.buttons || []);

        buttons.push(btnCancel);

        var content = DIV(null,
                        this.title,
                        this.content,
                            TABLE({'class': 'modalbox-buttons', 'cellpadding': 2, 'width': '100%'}, 
                                TBODY(null, 
                                    TR(null,
                                        TD({'align': 'right', 'width': '100%'}, buttons)))));
        
        this.overlay = DIV({id: 'modalbox_overlay'});
        MochiKit.DOM.appendChildNodes(document.body, this.overlay);
        MochiKit.Style.setOpacity(this.overlay, 0.7);
    
        this.box = DIV({id: 'modalbox'});
        MochiKit.DOM.appendChildNodes(document.body, this.box);        
        MochiKit.DOM.appendChildNodes(this.box, content);
    },

    show : function() {

        //setElementDimensions(this.overlay, elementDimensions(document.body));
        MochiKit.DOM.setElementDimensions(this.overlay, MochiKit.DOM.getViewportDimensions());

        var w = this.width || 0;
        var h = this.height || 0;

        MochiKit.DOM.setElementDimensions(this.box, {w: w, h: h});

        var vd = getElementDimensions(document.body);
        var md = getElementDimensions(this.box);

        var x = (vd.w / 2) - (w / 2);
        var y = (vd.h / 2) - (h / 2);

        x = Math.max(0, x);
        y = Math.max(0, y);
        
        setElementPosition(this.box, {x: x, y: y});

        showElement(this.overlay);
        showElement(this.box);

        MochiKit.Signal.signal(this, "show", this);
    },

    hide : function() {
        hideElement(this.box);
        hideElement(this.overlay);

        MochiKit.Signal.signal(this, "hide", this);
    }
}

// vim: sts=4 st=4 et
