
// requires: mootools & draw2d

if (typeof(openerp) == "undefined") {
    openerp = new Object;
}

if (typeof(openerp.workflow) == "undefined") {
    openerp.workflow = new Object;
}

openerp.workflow.State = new Class;
openerp.workflow.State.prototype = $merge(openerp.workflow.State.prototype, draw2d.Oval.prototype)
openerp.workflow.State.implement({

	initialize : function(id, act_name, flags, flage, action, kind) {
		
		draw2d.Oval.call(this);
		this.setDimension(100, 60);
		this.setDeleteable(false);
		
		if(flags || flage)
			this.setBackgroundColor(new draw2d.Color(155, 155, 155));
		else		
			this.setBackgroundColor(new draw2d.Color(255, 255, 255));	
				
		this.act_id = id || null;
		this.action = action;
		this.kind = kind || '';	
		this.port = null;
		
		var html = this.getHTMLElement();		
		this.signal = MochiKit.Signal.connect(html , 'ondblclick', this, this.ondblClick);	
		
		var span = document.createElement('span');
		span.id = act_name;
		span.style.position = 'absolute';
		span.style.fontSize = '12px';
		span.innerHTML = act_name;
		span.style.top = '20px';
		span.style.left = '20px';
		span.style.zIndex = '1000';
		span.style.textAlign = 'center';
		
		if(!isUndefinedOrNull(act_name)) {
			var n = act_name.length;
			
			if(n>10)
			{
				var width = 100 + Math.round((n-10)/2 * 10);
				this.setDimension(width,60);
			}
		}			
		html.appendChild(span);
	},
	
	initPort : function(){
		
		var workflow = this.getWorkflow();
		var width = this.getWidth();
		var height = this.getHeight();
		
		this.attachPort(workflow, width, height/2);
		this.attachPort(workflow, width/4*3, 0+3);
		this.attachPort(workflow, width/4*3, height-3);	
		this.attachPort(workflow, width/2, 0);
		this.attachPort(workflow, width/2, height);
		this.attachPort(workflow, width/4, 0+3);		
		this.attachPort(workflow, width/4, height-3);				
		this.attachPort(workflow, 0, height/2);
	},
	
	attachPort: function(workflow,left,top)
	{		
		if(workflow!=null) {
	    this.port = new openerp.workflow.Port();		
	    this.port.setWorkflow(this.getWorkflow());
		this.port.setDimension(3,3);
	    this.port.setHideIfConnected(true);
	    this.addPort(this.port,left,top);
	  }
	},
	
	ondblClick : function(event) {
		new InfoBox(this).show(event);
	},
	
	get_act_id : function() {
		return this.act_id;
	},
		
	
	setDimension : function(/*:int*/ w, /*:int*/ h ) {
		
		draw2d.Oval.prototype.setDimension.call(this,w, h);	
		var ports = this.getPorts();
		
		if(this.port!=null)	{
	  		ports.get(0).setPosition(w,h/2);	  		
	  		ports.get(4).setPosition(w/4*3,3);	  		
	  		ports.get(7).setPosition(w/4*3,h-3);	  		
	  		ports.get(3).setPosition(w/2,0);			
	  		ports.get(6).setPosition(w/2,h);		  		
	  		ports.get(2).setPosition(w/4,3);	   		  		
	  		ports.get(5).setPosition(w/4,h-3); 		
	  		ports.get(1).setPosition(0,h/2);
	  	}
	},
	
	edit : function() {
		
		params = {
		'_terp_model' : 'workflow.activity',
		'_terp_wkf_id' : WORKFLOW.id 
		}
		
		if(this.act_id)
			params['_terp_id'] = this.act_id;
			
		var act = getURL('/workflow/state/edit', params);
		openWindow(act);
		
	},
	
	__delete__ : function() {
		MochiKit.Signal.disconnect(this.signal);
	},
	
});