
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
		
	},
	
	
	getLocation : function(/*:draw2d.Point*/ reference)
	{
		var r = new draw2d.Dimension();
   		r.setBounds(this.getBox());
   		r.translate(-1, -1);
   		r.resize(1, 1);
		
		var centerX = r.x + r.w/2;
		var centerY = r.y + r.h/2;
		
		
		var connectors = this.owner.getConnections();
		var n = connectors.getSize();
		for(i=0; i<n; i++)
			if(connectors.get(i).tr_id==this.conn_id)
				var conn = connectors.get(i);
				
		if(conn.isOverlaping) {
			var center = this.getReferencePoint();
			
			//horizontal parallel lines
			if(reference.y-center.y==0) {				
				if(conn.OverlapingSeq%2==0)
					return new draw2d.Point(Math.round(center.x), Math.round(center.y + (10*conn.OverlapingSeq)));
				else
					return new draw2d.Point(Math.round(center.x), Math.round(center.y - (10*conn.OverlapingSeq)));
			}
			else if(reference.x-center.x==0) {//vertical parallel lines
				if(conn.OverlapingSeq%2==0)
					return new draw2d.Point(Math.round(center.x + (15*conn.OverlapingSeq)), Math.round(center.y));
				else
					return new draw2d.Point(Math.round(center.x - (15*conn.OverlapingSeq)), Math.round(center.y));
			} 
			else {
				var slope = (reference.y - center.y)/(reference.x - center.x);
				var m = -1/slope; //slope of perpendicular line  is negative of resiprocal of slope
				var bounds = this.getBox();			
				var h2 = bounds.h*bounds.h;
				var w2 = bounds.w*bounds.w;
				
				var x = Math.sqrt((w2*h2)/(h2+(m*m*w2)));
				var y = m*x;			
				var factor = 2*conn.totalOverlaped;
				
				if(conn.OverlapingSeq%2==0) {
					var xnew = center.x + x/factor;
					var ynew = center.y + y/factor;
//					return new draw2d.Point(Math.round(center.x + x/factor), Math.round(center.y + y/factor))
				}
				else {
					var xnew = center.x - x/factor;
					var ynew = center.y - y/factor;
//					return new draw2d.Point(Math.round(center.x - x/factor), Math.round(center.y - y/factor))
				}
				var denominator = Math.sqrt(((bounds.h*xnew) * (bounds.h*xnew)) + ((bounds.w*ynew) * (bounds.w*ynew)))
				var pointx = (bounds.w * bounds.h * xnew)/denominator + center.x;
				var pointy = (bounds.w * bounds.h * ynew)/denominator + center.y;
				var distance = Math.sqrt(((pointx-xnew) * (pointx-xnew)) + ((pointy-ynew) * (pointy-ynew)))
//				log(',spointx:'+pointx+',pointy:'+pointy+',distance:'+distance);
//				return new draw2d.Point(Math.round(center.x+pointx), Math.round(center.y+pointy))
				return new draw2d.Point(Math.round(xnew), Math.round(ynew));
			}
		}
		
		if (r.isEmpty() || (reference.x == centerX && reference.y == centerY))
			return new /*NAMESPACE*/Point(centerX, centerY);  //This avoids divide-by-zero
		
		var dx = reference.x - centerX;
		var dy = reference.y - centerY;
		
		
		//r.width, r.height, dx, and dy are guaranteed to be non-zero. 
		var scale = 0.5 / Math.max(Math.abs(dx) / r.w, Math.abs(dy) / r.h);
		
		dx *= scale;
		dy *= scale;
		
		centerX += dx;
		centerY += dy;		
		
		return new draw2d.Point(Math.round(centerX), Math.round(centerY));
	},
	

	
//	find_angle : function(c) {
//		var center1 = c.sourceAnchor.getReferencePoint();
//		var center2 = c.targetAnchor.getReferencePoint();
//		
//		var a = null;
//		if(center2.x-center1.x>0) {
//			a = 180/3.14 * Math.atan((center2.y-center1.y)/(center2.x-center1.x));
//		} else if((center2.x - center1.x)<0) {
//			if((center2.y - center1.y)>=0)
//				a = 180 + (180/3.14 *  Math.atan((center2.y-center1.y)/(center2.x-center1.x)));
//			else
//				a = -180 + (180/3.14 * Math.atan((center2.y-center1.y)/(center2.x-center1.x)));
//		} else {
//			if((center2.y - center1.y)>0)
//				a = 90;
//			else if((center2.y - center1.y)<0)
//				a = -90;	
//		}		
//		return a;	
//	}

});