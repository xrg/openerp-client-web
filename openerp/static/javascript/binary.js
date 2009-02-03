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

var save_binary_data = function(src, filename) {
    
    var name = $(src) ? $(src).name : src;
    var prefix = name.split(); prefix.pop(); 
    var prefix = prefix.join('/'); prefix ? prefix + '/' : '';

    var fname = $(filename) || $(prefix + 'name');

    fname = fname ? fname.value || fname.innerHTML : null;

    var act = get_form_action('save_binary_data');
    act = fname ? act + '/' + fname : act;

    submit_form(getURL(act, {_terp_field: name}));
}

var add_binary = function(src) {

    binary_add = $(src + '_binary_add');
    binary_buttons = $(src + '_binary_buttons');
        
    binary_add.style.display = "";
    binary_buttons.style.display = "none";
    
    fld = MochiKit.DOM.getElement(src);
    fld.disabled = false;

    // Firefox problem (bug: 324408)
    if (browser.isGecko) {
        fld.size = 50;
    }
}

var set_binary_filename = function(id, fname){

    var target = getElement(id);
    fname = getElement(fname);

    if (fname && target) {
        target.value = fname.value;
    }
}

// vim: ts=4 sts=4 sw=4 si et

