
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
		this.MaxFanOut = 1;
	},	
	
	onDrop : function(port) {

		WORKFLOW.connector.setSource(this);
		WORKFLOW.connector.setTarget(port);
		
		var source = this.getParent().get_act_id();
		var destination = port.getParent().get_act_id();
		
		if(source && destination) {			
			WORKFLOW.connector.getHTMLElement().style.display = '';
			WORKFLOW.create_conn(source,destination); 
		}
		
	},		
	
	
	getMaxFanOut : function() {
	  return this.MaxFanOut;
	},
	
	getFanOut : function() {
		
	  if(this.getParent().workflow==null)
	    return 0;
	
	  var count =0;
	  var lines = this.getParent().workflow.getLines();
	  var size=lines.getSize();
	  
	  for(var i=0;i< size;i++) {
	    var line = lines.get(i);
	    
	    if(line instanceof draw2d.Connection)
	    {
	      if(line.getSource()==this)
	        count++;
	      else if(line.getTarget()==this)
	        count++;
	    }
	  }
	  return count;
	},		
	
}); 

