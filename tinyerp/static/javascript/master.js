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

    var opts = MochiKit.Base.update({
        name : 'win' + Math.round(Math.random()*100000),
        center: true,
        x: null,
        y: null,
        width: 800, //screen.availWidth - 200,
        height: 600, //screen.availHeight - 200,
        scrollbars: 1,
        fullscreen: false,
        menubar: false,
        locationbar: false,
        resizable: true
    }, options || {});

    //opts.width = opts.width > 0 ? opts.width : 800;
    //opts.height = opts.height > 0 ? opts.height : 600;

    var args = '';

    if (!opts.fullscreen) {
        args += "height=" + opts.height + ",";
    }

    if (!opts.fullscreen) {
        args += "width=" + opts.width + ",";
    }

    if (opts.fullscreen) {
        args += "width=" + screen.availWidth + ",";
        args += "height=" + screen.availHeight + ",";
    }

    if (!opts.center) {
        opts.x = 0;
        opts.y = 0;
        args += "screenx=" + opts.x + ",";
        args += "screeny=" + opts.y + ",";
        args += "left=" + opts.x + ",";
        args += "top=" + opts.y + ",";
    }

    if (opts.center && !opts.fullscreen) {
        opts.y=Math.floor((screen.availHeight-(opts.height || screen.height))/2)-(screen.height-screen.availHeight);
        //opts.y=Math.floor((screen.availHeight-(opts.height || screen.height))/2-(screen.height-screen.availHeight)/2);
        opts.x=Math.floor((screen.availWidth-(opts.width || screen.width))/2)-(screen.width-screen.availWidth);
        args += "screenx=" + opts.x + ",";
        args += "screeny=" + opts.y + ",";
        args += "left=" + opts.x + ",";
        args += "top=" + opts.y + ",";
    }

    if (opts.scrollbars) { args += "scrollbars=1,"; }
    if (opts.menubar) { args += "menubar=1,"; }
    if (opts.locationbar) { args += "location=1,"; }
    if (opts.resizable) { args += "resizable=1,"; }

    log(args);

    var win = window.open(anchor, opts.name, args);
    return false;

}

// vim: sts=4 st=4 et
