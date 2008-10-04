////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
//
// $Id$
//
// Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
//
// WARNING: This program as such is intended to be used by professional
// programmers who take the whole responsibility of assessing all potential
// consequences resulting from its eventual inadequacies and bugs
// End users who are looking for a ready-to-use solution with commercial
// guarantees and support are strongly advised to contract a Free Software
// Service Company
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
////////////////////////////////////////////////////////////////////////////////

// requires: mootools & draw2d

if (typeof(openerp) == "undefined") {
    openerp = new Object;
}

if (typeof(openerp.workflow) == "undefined") {
    openerp.workflow = new Object;
}


openerp.workflow.Port = new Class;
openerp.workflow.Port.prototype = $merge(openerp.workflow.Port.prototype, draw2d.Port.prototype);

openerp.workflow.Port.implement({
	
	initialize : function() {
	    
//        draw2d.Port.call(this, new draw2d.ImageFigure('/static/workflow/images/port.gif'));
        
	    draw2d.Port.call(this);     
		this.setDimension(2,2);
		var html = this.getHTMLElement();
		html.style.backgroundColor = '#990200';
		html.style.zIndex = '1000';
		
	},	
	
	onDrop : function(port) {
		
		var source = this.getParent().get_act_id();
		var destination = port.getParent().get_act_id();
		
		if(source && destination) {	
			WORKFLOW.create_connection(source,destination); 
		}
	}
	
});

// vim: ts=4 sts=4 sw=4 si et


