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

var Menu = function(id, submenu){
    this.menu = $(id);
    this.layer = $(submenu);

    this.visible = false;

    if (this.menu){
        connect(this.menu, "onmouseover", bind(this.show, this));
        connect(this.menu, "onmouseout", bind(this.hide, this));
        connect(this.layer, "onmouseover", bind(this.show, this));
        connect(this.layer, "onmouseout", bind(this.hide, this));
    }
}

Menu.prototype.show = function(){
    if (!this.visible) {
        this.layer.style.visibility="visible";
        this.visible = true;
    }
}

Menu.prototype.hide = function(){
    if (this.visible) {
        this.layer.style.visibility="hidden";
        this.visible = false;
    }
}

// vim: ts=4 sts=4 sw=4 si et

