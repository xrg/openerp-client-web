
// requires: mootools & draw2d

if (typeof(openerp) == "undefined") {
    openerp = new Object;
}

if (typeof(openerp.workflow) == "undefined") {
    openerp.workflow = new Object;
}



openerp.workflow.Workflow = new Class;
openerp.workflow.Workflow.prototype = $merge(openerp.workflow.Workflow.prototype, draw2d.Workflow.prototype);

openerp.workflow.Workflow.implement({
	
	initialize : function(canvas) {
		
		draw2d.Workflow.call(this,canvas);
		this.setBackgroundImage(null, false);
		this.getCommandStack().setUndoLimit(0);
		
		this.states = new draw2d.ArrayList();
		this.conn = new draw2d.ArrayList();
		this.id = null;
		
		//this.setToolWindow(toolbar, 30, 30);
		var tbar = new openerp.workflow.Toolbar();
		this.toolPalette = tbar;
		tbar.setWorkflow(this);
		tbar.canDrag = false;
		
		tbar = tbar.getHTMLElement();
		tbar.style.position = 'relative';
		tbar.style.top = '0px';
		tbar.style.left = '0px';
		tbar.style.zIndex = 0;
		
        MochiKit.DOM.appendChildNodes('toolbox', tbar);
		
//		dummy state
		this.state = new openerp.workflow.State();
        this.state.setDimension(100, 60);
		this.state.setBackgroundColor(new draw2d.Color(255, 255, 255));
        this.addFigure(this.state, 100, 20);
		this.state.initPort();
		this.state.initPort();
		var html_state = this.state.getHTMLElement();	
		html_state.style.display = 'none';
		
		var state_ports = this.state.getPorts();
		
		//dummy connector
		this.connector = new openerp.workflow.Connector(999);
		this.connector.setSource(state_ports.get(0));
		this.connector.setTarget(state_ports.get(1));			
		this.addFigure(this.connector);
		var html_conn = this.connector.getHTMLElement();
		html_conn.style.display = 'none';
		
		this.draw_graph(getElement('wkf_id').value);
	},
	
	draw_graph : function(wkf_id) {
		
		this.id = wkf_id;
		self = this;
		
		for(i=0; i<this.conn.getSize(); i++) {
			this.conn.get(i).dispose();
			MochiKit.DOM.removeElement(this.conn.get(i).getHTMLElement());
		}
		
		var figures = this.getFigures();
		var n = figures.getSize();		
		var arr = [];
				
		for(var i=0; i<n; i++) {
						
			var fig = figures.get(i);
			if (fig instanceof openerp.workflow.State) {
				arr.push(fig);
			}
		}
		
		for(var i=0; i<arr.length; i++) {
			this.removeFigure(arr[i]);
		}
		
		this.states.removeAllElements();
		this.conn.removeAllElements();
		
		req = Ajax.JSON.post('/workflow/get_info',{id:wkf_id});
		req.addCallback(function(obj) {	
			
			for(i in obj.list) {
				var node = obj.list[i];
				var s = new openerp.workflow.State(node['id'], node['name'], node['flow_start'], node['flow_stop'], node['action'], node['kind']);	
		        self.addFigure(s, node['y']+100, node['x']);
		        s.initPort();
		        self.states.add(s);
			}
			 
			var n = self.states.getSize();
			
			for(i in obj.conn) {
				
				var conn = obj.conn[i];
				var start = 0;
				var end = 0;
				
				for(j=0; j<n; j++) {
						
					var node = self.states.get(j);
					var id = node.act_id;
					
					if(id==conn['c'][0])
						start = j;							
					else if(id==conn['c'][1])
						end =j;
				}
				self.add_conn(conn['id'], start, end, conn['signal'], conn['condition'], conn['source'], conn['destination']);
			}
			
	    	getElement('loading').style.display = 'none';
		});	
		
	},
	
	add_conn : function(id, start, end, signal, condition, from, to) {
		
		var source = this.states.get(start);
		var destination = this.states.get(end);		
				
		var c = new openerp.workflow.Connector(id, signal, condition, from, to);	
		var n = this.conn.getSize();
		var counter = 0;
		
		//self connection
		if(start==end) {
			c.setSourceAnchor(new draw2d.ConnectionAnchor);
		    c.setTargetAnchor(new draw2d.ConnectionAnchor);
		    c.setRouter(new draw2d.BezierConnectionRouter());		
		}
		
		for(i=0; i<n; i++) {
			var t = this.conn.get(i);
			var s = this.states.indexOf(t.getSource().getParent());
			var e = this.states.indexOf(t.getTarget().getParent());
			
			if(s==start && e==end) {
				c.isOverlaping = true;
				counter++;
//				log('if yes');
			} else if(e==start && s==end) {
				c.isOverlaping = true;
				counter++;
//				log('else yes');
			} 
		}
		
		c.OverlapingSeq = counter;
		
		var spos = source.getBounds();
		var dpos = destination.getBounds();
		
		//fix source an destination ports 
		if(spos.x<dpos.x) {
			c.setTarget(destination.portL);
			
			if((spos.y + spos.h - dpos.y)>50) 
				c.setSource(source.portD);
			else if((dpos.y + dpos.h - spos.y)>50)
				c.setSource(source.portU);
			else
				c.setSource(source.portR);
		}
		else {
			c.setTarget(destination.portR);
			
			if((spos.y + spos.h - dpos.y)>50) 
				c.setSource(source.portD);
			else if((dpos.y + dpos.h - spos.y)>50)
				c.setSource(source.portU);
			else
				c.setSource(source.portL);
		}
		
		self.addFigure(c);
		this.conn.add(c);
	},
	
	create_state : function(id) {
		if(id != 0) {	
				
			var position = this.state.getPosition();	
			self = this;
			
			req = Ajax.JSON.post('/workflow/state/get_info',{id:id});
			req.addCallback(function(obj) {
				var flag = false;
				var index = null;
				var n = self.states.getSize(); 
				var data = obj.data;
				
				for(i=0; i<n; i++) {
					if(self.states.get(i).get_act_id() == id)
					{
						flag=true;
						index = i;
						break;
					}
				}			
				
				if(!flag) {	
					var s = new openerp.workflow.State(data['id'], data['name'], data['flow_start'], data['flow_stop'], data['action'], data['kind']);
			        self.addFigure(s, position.x, position.y);
			        self.states.add(s);
			        s.initPort();
				} else {
					var state = self.states.get(index);
					var span = MochiKit.DOM.getElementsByTagAndClassName('span', null, state.getHTMLElement());
					span[0].innerHTML = data['name'];
					state.action = data['action'];
					state.kind = data['kind'];
//					div.style.width = Math.max(50,(obj.data['name'].length/2*10))+'px'							
					
//					if(obj.data['flow_start'] || obj.data['flow_stop'] )
//					{	
//						state.setBackgroundColor(new draw2d.Color(155, 155, 155));
//						log('if')
//					}
//					else
//					{
//						state.setBackgroundColor(new draw2d.Color(255, 255, 255));
//						log('else');
//					}
				}	
			});
		} else {
			alert('state could not be created');
		}
	},
	
	create_conn : function(act_from, act_to){
		
		var self = this;
		var html = this.connector.getHTMLElement();
		
		req = Ajax.JSON.post('/workflow/connector/auto_create', {act_from:act_from, act_to:act_to});
		req.addCallback(function(obj) {	
			
			html.style.display = 'none';
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
						end =j;
				}				
				self.add_conn(data['id'], start, end, data['signal'], data['condition'], data['act_from'][1], data['act_to'][1]);
				self.conn.getLastElement().edit();
			} else {
				alert('could not create transaction at server');
			}
		});		
	},
	
	
	update_conn : function(id) {	
		var self = this;
		
		req = Ajax.JSON.post('/workflow/connector/get_info',{id:id});
		req.addCallback(function(obj) {
			var n = self.conn.getSize();
			
			for(i=0; i<n; i++) {
				var c = self.conn.get(i);
				if(id==c.get_tr_id()) {
					c.signal = obj.data['signal'];
					c.condition = obj.data['condition'];
					break;		
				}
			}			
		});
	},
	
	remove_elem : function(elem) {

	if(elem instanceof openerp.workflow.State)
		this.unlink_state(elem);
	else if(elem instanceof openerp.workflow.Connector)
		this.unlink_connector(elem);
		
	},
	
	unlink_state : function(state) {
		
		params = {
		'model' : 'workflow.activity',
		'id' : state.get_act_id()		
		}
		
		var self = this;
		
		req = Ajax.JSON.post('/workflow/state/delete',params);
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
		
		var command = new draw2d.CommandDelete(self.getFigure(state.getId()));
		self.getCommandStack().execute(command);
		self.states.remove(state);
	},
	
	
	unlink_connector : function(conn) {
		
		var self = this;
		params = {
		'model' : 'workflow.transition',
		'id' : conn.get_tr_id()		
		}
		
		req = Ajax.JSON.post('/workflow/connector/delete',params);
		req.addCallback(function(obj) {
			
			if(!obj.error) {				
				conn.__delete__();
				self.remove_conn(conn);
			} else
				alert(obj.error);
			
		});
	},
	
	remove_conn : function(conn) {
		conn.dispose();
		this.conn.remove(conn);
	}
});