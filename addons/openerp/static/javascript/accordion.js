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

var Accordion = function(container, options) {

    var cls = arguments.callee;
    if (!(this instanceof cls)) {
        return new cls(container, options);
    }

    this.__init__(container, options);
};

Accordion.prototype = {

    __class__: Accordion,

    __init__: function(container, options) {

        this.element = MochiKit.DOM.getElement(container);

        if (!this.element) {
            throw(container + " doesn't exist!");
        }

        MochiKit.DOM.addElementClass(this.element, "accordion");

        this.options = MochiKit.Base.update({
            duration: 0.1
        }, options || {});
        
        var titles = MochiKit.DOM.getElementsByTagAndClassName(null, "accordion-title", container);
        var contents = MochiKit.DOM.getElementsByTagAndClassName(null, "accordion-content", container);
        
        for (var i=0; i<titles.length; i++) {
            var title = titles[i];
            var content = contents[i];
            
            title._content = content;
            
            MochiKit.Signal.connect(title, "onclick", this, partial(this.activate, title));
            
            if (i > 0) {
            	MochiKit.Style.hideElement(content);
            }
            else {
            	this.current = title;
            }
			
        }
    },

    activate : function(title) {
        if (this.current) {
            this.deactivate(this.current);
        }

        if (title == this.current) {
            this.current = null;
            return;
        }

        this.current = title;

        var content = title._content;

        MochiKit.Visual.blindDown(content, {
            duration: this.options.duration,
            afterFinish: MochiKit.Base.bind(function() {
                MochiKit.Signal.signal(this, "activate", this, title);
            }, this)
        });

        MochiKit.DOM.addElementClass(title, "accordion-title-active");
        
        if(title.id) {
            openLink(openobject.http.getURL('/openerp/custom_action', {'action':title.id}))
        }
    },

    deactivate : function(title) {

        var content = title._content;

        MochiKit.Visual.blindUp(content, {
            duration: this.options.duration,
            afterFinish: MochiKit.Base.bind(function() {
                MochiKit.Signal.signal(this, "deactivate", this, title);
            }, this)
        });

        MochiKit.DOM.removeElementClass(title, "accordion-title-active");
    },

    repr: function() {
        return "[Accordion]";
    },

    toString: MochiKit.Base.forwardCall("repr")

};
