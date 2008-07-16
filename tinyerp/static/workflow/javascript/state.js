
// requires: mootools & draw2d

if (typeof(openerp) == "undefined") {
    openerp = new Object;
}

if (typeof(openerp.workflow) == "undefined") {
    openerp.workflow = new Object;
}


openerp.workflow.StateBase = function(id, action, kind) {
    this.__init__(id, action, kind);
} 
    
openerp.workflow.StateBase.prototype = {
    __init__ : function(id, action, kind) {
    
        this.act_id = id || null;
        this.action = action;
        this.kind = kind || ''; 
        this.portR = null;
        this.portU = null;
        this.portL = null;
        this.portD = null;
    },
    
    init_label : function(flow_start, flow_stop, sname) {
    
        this.setDimension(100, 60);
        this.setDeleteable(false);
        
        if(flow_start || flow_stop)
            this.setBackgroundColor(new draw2d.Color(155, 155, 155));
        else        
            this.setBackgroundColor(new draw2d.Color(255, 255, 255));   
        
        var html = this.getHTMLElement();       
        this.signal = MochiKit.Signal.connect(html , 'ondblclick', this, this.ondblClick);  
        
        var span = document.createElement('span');
        span.id = sname;
        span.style.position = 'absolute';
        span.style.fontSize = '12px';
        span.innerHTML = sname;
        span.style.top = '20px';
        span.style.left = '20px';
        span.style.zIndex = '1000';
        span.style.textAlign = 'center';
        
        if(!isUndefinedOrNull(sname)) {
            var n = sname.length;
            
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
    
    setDimension : function(/*:int*/ w, /*:int*/ h ) {
        
        draw2d.Oval.prototype.setDimension.call(this, w, h);    
        
        if(this.portR!=null)    {
            this.portR.setPosition(w, h/2);
            this.portU.setPosition(w/2, 0);
            this.portL.setPosition(0, h/2);
            this.portD.setPosition(w/2, h);
        }
    },
    
    ondblClick : function(event) {
        new InfoBox(this).show(event);
    },
    
    get_act_id : function() {
        return this.act_id;
    },
    
    __delete__ : function() {
        MochiKit.Signal.disconnect(this.signal);
    }
}

//Oval shape node

openerp.workflow.StateOval = new Class;
openerp.workflow.StateOval.prototype = $merge(openerp.workflow.StateOval.prototype, openerp.workflow.StateBase.prototype, draw2d.Oval.prototype)
openerp.workflow.StateOval.implement({
    
    initialize : function(params) {
        
        openerp.workflow.StateBase.call(this, params.id, params.action, params.kind);
        draw2d.Oval.call(this); 
        
        this.init_label(params.flow_start, params.flow_stop, params.name)
    },
});

//Rectangle shape node when it is a sub-workflow

openerp.workflow.StateRectangle = new Class;
openerp.workflow.StateRectangle.prototype = $merge(openerp.workflow.StateRectangle.prototype, openerp.workflow.StateBase.prototype, draw2d.VectorFigure.prototype)
openerp.workflow.StateRectangle.implement({
    
    initialize : function(params) {
        
        openerp.workflow.StateBase.call(this, params.id, params.action, params.kind);
        draw2d.VectorFigure.call(this);
        this.lineColor = new draw2d.Color(0,0,0);
        this.setLineWidth(1);
        
        this.init_label(params.flow_start, params.flow_stop, params.name);
    },
    
    createHTMLElement : function() {
        
        var item = draw2d.VectorFigure.prototype.createHTMLElement.call(this);
        item.style.border = 1+"px solid "+this.lineColor.getHTMLStyle();
        
        if(this.bgColor!=null)
            item.style.backgroundColor=this.bgColor.getHTMLStyle();
            
        return item;
    },
        
});


