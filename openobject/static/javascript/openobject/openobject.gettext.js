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

openobject.gettext = {

    MESSAGES: {},

    ugettext: function(key) {
        try {
            return this.MESSAGES[key] || key;
        } catch(e) {
        }
        return key;
    },

    update: function(messages) {
        MochiKit.Base.update(this.MESSAGES, messages);
    }

};

window._ = function(key) {
    return openobject.gettext.ugettext(key);
};


// vim: ts=4 sts=4 sw=4 si et

