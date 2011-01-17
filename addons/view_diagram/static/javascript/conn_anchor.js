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

openobject.workflow.ConnectionAnchor = new Class;
openobject.workflow.ConnectionAnchor.prototype = $merge(openobject.workflow.ConnectionAnchor.prototype, draw2d.ChopboxConnectionAnchor.prototype);

openobject.workflow.ConnectionAnchor.implement({

	initialize : function(owner) {
		draw2d.ChopboxConnectionAnchor.call(this,owner);
		this.conn_id = 0;
		this.factor = 6;
		
	},

    getLocation : function(/*:draw2d.Point*/ reference)	{		
		
        var center = this.getReferencePoint();
		var bounds = this.getBox();
		var b2 = (bounds.h/2) * (bounds.h/2);//minor axis of ellipse
		var a2 = (bounds.w/2) * (bounds.w/2);//major axis of ellipse
		
		var ry = reference.y - center.y;
		var rx = reference.x - center.x;
		if(rx!=0)
			var slope = ry / rx;
		
		var connectors = this.owner.getConnections();
		var n = connectors.getSize();
		
		for(i=0; i<n; i++)
			if(connectors.get(i).tr_id==this.conn_id) {
				var conn = connectors.get(i);
				break;
			}	
			
		//multiple connectors		
		if(conn.isOverlaping) {	
			
			//vertical parallel lines
			if(rx==0) {
				var x = bounds.w / 2;
				var y = 0;		
			}//horizontal parallel lines			
			else if(ry==0) {
				var x = 0;
				var y = bounds.h / 2;
			} 
			else {
				
				var m = -1/slope; //slope of perpendicular line  is negative of resiprocal of slope				
				
				//solving equation of ellipse and line which is prependicular to the line passing through two center 
				var x = Math.sqrt((a2 * b2) / (b2 + (m * m * a2)));
				var y = m * x;		
			}
			
			var xd = -2 * x;
			var yd = -2 * y;	
			var k = 1/(conn.totalOverlaped + 1);
			
			var xnew = x + (k * xd * conn.OverlapingSeq); 
			var ynew = y + (k * yd * conn.OverlapingSeq);
		}
		else {//single connector
			var xnew = 0;
			var ynew = 0;			
		}
		
		
		//find point on ellipse when node is StateOval
		if(this.owner.getParent() instanceof openobject.workflow.StateOval) {
    	   
    		if(rx!=0) {
    			
    			var c = ynew - (slope * xnew);
    					
    			var A = (b2) + ((a2) * (slope*slope));
    			var B = 2 * c * slope * (a2);
    			var C = (a2) * ((c*c) - (b2));
    			
    			var discriminator = Math.sqrt((B*B) - (4 * A *C));
    			
    			var root1x = (-B + discriminator)/(2 * A);
    			var root2x = (-B - discriminator)/(2 * A);
    			
    			//substituting x in y=mx+c
    			var root1y = slope*root1x + c;
    			var root2y = slope*root2x + c;
    		}
    		else {			
    			var root1x = xnew;
    			var root2x = xnew;
    			
    			var root1y = Math.sqrt((b2 * (a2 - (root1x * root1x))) / (a2));
    			var root2y = -root1y;
    		}
    		
    		var dist1 = Math.sqrt(((rx-root1x)*(rx-root1x)) + ((ry-root1y)*(ry-root1y)));
    		var dist2 = Math.sqrt(((rx-root2x)*(rx-root2x)) + ((ry-root2y)*(ry-root2y)));
    
    		if(dist2>dist1)
    			return new draw2d.Point(Math.round(center.x + root1x), Math.round(center.y + root1y));
    		else
    			return new draw2d.Point(Math.round(center.x + root2x), Math.round(center.y + root2y));
		}
		else {//find point on rectangle when node is StateRectangle

            xnew += center.x;
            ynew += center.y;
		    
		    if(conn.isOverlaping) {//multiple connectors
		        
		        var bottom = bounds.y + bounds.h;//bottom line of the rectangle perimeter		        
		        var right = bounds.x + bounds.w;//right line of the rectangle perimeter
		        
		        var xtop = (bounds.y - ynew + (slope*xnew))/slope;
		        var xbase = (bottom - ynew + (slope*xnew))/slope;
		        var yleft = slope*(bounds.x - xnew) + ynew; 
                var yright = slope*(right - xnew) + ynew;
                
                //to check that points lies on rectangle perimeter
		        if(bounds.x > xtop  || xtop > right)
                    xtop = 0;
                    
                if(bounds.x > xbase  || xbase > right)
                    xbase = 0;
		        
		        if(bounds.y > yleft || yleft > bottom)
                    yleft = 0;
                    		          
		        if(bounds.y > yright || yright > bottom)
                    yright = 0;
                
                
                if(xtop != 0 && xbase != 0) {
                    var d1 = Math.abs(reference.y - bounds.y);
                    var d2 = Math.abs(reference.y - bottom);
                    
                    if(d1 > d2) 
                        return new draw2d.Point(Math.round(xbase), Math.round(bottom));
                    else
                        return new draw2d.Point(Math.round(xtop), Math.round(bounds.y));
                }                    
                else if(yleft != 0 && yright != 0) {
                    var d1 = Math.abs(reference.x - bounds.x);
                    var d2 = Math.abs(reference.x - right);
                    
                    if(d1 > d2) 
                        return new draw2d.Point(Math.round(right), Math.round(yright));
                    else
                        return new draw2d.Point(Math.round(bounds.x), Math.round(yleft));
                }
		        else {
		            if(xtop != 0) { 
                        var root1x = xtop;
                        var root1y = bounds.y;
		            }
                    else {
                        var root1x = xbase;
                        var root1y = bottom;
                    }    
                    
                    if(yleft != 0) { 	              
                        var root2y = yleft;
                        var root2x = bounds.x;
                    }
                    else {
                        var root2y = yright;
                        var root2x = right;
                    }    
                    
                    var dist1 = Math.sqrt(((reference.x-root1x)*(reference.x-root1x)) + ((reference.y-root1y)*(reference.y-root1y)));
                    var dist2 = Math.sqrt(((reference.x-root2x)*(reference.x-root2x)) + ((reference.y-root2y)*(reference.y-root2y)));
            
                    if(dist2>dist1)
                        return new draw2d.Point(Math.round(root1x), Math.round(root1y));
                    else
                        return new draw2d.Point(Math.round(root2x), Math.round(root2y));
		        }
		        
		    } else {//single connector
                var dx = reference.x - center.x;
                var dy = reference.y - center.y;    		    
    		    
    		    var scale = 0.5 / Math.max(Math.abs(dx) / bounds.w, Math.abs(dy) / bounds.h);
    
                dx *= scale;
                dy *= scale;
                xnew += dx;
                ynew += dy;
                
                return new draw2d.Point(Math.round(xnew), Math.round(ynew));
		    }
		}
	}
	
});

// vim: ts=4 sts=4 sw=4 si et
