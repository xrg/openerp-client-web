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

if (typeof(MochiKit) == "undefined") {
    throw "MochiKit is required.";
}

var openobject;
if (typeof(openobject) == "undefined") {
    openobject = {};
    window.openobject = openobject;
}

openobject.base = {
    filter: function(items, callback, instance) {
        if (instance) {
            callback = MochiKit.Base.bind(callback, instance);
        }
        return MochiKit.Base.filter(callback, items);
    },

    map: function(items, callback, instance) {
        if (instance) {
            callback = MochiKit.Base.bind(callback, instance);
        }
        return MochiKit.Base.map(callback, items);
    },

    each: function(items, callback, instance) {
        return MochiKit.Iter.forEach(items, callback, instance);
    },

    find: function(items, value, start, end) {
        return MochiKit.Base.findIdentical(items, value, start, end);
    }
};

// browser information
openobject.browser = {
    // Internet Explorer
    isIE: /msie/.test(navigator.userAgent.toLowerCase()),

    // Internet Explorer 6
    isIE6: /msie 6/.test(navigator.userAgent.toLowerCase()),

    // Internet Explorer 7
    isIE7: /msie 7/.test(navigator.userAgent.toLowerCase()),

    // Gecko(Mozilla) derived
    isGecko: /gecko\//.test(navigator.userAgent.toLowerCase()),

    isGecko18: /rv:1.9.*gecko\//.test(navigator.userAgent.toLowerCase()),

    isGecko19: /rv:1.9.*gecko\//.test(navigator.userAgent.toLowerCase()),

    // Apple WebKit derived
    isWebKit: /webkit/.test(navigator.userAgent.toLowerCase()),

    // Opera
    isOpera: /opera/.test(navigator.userAgent.toLowerCase())
};

window.browser = openobject.browser;

// hack to prevent cross-domain security errors, if window is opened
// from different domain.
jQuery(document).ready(function() {
    try {
        window.opener.document.domain;
    } catch (e) {
        window.opener = null;
    }
});

// monkey patching in order to bring indexOf() on arrays for Internet Explorer
if (!Array.prototype.indexOf) {
    Array.prototype.indexOf = function (obj, start) {
        for (var i = (start || 0); i < this.length; i++) {
            if (this[i] == obj) {
                return i;
            }
        }
        return -1;
    }
}
