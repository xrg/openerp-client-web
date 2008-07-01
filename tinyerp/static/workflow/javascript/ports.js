
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
		draw2d.Port.call(this, new draw2d.ImageFigure('/static/workflow/images/port.gif'));
		this.setDimension(1,1)
//		draw2d.Port.call(this);
		var html = this.getHTMLElement();
		html.style.zIndex = '1000';
//		html.style.backgroundColor = 'red';
		
	},	
	
	onDrop : function(port) {

//		WORKFLOW.connector.setSource(this);
//		WORKFLOW.connector.setTarget(port);
		
		var source = this.getParent().get_act_id();
		var destination = port.getParent().get_act_id();
		
		
		
		if(source && destination) {			
//			WORKFLOW.connector.getHTMLElement().style.display = '';
			WORKFLOW.create_conn(source,destination); 
		}
	},		
	
}); 

