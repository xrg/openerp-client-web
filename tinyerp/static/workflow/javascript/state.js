
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
	
	initialize : function(params) {
        
        draw2d.Oval.call(this);
        this.setDimension(100, 60);
        this.setDeleteable(false);
        
        if(params.flow_start || params.flow_stop)
            this.setBackgroundColor(new draw2d.Color(155, 155, 155));
        else        
            this.setBackgroundColor(new draw2d.Color(255, 255, 255));   
                
        this.act_id = params.id || null;
        this.action = params.action;
        this.kind = params.kind || ''; 
        this.portR = null;
        this.portU = null;
        this.portL = null;
        this.portD = null;
        
        var html = this.getHTMLElement();       
        this.signal = MochiKit.Signal.connect(html , 'ondblclick', this, this.ondblClick);  
        
        var span = document.createElement('span');
        span.id = params.name;
        span.style.position = 'absolute';
        span.style.fontSize = '12px';
        span.innerHTML = params.name;
        span.style.top = '20px';
        span.style.left = '20px';
        span.style.zIndex = '1000';
        span.style.textAlign = 'center';
        
        if(!isUndefinedOrNull(params.name)) {
            var n = params.name.length;
            
            if(n>10)
            {
                var width = 100 + Math.round((n-10)/2 * 10);
                this.setDimension(width,60);
            }
        }           
        html.appendChild(span);
    },
	
	initPort : function() {
		
		var workflow = this.getWorkflow();
		var width = this.getWidth();
		var height = this.getHeight();
		
		this.portR = new openerp.workflow.Port();		
	    this.portR.setWorkflow(workflow);
	    this.addPort(this.portR, width, height/2);
	    
	    this.portU = new openerp.workflow.Port();		
	    this.portU.setWorkflow(workflow);
	    this.addPort(this.portU, width/2, 0);
	    
	    this.portL = new openerp.workflow.Port();		
	    this.portL.setWorkflow(workflow);
	    this.addPort(this.portL, 0, height/2);
	    
	    this.portD = new openerp.workflow.Port();		
	    this.portD.setWorkflow(workflow);
	    this.addPort(this.portD, width/2, height);
	},
	
	ondblClick : function(event) {
		new InfoBox(this).show(event);
	},
	
	get_act_id : function() {
		return this.act_id;
	},
		
	
	setDimension : function(/*:int*/ w, /*:int*/ h ) {
		
		draw2d.Oval.prototype.setDimension.call(this, w, h);	
	
		if(this.portR!=null)	{
			this.portR.setPosition(w, h/2);
			this.portU.setPosition(w/2, 0);
			this.portL.setPosition(0, h/2);
			this.portD.setPosition(w/2, h);
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