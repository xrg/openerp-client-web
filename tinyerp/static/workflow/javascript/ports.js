
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


