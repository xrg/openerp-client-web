////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY OpenERP SA. All Rights Reserved.
//
// $Id$
//
// Developed by OpenERP (http://openerp.com) and Axelor (http://axelor.com).
//
// The OpenERP web client is distributed under the "OpenERP Public License".
// It's based on Mozilla Public License Version (MPL) 1.1 with following 
// restrictions:
//
// -   All names, links and logos of OpenERP must be kept as in original
//     distribution without any changes in all software screens, especially
//     in start-up page and the software header, even if the application
//     source code has been changed or updated or code has been added.
//
// You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
//
////////////////////////////////////////////////////////////////////////////////

var openerp;
if (!openerp && !openerp.ui) {
    throw "openerp.ui is required by openerp.ui.textarea.";
}

/**
 * @event onresize triggered when the widget's grip is moved (to resize the text area)
 *  @parameter 'the TextArea instance'
 */
openerp.ui.TextArea = function(ta) {
    this.__init__(ta);
};

openerp.ui.TextArea.prototype = {

    __init__ : function(ta) {
        this.textarea = jQuery('textarea#' + ta)[0];
        this.gripper = DIV({'class' : 'grip'});

        this.ta = this.textarea.cloneNode(true);

        MochiKit.DOM.swapDOM(this.textarea,
                DIV({'class' : 'resizable-textarea'},
                    this.ta, this.gripper)).textarea = this;

        this.textarea = openobject.dom.get(this.ta);
        this.draggin = false;

        this.evtMouseDn = MochiKit.Signal.connect(this.gripper, 'onmousedown', this, "dragStart");
    },

    __delete__ : function() {
        MochiKit.Signal.disconnect(this.evtMouseDn);
    },

    dragStart : function(evt) {
        if (!evt.mouse().button.left) {
            return;
        }

        this.offset = openobject.dom.height(this.textarea) - evt.mouse().page.y;

        this.evtMouseMv = MochiKit.Signal.connect(document, 'onmousemove', this, "dragUpdate");
        this.evtMouseUp = MochiKit.Signal.connect(document, 'onmouseup', this, "dragStop");
    },

    dragUpdate : function(evt) {
        var h = Math.max(32, this.offset + evt.mouse().page.y);
        this.textarea.style.height = h + 'px';
        MochiKit.Signal.signal(this, 'onresize', this);
        evt.stop();
    },

    dragStop : function(evt) {
        //MochiKit.Signal.disconnect(this.evtMouseMv);
        //MochiKit.Signal.disconnect(this.evtMouseUp);
        MochiKit.Signal.disconnectAll(document, 'onmousemove', this, "dragUpdate");
        MochiKit.Signal.disconnectAll(document, 'onmouseup', this, "dragStop");
        evt.stop();
    }
};
