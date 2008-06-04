////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://openerp.com) All Rights Reserved.
//
// $Id$
//
// WARNING: This program as such is intended to be used by professional
// programmers who take the whole responsibility of assessing all potential
// consequences resulting from its eventual inadequacies and bugs
// End users who are looking for a ready-to-use solution with commercial
// guarantees and support are strongly advised to contract a Free Software
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
// along with this program; if not, write to the 
// Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
// Boston, MA  02111-1307, USA.
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

// vim: sts=4 st=4 et
