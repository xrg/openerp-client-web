
if (typeof(openerp) == "undefined") {
    openerp = new Object;
}

if (typeof(openerp.workflow) == "undefined") {
    openerp.workflow = new Object;
}

openerp.workflow.ConnDecorator = new Class;
openerp.workflow.ConnDecorator.prototype = $merge(openerp.workflow.ConnDecorator.prototype, draw2d.ArrowConnectionDecorator.prototype);

openerp.workflow.ConnDecorator.implement({
	
	initialize : function() {
		draw2d.ArrowConnectionDecorator(this);
		this.setBackgroundColor(new draw2d.Color(0,0,0))
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