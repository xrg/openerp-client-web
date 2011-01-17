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

if (typeof(openobject) == "undefined") {
    openobject = new Object;
}

if (typeof(openobject.workflow) == "undefined") {
    openobject.workflow = new Object;
}

openobject.workflow.ConnectionDecorator = new Class;
openobject.workflow.ConnectionDecorator.prototype = $merge(openobject.workflow.ConnectionDecorator.prototype, draw2d.ArrowConnectionDecorator.prototype);

openobject.workflow.ConnectionDecorator.implement({
	
	initialize : function() {
		draw2d.ArrowConnectionDecorator(this);
		this.setColor(new draw2d.Color(100, 100, 100));
		this.setBackgroundColor(new draw2d.Color(100, 100, 100))
	},
	
	paint : function(/*:draw2d.Graphics*/ g) {
		
		if(this.backgroundColor!=null)
  		{
     		g.setColor(this.backgroundColor);
     		g.fillPolygon([1,6,6,1],[0,3,-3,0]);
  		}

		 // draw the border
		g.setColor(this.color);
		g.setStroke(1);
		g.drawPolygon([1,6,6,1],[0,3,-3,0]);
	}
	
	
});

// vim: ts=4 sts=4 sw=4 si et

