
if (typeof(openerp) == "undefined") {
    openerp = new Object;
}

if (typeof(openerp.workflow) == "undefined") {
    openerp.workflow = new Object;
}


openerp.workflow.Connector=function(id, signal, condition)
{
	draw2d.Connection.call(this);
	this.setTargetDecorator(new draw2d.ArrowConnectionDecorator());
	this.setRouter(new draw2d.BezierConnectionRouter());
	  
	var html = this.getHTMLElement();
	
	MochiKit.Signal.connect(html, 'ondblclick', this, this.ondblClick);
	MochiKit.Signal.connect(html, 'onmouseover', this, this.onmouseOver);
	MochiKit.Signal.connect(html, 'onmouseout', this, this.onmouseOut);
	
	
	this.sourceId = null;
	this.destId = null;
	this.setDeleteable(false);
	
	if(id)
	{
		this.tr_id = id;
		this.signal = signal;
		this.condition = condition;
	}
	
}

openerp.workflow.Connector.prototype = new draw2d.Connection();

openerp.workflow.Connector.prototype.ondblClick = function(event) {	
		new InfoBox(this).show(event);
}

openerp.workflow.Connector.prototype.onmouseOver = function(event){
	tr_info.style.visibility = 'visible';		
	tr_info.innerHTML = "<span></span>"+"Condition:"+this.condition+"<span></span>"+" | Signal:"+this.signal;
}


openerp.workflow.Connector.prototype.onmouseOut = function(event){
	tr_info.style.visibility = 'hidden';		
	
}

openerp.workflow.Connector.prototype.edit = function() {
	
	params = {
		'_terp_model' : 'workflow.transition',
		'_terp_start' : this.getSource().getParent().get_act_id(),
		'_terp_end' : this.getTarget().getParent().get_act_id()
		}
		
		if(!isUndefinedOrNull(this.tr_id))
			params['_terp_id'] = this.tr_id	;	
			
		var act = getURL('/connector/edit', params);
		openWindow(act);
}

openerp.workflow.Connector.prototype.get_tr_id = function() {
	return this.tr_id;
}

openerp.workflow.Connector.prototype.__delete__ = function() {
		MochiKit.Signal.disconnect(this.signal);
}

openerp.workflow.Connector.prototype.setSource = function(port) {
	draw2d.Connection.prototype.setSource.call(this,port);
	
	if(this.sourceId==null)
		this.sourceId = port.getParent().get_act_id();
	else if(this.sourceId != port.getParent().get_act_id())
	{
		this.sourceId = port.getParent().get_act_id();
		req = Ajax.JSON.post('/connector/change_ends',{id:this.tr_id, field:'act_from', value:this.sourceId});
	}
}

openerp.workflow.Connector.prototype.setTarget = function(port) {
	draw2d.Connection.prototype.setTarget.call(this,port);
	
	if(this.destId==null)
		this.destId = port.getParent().get_act_id();
	else if(this.destId != port.getParent().get_act_id())
	{
		this.destId = port.getParent().get_act_id();
		req = Ajax.JSON.post('/connector/change_ends',{id:this.tr_id, field:'act_to', value:this.destId});
	}
}

