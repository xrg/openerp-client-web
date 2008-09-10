
if (typeof(openerp) == "undefined") {
    openerp = {};
}

if (typeof(openerp.process) == 'undefined') {
    openerp.process = {};
}

openerp.process.NAME = "openerp.process";
openerp.process.VERSION = "4.3";
openerp.process.__repr__ = openerp.process.toString = function () {
    return "[" + this.NAME + " " + this.VERSION + "]";
};

/**
 * openerp.process.Workflow
 */
openerp.process.Workflow = function(canvas) {
    this.__init__(canvas);
}

openerp.process.Workflow.prototype = new draw2d.Workflow();
MochiKit.Base.update(openerp.process.Workflow.prototype, {

    __super__: draw2d.Workflow,

    __init__: function(canvas) {
        this.__super__.call(this, canvas);
        
        this.nodes = {};
        this.transitions = {};
    },
    
    load: function(id) {
    
    	//TODO: fetch nodes and transitions
    	
		var TRANS = {
			11:  {source: 1, target: 2, buttons: [], roles: []},
			22: {source: 1, target: 3, buttons: [], roles: []},
		};

		var NODES = {
		 	1: {x: 100, y: 200, buttons: [], title: 'Sale Order', menu: ''},
			2: {x: 400, y: 50, buttons: [], title: '', menu: ''},
		 	3: {x: 400, y: 350, buttons: [], title: '', menu: ''},
		};

    	for(var id in NODES){
    		var data = NODES[id];
    		var n = new openerp.process.Node(data);
	    	this.addFigure(n, data.x, data.y);
	    	
	    	this.nodes[id] = n; // keep reference
	    }
	    
	    for(var id in TRANS){
    		var data = TRANS[id];
    		var t = new openerp.process.Transition(data);
    		
    		var src = this.nodes[data.source];
    		var dst = this.nodes[data.target];
    		
    		t.setSource(src.outPort);
    		t.setTarget(dst.inPort);
    		
    		this.addFigure(t);
    		
    		this.transitions[id] = t; // keep reference
    	}
    }
   
});

/**
 * openerp.process.Node
 */
openerp.process.Node = function(data) {
    this.__init__(data);
}

openerp.process.Node.prototype = new draw2d.Node();
MochiKit.Base.update(openerp.process.Node.prototype, {

    __super__: draw2d.Node,

    __init__: function(data) {
        this.data = data;
        
        this.__super__.call(this);
        
        this.setDimension(180, 120);
        this.setResizeable(false);
        this.setSelectable(false);
        this.setCanDrag(false);
        this.setColor(null);
    },

    createHTMLElement: function() {
        var elem = this.__super__.prototype.createHTMLElement.call(this);
        elem.style.background = "url(/static/workflow/images/node.png) no-repeat";
                
        elem.innerHTML = (
        "<table border='0' class='node-table'>"+
        "	<tr>"+
        "		<td width='30'></td>"+
        "		<td class='node-title' colspan='5'></td>"+
        "	</tr>"+
        "	<tr>"+
        "		<td colspan='6' class='node-text'></td>"+
        "	</tr>"+
        "	<tr>"+
        "		<td></td>"+
        "		<td class='node-button'></td>"+
        "		<td class='node-button'></td>"+
        "		<td class='node-button'></td>"+
        "		<td class='node-button'></td>"+
        "		<td></td>"+
        "	</tr>"+
        "</table>");
        
        var table = elem.getElementsByTagName('table')[0];
        var title = MochiKit.DOM.getElementsByTagAndClassName('td', 'node-title', table)[0];
        var text = MochiKit.DOM.getElementsByTagAndClassName('td', 'node-text', table)[0];        
        var buttons = MochiKit.DOM.getElementsByTagAndClassName('td', 'node-button', table);
        
        table.cellPadding = table.cellSpacing = 0;        
        title.innerHTML = this.data.title;
        text.innerHTML = this.data.menu;
        
        buttons[0].innerHTML = "<img src='/static/images/stock/gtk-info.png'/>";
        buttons[1].innerHTML = "<img src='/static/images/stock/gtk-new.png'/>";
        buttons[2].innerHTML = "<img src='/static/images/stock/gtk-open.png'/>";
        buttons[3].innerHTML = "<img src='/static/images/stock/gtk-print.png'/>";

		elem.className = 'node';
        return elem;
    },
    
    setWorkflow: function(workflow) {
    	this.__super__.prototype.setWorkflow.call(this, workflow);
    	
    	this.outPort = new draw2d.OutputPort();
        this.inPort = new draw2d.OutputPort();
        
        this.outPort.setWorkflow(workflow);
        this.inPort.setWorkflow(workflow);
        
        this.addPort(this.outPort, this.width, this.height/2);
        this.addPort(this.inPort, 0, this.height/2);
        
        this.inPort.getHTMLElement().style.display = 'none';    
    	this.outPort.getHTMLElement().style.display = 'none';
    }
});

/**
 * openerp.process.Transition
 */
openerp.process.Transition = function(data) {
    this.__init__(data);
}

openerp.process.Transition.prototype = new draw2d.Connection();
MochiKit.Base.update(openerp.process.Transition.prototype, {

    __super__: draw2d.Connection,

    __init__: function(data) {
        this.__super__.call(this);
        this.setRouter(new draw2d.ManhattanConnectionRouter());
        this.setTargetDecorator(new openerp.process.TargetDecorator());
        this.setLineWidth(2);
        this.setSelectable(false);
    }

});

/**
 * openerp.process.TargetDecorator
 */
openerp.process.TargetDecorator = function() {
    this.__init__();
}

openerp.process.TargetDecorator.prototype = new draw2d.ArrowConnectionDecorator();
MochiKit.Base.update(openerp.process.TargetDecorator.prototype, {

    __super__: draw2d.ArrowConnectionDecorator,

    __init__: function() {
        this.__super__.call(this);
	    this.setBackgroundColor(new draw2d.Color(0, 0, 0));
    },
    
    paint: function(/*draw2d.Graphics*/ g) {
		
		if(this.backgroundColor!=null) {
     		g.setColor(this.backgroundColor);
     		g.fillPolygon([0, 6, 6, 0], [0, 6, -6, 0]);
  		}

		 // draw the border
		g.setColor(this.color);
		g.setStroke(1);
		g.drawPolygon([0, 6, 6, 0], [0, 6, -6, 0]);
	}
});

// vim: ts=4 sts=4 sw=4 si et


