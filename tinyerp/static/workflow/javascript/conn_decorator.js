
if (typeof(openerp) == "undefined") {
    openerp = new Object;
}

if (typeof(openerp.workflow) == "undefined") {
    openerp.workflow = new Object;
}

openerp.workflow.ConnectionDecorator = new Class;
openerp.workflow.ConnectionDecorator.prototype = $merge(openerp.workflow.ConnectionDecorator.prototype, draw2d.ArrowConnectionDecorator.prototype);

openerp.workflow.ConnectionDecorator.implement({
	
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

