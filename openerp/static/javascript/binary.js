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
    var fname = $(filename) || $(name + 'name');
    var act = '/form/save_binary_data';
    
    act = fname ? act + '/' + fname.value : act;
    act = act + '?_terp_field=' + name;
    
    submit_form(act);
}

var add_binary = function(src) {
    binary_add = $(src + '_binary_add');
    binary_buttons = $(src + '_binary_buttons');
        
    binary_add.style.display = "";
    binary_buttons.style.display = "none";
    
    fld = MochiKit.DOM.getElement(src);
    fld.disabled = false;
    
    connect(src, 'onkeydown', function(e){
        if (e.key().string == 'KEY_ESCAPE') {
            binary_add.style.display = "none";
            binary_buttons.style.display = "";
            
            fld.disabled = true;
        } 
    });
}

function set_binary_filename(id, fname){
    if ($(id)) {
        $(id).value = fname.value;
    }
}


