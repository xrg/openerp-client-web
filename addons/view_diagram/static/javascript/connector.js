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


openobject.workflow.Connector = function(id, from, to, options) {
	
    draw2d.Connection.call(this);
    this.setLineWidth(2);
    this.setColor(new draw2d.Color(180, 180, 180));
    this.setTargetDecorator(new openobject.workflow.ConnectionDecorator());
    
    this.setSourceAnchor(new openobject.workflow.ConnectionAnchor());
    this.setTargetAnchor(new openobject.workflow.ConnectionAnchor());
    this.setRouter(new draw2d.NullConnectionRouter());
	  
    var html = this.getHTMLElement();
    html.style.cursor = 'pointer';
	
    MochiKit.Signal.connect(html, 'ondblclick', this, this.ondblClick);
    MochiKit.Signal.connect(html, 'onmouseover', this, this.onmouseOver);
    MochiKit.Signal.connect(html, 'onmouseout', this, this.onmouseOut);
    MochiKit.Signal.connect(html, 'onclick', this, this.onClick);
	
	
    this.sourceId = null;
    this.destId = null;
    this.setDeleteable(false);
	
    if (id) {
        this.tr_id = id;
        this.from = from;
        this.to = to;
        this.isOverlaping = false;
        this.OverlapingSeq = 0;
        this.totalOverlaped = 0;
        this.options = MochiKit.Base.update({}, options || {});
        this.sourceAnchor.conn_id = id;
        this.targetAnchor.conn_id = id;
    }
};

openobject.workflow.Connector.prototype = new draw2d.Connection();

openobject.workflow.Connector.prototype.ondblClick = function(event) {	
    new InfoBox(this).show(event);
};

openobject.workflow.Connector.prototype.onClick = function(event) {
    
    if (WORKFLOW.selected == this)
        new InfoBox(this).show(event);
};


openobject.workflow.Connector.prototype.onmouseOver = function(event) {
    str = '';
    for (f in this.options) 
        str += f + ': ' + this.options[f] + ' | '
            
    openobject.dom.get('status').innerHTML = str.substring(0, str.length - 3);//"Condition: " + this.condition + " | Signal: "+ this.signal;
};

openobject.workflow.Connector.prototype.onmouseOut = function(event) {
    openobject.dom.get('status').innerHTML = '';
};

openobject.workflow.Connector.prototype.edit = function() {
    params = {
        '_terp_model' : WORKFLOW.connector_obj,//'workflow.transition',
        '_terp_start' : this.getSource().getParent().get_act_id(),
        '_terp_end' : this.getTarget().getParent().get_act_id(),
        '_terp_m2o_model': WORKFLOW.node_obj
    };
	
    if (!isUndefinedOrNull(this.tr_id))
        params['_terp_id'] = this.tr_id;
		
	var act = openobject.http.getURL('/view_diagram/workflow/connector/edit', params);
	openobject.tools.openWindow(act);
}

openobject.workflow.Connector.prototype.get_tr_id = function() {
    return this.tr_id;
};

openobject.workflow.Connector.prototype.__delete__ = function() {
    MochiKit.Signal.disconnectAll(this.getHTMLElement(), 'ondblclick', 'onmouseover', 'onmouseout', 'onclick');
};

openobject.workflow.Connector.prototype.setSource = function(port) {
	
    draw2d.Connection.prototype.setSource.call(this, port);
	
    if (this.sourceId == null)
        this.sourceId = port.getParent().get_act_id();
    else if (this.sourceId != port.getParent().get_act_id()) {
        this.sourceId = port.getParent().get_act_id();

        req = openobject.http.postJSON('/view_diagram/workflow/connector/change_ends', {conn_obj: WORKFLOW.connector_obj,
            id: this.tr_id,
            field: WORKFLOW.src_node_nm,
            value: this.sourceId});
    }
};

openobject.workflow.Connector.prototype.setTarget = function(port) {
    draw2d.Connection.prototype.setTarget.call(this, port);
	
    if (this.destId == null)
        this.destId = port.getParent().get_act_id();
    else if (this.destId != port.getParent().get_act_id()) {
        this.destId = port.getParent().get_act_id();

        req = openobject.http.postJSON('/view_diagram/workflow/connector/change_ends', {conn_obj: WORKFLOW.connector_obj,
            id: this.tr_id,
            field: WORKFLOW.des_node_nm,
            value: this.destId});
    }
};
