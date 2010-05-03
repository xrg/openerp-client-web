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
            return false;
        }

        MochiKit.DOM.addElementClass(this.element, "accordion");

        this.options = MochiKit.Base.update({
            duration: 0.5
        }, options || {});

        var accordions = MochiKit.DOM.getElementsByTagAndClassName(null, "accordion-block", container);

        MochiKit.Iter.forEach(accordions, function(accordion) {

            var title = getElementsByTagAndClassName(null, "accordion-title", accordion)[0];
            var content = getElementsByTagAndClassName(null, "accordion-content", accordion)[0];

            title._content = content;

            MochiKit.Signal.connect(title, "onclick", this, partial(this.activate, title));
            MochiKit.Style.hideElement(content);

            this.current = title;

        }, this);
    },

    activate : function(title) {

        if (this.animate) {
            return;
        }

        if (this.current) {
            this.deactivate(this.current);
        }

        if (title == this.current) {
            this.current = null;
            return;
        }

        this.current = title;
        this.animate = true;

        var content = title._content;

        MochiKit.Visual.blindDown(content, {
            duration: this.options.duration,
            afterFinish: MochiKit.Base.bind(function() {
                this.animate = false;
                MochiKit.Signal.signal(this, "activate", this, title);
            }, this)
        });

        MochiKit.DOM.addElementClass(title, "accordion-title-active");
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
