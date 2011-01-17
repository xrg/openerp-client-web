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

// requires: mootools & draw2d

if (typeof(openobject) == "undefined") {
    openobject = new Object;
}

if (typeof(openobject.workflow) == "undefined") {
    openobject.workflow = new Object;
}

colors = {
'gray': [155, 155, 155],
'grey': [155, 155, 155],
'red': [236, 20, 60],
'white': [255, 255, 255]
};

openobject.workflow.StateBase = function(id, action, kind, sname, options) {
    this.__init__(id, action, kind, sname, options);
};
    
openobject.workflow.StateBase.prototype = {
    __init__ : function(id, action, kind, name, options) {
        
        this.act_id = id || null;
        this.name = name;
        this.options = MochiKit.Base.update({}, options || {});
        
        this.in_transition = new Array;
        this.out_transition = new Array;
        
        this.portR = null;
        this.portU = null;
        this.portL = null;
        this.portD = null;
    },
    
    init_label : function(color) {
    
        this.setDimension(100, 60);
        this.setDeleteable(false);
        this.setResizeable(false);
        this.setLineWidth(2);
              
        if (!color)
            var c = colors['white'];
        else                 
            var c = colors[color];
            
        this.setBackgroundColor(new draw2d.Color(c[0], c[1], c[2]));
        
        var html = this.getHTMLElement();    
        html.style.textAlign = 'center';
        html.style.marginLeft = 'auto';
        html.style.marginRight = 'auto';           
        this.sgnl_dblclk = MochiKit.Signal.connect(html, 'ondblclick', this, this.ondblClick);
        this.sgnl_clk = MochiKit.Signal.connect(html, 'onclick', this, this.onClick);
        this.disableTextSelection(html);
        
        var span = SPAN({'class': 'stateName', id: this.name}, this.name);
        MochiKit.DOM.appendChildNodes(html, span);
        
        if (!isUndefinedOrNull(this.sname)) {
            var n = this.sname.length;
            var width = 100;
            
            if (n > 10) {
                width = width + Math.round((n - 10) / 2 * 10);
                this.setDimension(width, 60);
            }            
        }
    },
    
    initPort : function() {
        
        var workflow = this.getWorkflow();
        var width = this.getWidth();
        var height = this.getHeight();
        
        this.portR = new openobject.workflow.Port();       
        this.portR.setWorkflow(workflow);
        this.addPort(this.portR, width, height / 2);
        
        this.portU = new openobject.workflow.Port();    
        this.portU.setWorkflow(workflow);        
        this.addPort(this.portU, width / 2, 0);
        
        this.portL = new openobject.workflow.Port();              
        this.portL.setWorkflow(workflow);
        this.addPort(this.portL, 0, height / 2);
        
        this.portD = new openobject.workflow.Port();      
        this.portD.setWorkflow(workflow);         
        this.addPort(this.portD, width / 2, height);
    },  
    
    edit : function() {
        params = {
            '_terp_model' : WORKFLOW.node_obj,
            '_terp_o2m_model': getElement('_terp_model').value,
            '_terp_o2m_id' : WORKFLOW.id
        };
        
        if (!isUndefinedOrNull(this.act_id))
            params['_terp_id'] = this.act_id;
            
        var act = openobject.http.getURL('/view_diagram/workflow/state/edit', params);
        jQuery.frame_dialog({src:act}, null, { height: 450 });
    },

    ondblClick : function(event) {
        new InfoBox(this).show(event);
    },
    
    onClick : function(event) {
        
        if (WORKFLOW.selected == null)
            WORKFLOW.selected = this.workflow.currentSelection;
        else if (WORKFLOW.selected != this)
            WORKFLOW.selected = this.workflow.currentSelection;            
        else {
            if (!this.dragged)
                new InfoBox(this).show(event);                
            else
                this.dragged = false;
        }
    },   
    
    onDragend : function() {
        this.dragged = this.isMoving;
        draw2d.Node.prototype.onDragend.call(this);  
    },
    
    get_act_id : function() {
        return this.act_id;
    },
        
    __delete__ : function() {
        MochiKit.Signal.disconnectAll(this.getHTMLElement(), 'ondblclick', 'onclick');
    }
};

//Oval shape node
openobject.workflow.StateOval = new Class;
openobject.workflow.StateOval.prototype = $merge(openobject.workflow.StateOval.prototype, draw2d.Oval.prototype, openobject.workflow.StateBase.prototype);
openobject.workflow.StateOval.implement({
    
    initialize : function(params) {
        openobject.workflow.StateBase.call(this, params.id, params.action, params.kind, params.name, params.options);
        draw2d.Oval.call(this); 
        
        this.dragged = false;
        this.init_label(params.color);
    }   
});

//Rectangle shape node when it is a sub-workflow
openobject.workflow.StateRectangle = new Class;
openobject.workflow.StateRectangle.prototype = $merge(openobject.workflow.StateRectangle.prototype, draw2d.VectorFigure.prototype, openobject.workflow.StateBase.prototype);
openobject.workflow.StateRectangle.implement({
    
    initialize : function(params) {
        
        openobject.workflow.StateBase.call(this, params.id, params.action, params.kind, params.name, params.options);
        draw2d.VectorFigure.call(this);
        
        this.lineColor = new draw2d.Color(0,0,0);
        this.setLineWidth(1);
        this.init_label(params.color);
    },
    
    createHTMLElement : function() {
        
        var item = draw2d.VectorFigure.prototype.createHTMLElement.call(this);
        item.style.border = 1+"px solid "+this.lineColor.getHTMLStyle();
        
        if(this.bgColor!=null)
            item.style.backgroundColor=this.bgColor.getHTMLStyle();
            
        return item;
    }        
});

// vim: ts=4 sts=4 sw=4 si et
