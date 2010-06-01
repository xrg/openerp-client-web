////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
//
// $Id$
//
// Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
//
// The OpenERP web client is distributed under the "OpenERP Public License".
// It's based on Mozilla Public License Version (MPL) 1.1 with following 
// restrictions:
//
// -   All names, links and logos of Tiny, Open ERP and Axelor must be 
//     kept as in original distribution without any changes in all software 
//     screens, especially in start-up page and the software header, even if 
//     the application source code has been changed or updated or code has been 
//     added.
//
// -   All distributions of the software must keep source code with OEPL.
// 
// -   All integrations to any other software must keep source code with OEPL.
//
// If you need commercial licence to remove this kind of restriction please
// contact us.
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



openobject.workflow.Workflow = new Class;
openobject.workflow.Workflow.prototype = $merge(openobject.workflow.Workflow.prototype, draw2d.Workflow.prototype);

openobject.workflow.Workflow.implement({
	
	initialize : function(canvas) {
		
		draw2d.Workflow.call(this, canvas);
		this.getCommandStack().setUndoLimit(0);
        this.setEnableSmoothFigureHandling(true);

        // enable grid by default
        this.setBackgroundImage(openobject.http.getURL('/images/grid_10.jpg'), true);
        this.setGridWidth(10, 10);
        this.setSnapToGrid(true);
		
		this.id = null;
		this.workitems = [];
		this.node_obj = openobject.dom.get('node').value;
		this.connector_obj = openobject.dom.get('connector').value;
		this.src_node_nm = openobject.dom.get('src_node').value;
		this.des_node_nm = openobject.dom.get('des_node').value;
		
		this.states = new draw2d.ArrayList();
		this.connectors = new draw2d.ArrayList();		
		this.selected = null;
		
		if ($('_terp_editable').value=='True') {
			var tbar = new openobject.workflow.Toolbar();
			this.toolPalette = tbar;
			tbar.setWorkflow(this);
			tbar.canDrag = false;
			
			tbar = tbar.getHTMLElement();
			tbar.style.position = 'relative';
			tbar.style.top = '0px';
			tbar.style.left = '0px';
			tbar.style.zIndex = 0;
			
	        MochiKit.DOM.appendChildNodes('toolbox', tbar);
		}else {
            this.workitems = eval($('workitems').value);
            removeElement('toolbox');
		}
		
//		dummy state
		this.state = new openobject.workflow.StateOval({}, []);
        this.state.setDimension(100, 60);
		this.state.setBackgroundColor(new draw2d.Color(255, 255, 255));
		this.state.getHTMLElement().style.display = 'none';
        this.addFigure(this.state, 100, 20);
		this.state.initPort();
		this.state.initPort();
		
		this.node_flds_v = getElement('node_flds_visible').value;          
        this.node_flds_h = getElement('node_flds_invisible').value;
        this.conn_flds = getElement('conn_flds').value;
        this.bgcolors = getElement('bgcolors').value;
        this.shapes = getElement('shapes').value;	
        
        if (!getElement('workitems') || this.workitems.length>0)        			
            this.draw_graph(openobject.dom.get('wkf_id').value);
        else {            
            openobject.dom.get('loading').style.display = 'none';
        }   	    
	},
	
    draw_graph : function(wkf_id) {
		
		this.id = wkf_id;
		var self = this;
		
		req = openobject.http.postJSON('/view_diagram/workflow/get_info',{id:wkf_id, model:$('_terp_model').value,
		                                                      node_obj: self.node_obj, conn_obj:self.connector_obj,
		                                                      src_node: self.src_node_nm, des_node:self.des_node_nm,
		                                                      node_flds_v: this.node_flds_v, node_flds_h: this.node_flds_h, conn_flds: this.conn_flds,
		                                                      bgcolors: this.bgcolors, shapes: this.shapes});
		req.addCallback(function(obj) {	
			
			for(i in obj.nodes) {
                var node = obj.nodes[i];

                if(node['shape']=='ellipse')
                    var state = new openobject.workflow.StateOval(node, self.workitems);
		        else if(node['shape']=='rectangle')
                    var state = new openobject.workflow.StateRectangle(node, self.workitems);
		          
                self.addFigure(state, node['x'], node['y']);
                state.initPort();
                self.states.add(state);
			}
			
			//check for overlapping connections
			for(i in obj.conn) {
				var counter = 1;
				var check_for = obj.conn[i];
				check_for['isOverlaping'] = false;
				
				for(k in obj.conn) {
					if(i!=k) {
						check_to = obj.conn[k];
						
						if(check_for['s_id']==check_to['s_id'] && check_for['d_id']==check_to['d_id']) {
							check_for['isOverlaping'] = true;
							counter++;
						}
						else if(check_for['d_id']==check_to['s_id'] && check_for['s_id']==check_to['d_id']) {
							check_for['isOverlaping'] = true;
							counter++;
						}						
					}
					else {
						check_for['OverlapingSeq'] = counter;
					}
				}
                check_for['totalOverlaped'] = counter;
			}			
			 
			var n = self.states.getSize();
			
			for(i in obj.conn) {				
				var conn = obj.conn[i];
				var start = 0;
				var end = 0;
				
				for(j=0; j<n; j++) {
						
					var node = self.states.get(j);
					var id = node.act_id;
					
					if(id==conn['s_id'])
						start = j;							
					else if(id==conn['d_id'])
						end =j;
				}
                self.add_connection(start, end, conn)
			}
			
	    	openobject.dom.get('loading').style.display = 'none';
		});		
	},
	
	get_overlaping_connection : function(s, e, flag) {
		
		var n = this.connectors.getSize();
		var conn_overlapped = new Array();
		var counter = 1;
		
		for(i=0; i<n; i++) {
			var conn = this.connectors.get(i)
			var start = conn.getSource().getParent().get_act_id();
			var end = conn.getTarget().getParent().get_act_id();
			
			if((start==s && end==e)) {
				conn.isOverlaping = true;
				conn.OverlapingSeq = counter ++;
				conn_overlapped.push(i);
			}else if(end==s && start==e) {
				conn.isOverlaping = true;
				conn.OverlapingSeq = counter ++;
				conn_overlapped.push(i);	
			}
		}
		
		for(i=0; i<conn_overlapped.length; i++) {
			var conn = this.connectors.get(conn_overlapped[i]) 
			
			if(flag) {
				conn.totalOverlaped = counter;
			} else {
				conn.totalOverlaped = counter - 1;
				if(counter-1==1)
					conn.isOverlaping = false;
			}
		}
		
		return counter;
	},	
	
	add_connection : function(start, end, params) {
        
        var source = this.states.get(start);
        var destination = this.states.get(end);
 
        var conn = new openobject.workflow.Connector(params.id, params.source, params.destination, params.options);
        var n = this.connectors.getSize();
        
        //self connection
        if(start==end) {
            conn.setSourceAnchor(new draw2d.ConnectionAnchor);
            conn.setTargetAnchor(new draw2d.ConnectionAnchor);
            conn.setRouter(new draw2d.BezierConnectionRouter());        
        }
        
        conn.isOverlaping = params.isOverlaping;       
        conn.OverlapingSeq = params.OverlapingSeq;
        conn.totalOverlaped = params.totalOverlaped;
        
        var spos = source.getBounds();
        var dpos = destination.getBounds();
    
        //fix source and destination ports 
        if(spos.x<dpos.x) {
            conn.setTarget(destination.portL);
            
            if((spos.y + spos.h - dpos.y)>50) 
                conn.setSource(source.portD);
            else if((dpos.y + dpos.h - spos.y)>50)
                conn.setSource(source.portU);
            else 
                conn.setSource(source.portR);
        }
        else {
            conn.setTarget(destination.portR);
            
            if((spos.y + spos.h - dpos.y)>50) 
                conn.setSource(source.portD);
            else if((dpos.y + dpos.h - spos.y)>50)
                conn.setSource(source.portU);
            else
                conn.setSource(source.portL);
        }
        
        this.addFigure(conn);
        this.connectors.add(conn);
    },
	
	create_state : function(id) {
	    
		if(id != 0) {	
			var position = this.state.getPosition();
			this.state.setPosition(100, 20);	
			var self = this;
			
			req = openobject.http.postJSON('/view_diagram/workflow/state/get_info',{node_obj: self.node_obj, id: id, 
			                                                         node_flds_v: this.node_flds_v, 
			                                                         node_flds_h: this.node_flds_h,
			                                                         bgcolors: this.bgcolors, 
			                                                         shapes: this.shapes});
			req.addCallback(function(obj) {
				var flag = false;
				var index = null;
				var n = self.states.getSize(); 
				var data = obj.data;
				
				for(i=0; i<n; i++) {
					if(self.states.get(i).get_act_id() == id) {
						flag=true;
						index = i;
						break;
					}
				}			
			
				if(!flag) {
			        if(!data['subflow_id'])
			             var state = new openobject.workflow.StateOval(data, self.workitems);
			        else
			             var state = new openobject.workflow.StateRectangle(data, self.workitems);
			             
			        self.addFigure(state, position.x, position.y);
			        self.states.add(state);
			        state.initPort();
				}else {				    
					var state = self.states.get(index);
					var span = openobject.dom.get(state.name);
					span.innerHTML = data['name'];
					span.id = data['name'];
					
					MochiKit.Base.update(state.options, data['options'])
				}	
			});
		} else {
			alert('state could not be created');
		}
	},
	
	create_connection : function(act_from, act_to) {
		
		var self = this;
		req = openobject.http.postJSON('/view_diagram/workflow/connector/auto_create', {conn_obj: self.connector_obj, 
		                                                                  src: self.src_node_nm, 
		                                                                  des: self.des_node_nm, 
		                                                                  act_from: act_from, 
		                                                                  act_to: act_to,
		                                                                  conn_flds: this.conn_flds});
		req.addCallback(function(obj) {
			var data = obj.data;
			
			if(obj.flag) {
				var n = self.states.getSize();
				var start = 0;
				var end = 0;
				
				for(j=0; j<n; j++) {	
					var node = self.states.get(j);
					var id = node.get_act_id();
					if(id==act_from)
						start = j;							
					if(id==act_to)
						end = j;
				}
				
				var counter = self.get_overlaping_connection(data['s_id'], data['d_id'], 1)
				var params = MochiKit.Base.update({}, obj.data);
				
				if(counter>1) {
					params['isOverlaping'] = true;
					params['OverlapingSeq'] = counter;
					params['totalOverlaped'] = counter;
				}		
				
				self.add_connection(start, end, params);
			} else {
				alert('Could not create transaction at server');
			}
		});		
	},
	
	update_connection : function(id) {	
		
		var self = this;
		req = openobject.http.postJSON('/view_diagram/workflow/connector/get_info',{conn_obj: self.connector_obj, id: id});
		req.addCallback(function(obj) {
			var n = self.connectors.getSize();
			
			for(i=0; i<n; i++) {
				var conn = self.connectors.get(i);
				if(id==conn.get_tr_id()) {
					conn.signal = obj.data['signal'];
					conn.condition = obj.data['condition'];
					break;		
				}
			}			
		});
	},
	
	remove_elem : function(elem) {	
        if(elem instanceof openobject.workflow.StateOval || elem instanceof openobject.workflow.StateRectangle)
            this.unlink_state(elem);
        else if(elem instanceof openobject.workflow.Connector)
            this.unlink_connector(elem);
	},
	
	unlink_state : function(state) {
		
		var self = this;
		req = openobject.http.postJSON('/view_diagram/workflow/state/delete', {node_obj: self.node_obj, 'id': state.get_act_id()});
		req.addCallback(function(obj) {
			if(!obj.error) {
				state.__delete__();
				self.remove_state(state);
			} else {
				alert(obj.error);
			}			
		});
	},
	
	remove_state : function(state) {     
        
        var fig = this.getFigure(state.getId());
        var connections = null
                
        if(fig.getPorts && connections==null) {
            connections = new draw2d.ArrayList();
            var ports = fig.getPorts();
            for(var i=0; i<ports.getSize(); i++) {
                if(ports.get(i).getConnections) {                
                    connections.addAll(ports.get(i).getConnections());
            }
          }
        }
    
        if(connections == null)
            connections = new draw2d.ArrayList();
      
        for (var i = 0; i < connections.getSize(); ++i) {
            this.removeFigure(connections.get(i));
        }
   
        this.removeFigure(fig);
        this.setCurrentSelection(null); 
        if(fig.parent!=null)
            fig.parent.removeChild(fig);
        this.states.remove(state);
	},
	
	unlink_connector : function(conn) {
		
		var self = this;
		req = openobject.http.postJSON('/view_diagram/workflow/connector/delete', {conn_obj: self.connector_obj, 'id': conn.get_tr_id()});
		req.addCallback(function(obj) {
			if(!obj.error) {				
				conn.__delete__();
				self.remove_conn(conn);
			} else
				alert(obj.error);
		});
	},
	
	remove_conn : function(conn) {
		
		var start = conn.getSource().getParent().get_act_id();
		var end = conn.getTarget().getParent().get_act_id();
		
		this.connectors.remove(conn);		
		if(conn.isOverlaping)	
			this.get_overlaping_connection(start, end, 0);
			
		this.removeFigure(conn);
	},
	
	onMouseDown : function(x, y) {
        
        if (this.currentSelection instanceof draw2d.Connection)
            this.selected = this.currentSelection;
        else
            this.selected = null;	 
                
	    draw2d.Workflow.prototype.onMouseDown.call(this, x, y);
	}
});

// vim: ts=4 sts=4 sw=4 si et
