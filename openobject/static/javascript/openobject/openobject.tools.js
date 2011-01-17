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

openobject.tools = {

    openWindow: function(anchor, options) {

        var opts = jQuery.extend({
            name        : 'win' + Math.round(Math.random() * 100000),
            center      : true,
            x           : -1,
            y           : -1,
            width       : 800, //screen.availWidth - 200,
            height      : 600, //screen.availHeight - 200,
            scrollbars  : true,
            fullscreen  : false,
            menubar     : false,
            locationbar : false,
            resizable   : true,
            autosize    : true,
            toolbar     : false
        }, options || {});

        //opts.width = opts.width > 0 ? opts.width : 800;
        //opts.height = opts.height > 0 ? opts.height : 600;

        var args = [];

        if (opts.autosize) {
            args.push("height=", opts.fullscreen ? screen.availHeight : opts.height, ',');
            args.push("width=", opts.fullscreen ? screen.availWidth : opts.width, ',');

            if (!opts.center) {
                if(opts.x == -1) {opts.x = 0;}
                if(opts.y == -1) {opts.y = 0;}
            } else if (!opts.fullscreen) {
                opts.y = Math.floor((screen.availHeight - opts.height - (screen.height - screen.availHeight)) / 2);
                opts.x = Math.floor((screen.availWidth - opts.width - (screen.width - screen.availWidth)) / 2);
            }

            if(opts.x != -1 && opts.y != -1) {
                args.push("screenx=", opts.x, ',');
                args.push("screeny=", opts.y, ',');
                args.push("left=", opts.x, ',');
                args.push("top=", opts.y, ',');
            }
        }

        if (opts.scrollbars) {
            args.push("scrollbars=1,");
        }
        if (opts.menubar) {
            args.push("menubar=1,");
        }
        if (opts.toolbar) {
            args.push("toolbar=1,");
        }
        if (opts.locationbar) {
            args.push("location=1,");
        }
        if (opts.resizable) {
            args.push("resizable=1,");
        }
        return window.open(openobject.http.getURL(anchor), opts.name, args.join(''));

    },

    validateEmail: function(value) {
        var re = /((^[a-z]([a-z_\.]*)@([a-z_\.]*)([.][a-z]{3})$)|(^[a-z]([a-z_\.]*)@([a-z_\.]*)(\.[a-z]{3})(\.[a-z]{2})*[\s,.]*$))*/i;
        return re.test(value);
    },

    validateURL: function(value) {

    }
};

// vim: ts=4 sts=4 sw=4 si et

