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
    throw "openerp.ui is required by openerp.ui.waitbox.";
}

openerp.ui.WaitBox = function(options) {
    this.__init__(options);
};

openerp.ui.WaitBox.prototype = {

    __init__ : function(options) {
    
        this.layer = document.getElementById('WaitBoxLayer');
        this.box = document.getElementById('WaitBox');

        if (!this.layer) {
        
            this.layer = DIV({id: 'WaitBoxLayer'});
            this.box = DIV({id: 'WaitBox'});

            jQuery([this.layer, this.box]).appendTo(document.body);

            jQuery(this.box).append(DIV(null, DIV({'class': 'WaitImage'})));
        }
    },

    /**
     * Cancels and deletes the internal timer, if there is any.
     */
    clearTimeout : function () {
        clearTimeout(this.timeout);
        delete this.timeout;
    },

    show : function() {
        this.clearTimeout();

        var viewPort = jQuery(window);
        var box = jQuery(this.box);
        var x = (viewPort.width() / 2) - (box.outerWidth() / 2);
        var y = (viewPort.height() / 2) - (box.outerHeight() / 2);

        jQuery(this.layer).height(jQuery(document).height());
        jQuery([this.layer, this.box]).show();

        box.offset({
            top: Math.max(0, Math.round(y)),
            left: Math.max(0, Math.round(x))
        });
    },

    /**
     * Shows the wait box after the specified delay, unless it's explicitly showed or hidden before that.
     *
     * Creates and sets an internal timer accessible via @property timeout, this is a normal setTimeout return
     * value.
     *
     * @param delay delay before actually showing the wait box, in milliseconds (same as setTimeout)
     * @returns this
     */
    showAfter : function(delay) {
        // in case we already have a timeout, override it?
        this.clearTimeout();
        this.timeout = setTimeout(jQuery.proxy(function () {
            this.show();
        }, this), delay);
        return this;
    },

    hide : function() {
        this.clearTimeout();
        jQuery([this.box, this.layer]).hide();
    }
};
