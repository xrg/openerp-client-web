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

var getURL = function(path, args) {
    var qs = args ? queryString(args) : null;
    return qs ? path + "?" +  qs : path;
}

function validate_email(email) {
    var re  = /(^[a-z]([a-z_\.]*)@([a-z_\.]*)([.][a-z]{3})$)|(^[a-z]([a-z_\.]*)@([a-z_\.]*)(\.[a-z]{3})(\.[a-z]{2})*$)/i;
    return re.test(email);
}

function getElementsByAttribute(/*...*/) {

    
    var elems = document.getElementsByTagName('*');
    var exprs = {};
    
    for(var i=0; i<arguments.length; i++) {
    
        var arg = arguments[i];
        
        if (typeof(arg) == "string") {
            exprs[arg] = null; 
        } else {
            var a = arg[0];
            var x = arg[1];
            var c = "=";
            
            if (/[~*!^$]=/.test(x)) {
                c = x.slice(0, 2);
                x = x.slice(2);
            } 
            else if (/=/.test(x)) {
                c = x.slice(0, 1);
                x = x.slice(1);
            }
            exprs[a] = [c, x];
        }
    }
    
    //log(keys(exprs));
    
    return MochiKit.Base.filter(function(e){
    
        for(var a in exprs) {
        
            var v = MochiKit.DOM.getNodeAttribute(e, a);
            if (v == null || typeof(v) != 'string') return false;
            
            var x = exprs[a];
            if (!x) continue;
            
            var c = x[0];
            var x = x[1];
        
            switch(c) {
                case '^=': 
                    if (!v.match('^' + x)) return false;
                    break;
                case '$=': 
                    if (!v.match(x + '$')) return false;
                    break;
                case '~=':
                case '*=':
                    if (!v.match(x)) return false;
                    break;
                case '=' : 
                    if (v != x) return false;
                    break;
            }
        }
        return true;
        
    }, elems);
}

function set_cookie(name, value) {
    document.cookie = name + "=" + escape(value) + "; path=/";
}

function get_cookie(name) {
    var dc = document.cookie;
    var prefix = name + "=";
    var begin = dc.indexOf("; " + prefix);
    if (begin == -1) {
        begin = dc.indexOf(prefix);
        if (begin != 0) return null;
    } else {
        begin += 2;
    }
    var end = document.cookie.indexOf(";", begin);
    if (end == -1) {
        end = dc.length;
    }
    return unescape(dc.substring(begin + prefix.length, end));
}

function del_cookie(name) {
    document.cookie = name + "=; path=/;expires=Thu, 01-Jan-1970 00:00:01 GMT";
}

function openWindow(anchor, options) {

    var opts = MochiKit.Base.update({
        name        : 'win' + Math.round(Math.random()*100000),
        center      : true,
        x           : null,
        y           : null,
        width       : 800, //screen.availWidth - 200,
        height      : 600, //screen.availHeight - 200,
        scrollbars  : true,
        fullscreen  : false,
        menubar     : false,
        locationbar : false,
        resizable   : true
    }, options || {});

    //opts.width = opts.width > 0 ? opts.width : 800;
    //opts.height = opts.height > 0 ? opts.height : 600;

    var args = '';

    args += "height=" + (opts.fullscreen ? screen.availHeight : opts.height) + ",";
    args += "width=" + (opts.fullscreen ? screen.availWidth : opts.width) + ",";
    
    if (!opts.center) {
        opts.x = 0;
        opts.y = 0;
        args += "screenx=" + opts.x + ",";
        args += "screeny=" + opts.y + ",";
        args += "left=" + opts.x + ",";
        args += "top=" + opts.y + ",";
    }

    if (opts.center && !opts.fullscreen) {
        opts.y = Math.floor((screen.availHeight - opts.height - (screen.height - screen.availHeight)) / 2);
        opts.x = Math.floor((screen.availWidth - opts.width - (screen.width - screen.availWidth)) / 2);
        args += "screenx=" + opts.x + ",";
        args += "screeny=" + opts.y + ",";
        args += "left=" + opts.x + ",";
        args += "top=" + opts.y + ",";
    }

    if (opts.scrollbars) { args += "scrollbars=1,"; }
    if (opts.menubar) { args += "menubar=1,"; }
    if (opts.locationbar) { args += "location=1,"; }
    if (opts.resizable) { args += "resizable=1,"; }

    var win = window.open(anchor, opts.name, args);
    return false;

}

// browser information
window.browser = new Object;

// Internet Explorer
window.browser.isIE = /msie/.test(navigator.userAgent.toLowerCase());

// Internet Explorer 6
window.browser.isIE6 = /msie 6/.test(navigator.userAgent.toLowerCase());

// Internet Explorer 7
window.browser.isIE7 = /msie 7/.test(navigator.userAgent.toLowerCase());

// Gecko(Mozilla) derived
window.browser.isGecko = /gecko\//.test(navigator.userAgent.toLowerCase());
window.browser.isGecko18 = /rv:1.9.*gecko\//.test(navigator.userAgent.toLowerCase());
window.browser.isGecko19 = /rv:1.9.*gecko\//.test(navigator.userAgent.toLowerCase());

// Apple WebKit derived
window.browser.isWebKit = /webkit/.test(navigator.userAgent.toLowerCase());

// Opera
window.browser.isOpera = /opera/.test(navigator.userAgent.toLowerCase());



// hack to prevent cross-domain secutiry errors, if window is opened 
// from different domain.
MochiKit.DOM.addLoadEvent(function(evt){
    try {
        window.opener.document.domain;
    } catch (e) {
        window.opener = null;
    }
});

// vim: ts=4 sts=4 sw=4 si et

