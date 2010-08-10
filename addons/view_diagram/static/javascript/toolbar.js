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
// -   All names, links and logos of Tiny, OpenERP and Axelor must be 
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

// Toolbar Class
openobject.workflow.Toolbar = new Class;
openobject.workflow.Toolbar.prototype = $merge(openobject.workflow.Toolbar.prototype, draw2d.ToolPalette.prototype);

openobject.workflow.Toolbar.implement({
    
    initialize : function() {

        draw2d.ToolPalette.call(this, "Tools");

        this.tool1 = new openobject.workflow.ToolShowGrid(this);
        this.tool2 = new openobject.workflow.ToolCreateState(this);
			
        this.tool1.setPosition(13, 10);
        this.tool2.setPosition(13, 40);
        
        this.addChild(this.tool1);
        this.addChild(this.tool2);

        this.tool1.setActive(1);
        this.setDimension(30, 300);
    },
    
    createHTMLElement : function() {

        var item = draw2d.ToolPalette.prototype.createHTMLElement.call(this);

        item.style.backgroundImage = 'none';//"url(/static/workflow/images/window_bg.png)";

        if (this.hasTitleBar()) {        	
            this.titlebar.style.backgroundImage = "url(/view_diagram/static/images/window_toolbar.png)";
        }
        
        return item;
    },

    onSetDocumentDirty : function() {
    }

});

// Tool buttons

// Class: ToolToggle
openobject.workflow.ToolToggle = new Class;
openobject.workflow.ToolToggle.prototype = $merge(openobject.workflow.ToolToggle.prototype, draw2d.ToggleButton.prototype);

openobject.workflow.ToolToggle.implement({
    
    initialize : function(palette, image) {
        this.image = image;        
        draw2d.ToggleButton.call(this, palette);
        this.getHTMLElement().title = 'Show grid';
    },

    getImageUrl : function() {
        return this.image;
    }
});

// Class: ToolGeneric
openobject.workflow.ToolGeneric = new Class;
openobject.workflow.ToolGeneric.prototype = $merge(openobject.workflow.ToolGeneric.prototype, draw2d.ToolGeneric.prototype);

openobject.workflow.ToolGeneric.implement({
    
    initialize : function(palette, image) {
        this.image = image;
        draw2d.ToolGeneric.call(this, palette);
        this.getHTMLElement().title = 'Create State';
    },

    getImageUrl : function() {
        return this.image;
    }
});

// Class: ToolShowGrid
openobject.workflow.ToolShowGrid = openobject.workflow.ToolToggle.extend({

    initialize : function(palette) {
        this.parent(palette, '/view_diagram/static/images/ToolShowGrid.jpg');
    },

    execute : function() {
        var isdown = this.isDown();
        
        WORKFLOW.setBackgroundImage(isdown ? '/view_diagram/static/images/grid_10.jpg' : null, isdown);
        WORKFLOW.setGridWidth(10, 10);
        WORKFLOW.setSnapToGrid(isdown);
    }
});

// Class: ToolCreateState
openobject.workflow.ToolCreateState = openobject.workflow.ToolGeneric.extend({

    initialize : function(palette) {
        this.parent(palette, '/view_diagram/static//images/ToolOval.jpg');
    },

	execute : function(x, y) {
	    
		WORKFLOW.state.setPosition(x,y);
		
		var html = WORKFLOW.state.getHTMLElement();
		html.style.display = '';
		WORKFLOW.state.edit();
		html.style.display = 'none';

        // call the parent method
        openobject.workflow.ToolGeneric.prototype.execute.call(this, x, y);
    }
});

// vim: ts=4 sts=4 sw=4 si et
