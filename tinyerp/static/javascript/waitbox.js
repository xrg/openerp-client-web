///////////////////////////////////////////////////////////////////////////////
//
// Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
//
// $Id: calendar_box.js 1598 2008-01-31 05:02:08Z ame $
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

var WaitBox = function(options) {
    this.__init__(options);
}

WaitBox.prototype = {

    __init__ : function(options) {
        
        this.options = MochiKit.Base.update({
        }, options || {});

        this.layer = MochiKit.DOM.getElement('WaitBoxLayer');
        this.box = MochiKit.DOM.getElement('WaitBox');
        
        if (!this.layer) {
        
            var btnCancel = BUTTON({'class': 'button', 'type': 'button'}, 'Cancel');
            MochiKit.Signal.connect(btnCancel, 'onclick', this, this.hide);
            
            var title = this.options.title || "Please wait...";
            
            var info = DIV(null,
                        DIV({'class': 'WaitTitle'}, title),
                        DIV({'class': 'WaitImage'}, null),
                            TABLE({'class': 'WaitButtons', 'cellpadding': 2, 'width': '100%'}, 
                                TBODY(null, 
                                    TR(null,
                                        TD({'align': 'right', 'width': '100%'}, btnCancel)))));
        
            this.layer = DIV({id: 'WaitBoxLayer'});
            appendChildNodes(document.body, this.layer);
            setOpacity(this.layer, 0.3);
    
            this.box = DIV({id: 'WaitBox'});
            appendChildNodes(document.body, this.box);
        
            appendChildNodes(this.box, info);
        }
    },

    show : function() {

        setElementDimensions(this.layer, elementDimensions(document.body));
        //setElementDimensions(this.layer, getViewportDimensions());

        var w = 350;
        var h = 125;

        setElementDimensions(this.box, {w: w, h: h});
        
        var vd = elementDimensions(document.body);
        var md = elementDimensions(this.box);

        var x = (vd.w / 2) - (w / 2);
        var y = (vd.h / 2) - (h / 2);

        x = Math.max(0, x);
        y = Math.max(0, y);
        
        log(x, y);

        setElementPosition(this.box, {x: x, y: y});

        showElement(this.layer);
        showElement(this.box);
    },

    hide : function() {
        hideElement(this.box);
        hideElement(this.layer);
    }
}

// vim: sts=4 st=4 et
