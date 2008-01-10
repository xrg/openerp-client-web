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

var ResizableTextarea = function(ta){
    this.__init__(ta);
}

ResizableTextarea.prototype = {
    
    __init__ : function(ta){
        this.textarea = MochiKit.DOM.getElement(ta);
        this.gripper = DIV({'class' : 'grip'});
        
        this.ta = this.textarea.cloneNode(true);
        
        MochiKit.DOM.swapDOM(this.textarea, DIV({'class' : 'resizable-textarea'}, this.ta, this.gripper));
        
        this.textarea = MochiKit.DOM.getElement(this.ta);        
        this.draggin = false;
        
        this.evtMouseDn = MochiKit.Signal.connect(this.gripper, 'onmousedown', this, "dragStart");
    },
    
    __delete__ : function(){
        MochiKit.Signal.disconnect(this.evtMouseDn);
    },
    
    dragStart : function(evt){
        
        if (!evt.mouse().button.left) 
            return;

        this.offset = elementDimensions(this.textarea).h - evt.mouse().page.y;
        
        this.evtMouseMv = MochiKit.Signal.connect(document, 'onmousemove', this, "dragUpdate");
        this.evtMouseUp = MochiKit.Signal.connect(document, 'onmouseup', this, "dragStop");
    },
    
    dragUpdate : function(evt){
        var h = Math.max(32, this.offset + evt.mouse().page.y);
        this.textarea.style.height = h + 'px';
	evt.stop();
    },
    
    dragStop : function(evt){
        //MochiKit.Signal.disconnect(this.evtMouseMv);
        //MochiKit.Signal.disconnect(this.evtMouseUp);
        MochiKit.Signal.disconnectAll(document, 'onmousemove', this, "dragUpdate");
        MochiKit.Signal.disconnectAll(document, 'onmouseup', this, "dragStop");
	evt.stop();
    }
}

if (! /webkit/.test(navigator.userAgent.toLowerCase())){
    MochiKit.DOM.addLoadEvent(function(evt){
        var tas = getElementsByTagAndClassName('textarea', null, 'view_form');
        forEach(tas, function(ta){
            new ResizableTextarea(ta);
        });
    })
}
