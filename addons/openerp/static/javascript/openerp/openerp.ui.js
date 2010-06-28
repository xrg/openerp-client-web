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

if (typeof(openobject.dom) == "undefined") {
    throw "openobject.dom is required by 'openerp.ui'.";
}

if (typeof(openerp) == "undefined") {
    openerp = {};
}

openerp.ui = {};

function toggle_sidebar(forced) {
    function a() {
        var sb = openobject.dom.get('sidebar');

        sb.style.display = forced ? forced : (sb.style.display == "none" ? "" : "none");
        openobject.http.setCookie("terp_sidebar", sb.style.display);

        var a_img = openobject.dom.get('toggle-click');
        var tertiary = openobject.dom.get('tertiary');
        var tertiary_wrap = openobject.dom.get('tertiary_wrap');
        var sidebar_hide = openobject.dom.get('sidebar_hide');
        var attach_sidebar = openobject.dom.get('attach_sidebar');
        var add_attachment = openobject.dom.get('add_attachment');
        var customise_menu = openobject.dom.get('customise_menu');
        if (sb.style.display == "none") {
            setNodeAttribute(a_img, 'class', 'off');
            setNodeAttribute(tertiary, 'style', 'width: 21px');
            setNodeAttribute(tertiary_wrap, 'style', 'padding: 0 0 0 0');
            setNodeAttribute(sidebar_hide, 'style', 'padding: 0 0 0 0');
            setNodeAttribute(attach_sidebar, 'style', 'display: none');
            setNodeAttribute(add_attachment, 'style', 'display: none');
            setNodeAttribute(customise_menu, 'style', 'display: none');
        } else {
            setNodeAttribute(a_img, 'class', 'on');
            setNodeAttribute(tertiary, 'style', 'width: 180px');
            setNodeAttribute(tertiary_wrap, 'style', 'padding: 0 0 0 10px');
            setNodeAttribute(sidebar_hide, 'style', 'padding: 0 0 0 8px');
            setNodeAttribute(attach_sidebar, 'style', "display: ''");
            setNodeAttribute(add_attachment, 'style', "display: ''");
            setNodeAttribute(customise_menu, 'style', "display: ''");
        }
    }
    if (typeof(Notebook) == "undefined") {
        a();
    } else {
        Notebook.adjustSize(a);
    }

    MochiKit.Signal.signal(document, 'toggle_sidebar');
}
