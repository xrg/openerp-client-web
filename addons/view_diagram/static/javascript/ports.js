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

// requires: mootools & draw2d

if (typeof(openobject) == "undefined") {
    openobject = new Object;
}

if (typeof(openobject.workflow) == "undefined") {
    openobject.workflow = new Object;
}


openobject.workflow.Port = new Class;
openobject.workflow.Port.prototype = $merge(openobject.workflow.Port.prototype, draw2d.Port.prototype);

openobject.workflow.Port.implement({
	
	initialize : function() {
        
	    draw2d.Port.call(this);     
		this.setDimension(2,2);
		var html = this.getHTMLElement();
		html.style.backgroundColor = '#990200';
		html.style.zIndex = '1000';

        if(jQuery('#_terp_editable').val() == 'False')
            this.setCanDrag(false);
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


