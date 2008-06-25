
if (typeof(openerp) == "undefined") {
    openerp = new Object;
}

if (typeof(openerp.workflow) == "undefined") {
    openerp.workflow = new Object;
}

openerp.workflow.ConnectionAnchor = new Class;
openerp.workflow.ConnectionAnchor.prototype = $merge(openerp.workflow.ConnectionAnchor.prototype, draw2d.ChopboxConnectionAnchor.prototype);

openerp.workflow.ConnectionAnchor.implement({

	initialize : function(owner) {
		draw2d.ChopboxConnectionAnchor.call(this,owner);
		this.conn_id = 0;
		this.factor = 6;
		
	},
	

getLocation : function(/*:draw2d.Point*/ reference)
	{		
		
		var center = this.getReferencePoint();
		var bounds = this.getBox();
		var b2 = (bounds.h/2) * (bounds.h/2);//minor axis of ellipse
		var a2 = (bounds.w/2) * (bounds.w/2);//major axis of ellipse
		
		var ry = reference.y - center.y
		var rx = reference.x - center.x
		if(rx!=0)
			var slope = ry / rx;
		
		var connectors = this.owner.getConnections();
		var n = connectors.getSize();
		for(i=0; i<n; i++)
			if(connectors.get(i).tr_id==this.conn_id)
				var conn = connectors.get(i);
				
		if(conn.isOverlaping) {		
			
			
			//horizontal parallel lines
			if(ry==0) {				
				if(conn.OverlapingSeq%2==0)
					return new draw2d.Point(Math.round(center.x), Math.round(center.y + (10*conn.OverlapingSeq)));
				else
					return new draw2d.Point(Math.round(center.x), Math.round(center.y - (10*conn.OverlapingSeq)));
			}//vertical parallel lines			
			else if(rx==0) {
				if(conn.OverlapingSeq%2==0)
					return new draw2d.Point(Math.round(center.x + (15*conn.OverlapingSeq)), Math.round(center.y));
				else
					return new draw2d.Point(Math.round(center.x - (15*conn.OverlapingSeq)), Math.round(center.y));
			} 
			else {
				
				var m = -1/slope; //slope of perpendicular line  is negative of resiprocal of slope				
				
				//solving equation of ellipse and line which is prependicular to the line passing through two center 
				var x = Math.sqrt((a2*b2)/(b2+(m*m*a2)));
				var y = m*x;	
				var k = 1/(conn.totalOverlaped+1);
				
				var xd = -2*x;
				var yd = -2*y;					
				
				var xnew = x + (k*xd*conn.OverlapingSeq);
				var ynew = y + (k*yd*conn.OverlapingSeq);
				
			}
		}else {
			
			var xnew = 0;
			var ynew = 0;			
		}
		
		//find point on ellipse
		var c = ynew - (slope * xnew);
				
		var A = (b2) + ((a2) * (slope*slope));
		var B = 2 * c * slope * (a2);
		var C = (a2) * ((c*c) - (b2));
		
		var discriminator = Math.sqrt((B*B) - (4 * A *C));
		
		var root1x = (-B + discriminator)/(2*A);
		var root2x = (-B - discriminator)/(2*A);
		
		var root1y = slope*root1x + c;
		var root2y = slope*root2x + c;
						
		
		var dist1 = Math.sqrt(((reference.x-(center.x+root1x))*(reference.x-(center.x+root1x))) + ((reference.y-(center.y+root1y))*(reference.y-(center.y+root1y))));
		var dist2 = Math.sqrt(((reference.x-(center.x+root2x))*(reference.x-(center.x+root2x))) + ((reference.y-(center.y+root2y))*(reference.y-(center.y+root2y))));

		if(dist2>dist1)
			return new draw2d.Point(Math.round(center.x + root1x), Math.round(center.y + root1y));
		else
			return new draw2d.Point(Math.round(center.x + root2x), Math.round(center.y + root2y));

	},
});