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

var getURL = function(path, args) {
    var qs = args ? queryString(args) : null;
    return qs ? path + "?" +  qs : path;
}

function validate_email(email) {
    var re  = /(^[a-z]([a-z_\.]*)@([a-z_\.]*)([.][a-z]{3})$)|(^[a-z]([a-z_\.]*)@([a-z_\.]*)(\.[a-z]{3})(\.[a-z]{2})*$)/i;
    return re.test(email);
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

/**
*
*  Javascript open window
*  http://www.webtoolkit.info/
*
**/

function openWindow(anchor, options) {

    var args = '';

    if (typeof(options) == 'undefined') { var options = new Object(); }
    if (typeof(options.name) == 'undefined') { options.name = 'win' + Math.round(Math.random()*100000); }

    // default options
    options.center = typeof(options.center) == 'undefined' ? true : options.center;
    options.width = typeof(options.width) == 'undefined' ? 800 : options.width;
    options.height = typeof(options.height) == 'undefined' ? 600 : options.height;
    options.scrollbars = typeof(options.scrollbars) == 'undefined' ? 1 : options.scrollbars;

    if (typeof(options.height) != 'undefined' && typeof(options.fullscreen) == 'undefined') {
        args += "height=" + options.height + ",";
    }

    if (typeof(options.width) != 'undefined' && typeof(options.fullscreen) == 'undefined') {
        args += "width=" + options.width + ",";
    }

    if (typeof(options.fullscreen) != 'undefined') {
        args += "width=" + screen.availWidth + ",";
        args += "height=" + screen.availHeight + ",";
    }

    if (typeof(options.center) == 'undefined') {
        options.x = 0;
        options.y = 0;
        args += "screenx=" + options.x + ",";
        args += "screeny=" + options.y + ",";
        args += "left=" + options.x + ",";
        args += "top=" + options.y + ",";
    }

    if (typeof(options.center) != 'undefined' && typeof(options.fullscreen) == 'undefined') {
        options.y=Math.floor((screen.availHeight-(options.height || screen.height))/2)-(screen.height-screen.availHeight);
        options.x=Math.floor((screen.availWidth-(options.width || screen.width))/2)-(screen.width-screen.availWidth);
        args += "screenx=" + options.x + ",";
        args += "screeny=" + options.y + ",";
        args += "left=" + options.x + ",";
        args += "top=" + options.y + ",";
    }

    if (typeof(options.scrollbars) != 'undefined') { args += "scrollbars=1,"; }
    if (typeof(options.menubar) != 'undefined') { args += "menubar=1,"; }
    if (typeof(options.locationbar) != 'undefined') { args += "location=1,"; }
    if (typeof(options.resizable) != 'undefined') { args += "resizable=1,"; }

    var win = window.open(anchor, options.name, args);
    return false;

}

// vim: sts=4 st=4 et
