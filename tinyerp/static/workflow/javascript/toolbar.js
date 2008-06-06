
// requires: mootools & draw2d

if (typeof(openerp) == "undefined") {
    openerp = new Object;
}

if (typeof(openerp.workflow) == "undefined") {
    openerp.workflow = new Object;
}

// Toolbar Class
openerp.workflow.Toolbar = new Class;
openerp.workflow.Toolbar.prototype = $merge(openerp.workflow.Toolbar.prototype, draw2d.ToolPalette.prototype);

openerp.workflow.Toolbar.implement({
    
    initialize : function() {

        draw2d.ToolPalette.call(this, "Tools");

        this.tool1 = new openerp.workflow.ToolShowGrid(this);
        this.tool2 = new openerp.workflow.ToolCreateState(this);
			
        this.tool1.setPosition(13, 10);
        this.tool2.setPosition(13, 40);
        
        this.addChild(this.tool1);
        this.addChild(this.tool2);

        this.setDimension(30, 300);
    },
    
    createHTMLElement : function() {

        var item = draw2d.ToolPalette.prototype.createHTMLElement.call(this);

        if (this.hasTitleBar()) {
            this.titlebar.style.backgroundImage = "url(/static/workflow/images/window_toolbar.png)";
        }

        item.style.backgroundImage = "url(/static/workflow/images/window_bg.png)";
        return item;
    },

    onSetDocumentDirty : function() {
    }

});

// Tool buttons

// Class: ToolToggle
openerp.workflow.ToolToggle = new Class;
openerp.workflow.ToolToggle.prototype = $merge(openerp.workflow.ToolToggle.prototype, draw2d.ToggleButton.prototype);

openerp.workflow.ToolToggle.implement({
    
    initialize : function(palette, image) {
        this.image = image;
        draw2d.ToggleButton.call(this, palette);
    },

    getImageUrl : function() {
        return this.image;
    }
});

// Class: ToolGeneric
openerp.workflow.ToolGeneric = new Class;
openerp.workflow.ToolGeneric.prototype = $merge(openerp.workflow.ToolGeneric.prototype, draw2d.ToolGeneric.prototype);

openerp.workflow.ToolGeneric.implement({
    
    initialize : function(palette, image) {
        this.image = image;
        draw2d.ToolGeneric.call(this, palette);
    },

    getImageUrl : function() {
        return this.image;
    }
});

// Class: ToolShowGrid
openerp.workflow.ToolShowGrid = openerp.workflow.ToolToggle.extend({

    initialize : function(palette) {
        this.parent(palette, '/static/workflow/images/ToolShowGrid.png');
    },

    execute : function() {
        var isdown = this.isDown();
        this.getToolPalette().getWorkflow().setBackgroundImage(isdown ? '/static/workflow/images/grid_10.png' : null, isdown);

        this.getToolPalette().getWorkflow().setGridWidth(10, 10);
        this.getToolPalette().getWorkflow().setSnapToGrid(isdown);
    }
});

// Class: ToolCreateState
openerp.workflow.ToolCreateState = openerp.workflow.ToolGeneric.extend({

    initialize : function(palette) {
        this.parent(palette, '/static/workflow/images/ToolOval.png');
    },

	execute : function(x, y) {
	    
		WORKFLOW.state.setPosition(x,y);
		
		var html = WORKFLOW.state.getHTMLElement();
		html.style.display = '';
		WORKFLOW.state.edit();
		html.style.display = 'none';

        // call the parent method
        openerp.workflow.ToolGeneric.prototype.execute.call(this, x, y);
    }
});

openerp.workflow.ToolCreateSubwkf = openerp.workflow.ToolGeneric.extend({
	
	initialize : function(palette) {
		this.parent(palette, '/static/workflow/images/ToolRectangle.png');
	},
	
	execute : function(x,y) {
		
		var figure= new draw2d.Rectangle();
        figure.setDimension(60, 60);
        figure.setBackgroundColor(new draw2d.Color(255, 255, 255));
        this.palette.workflow.addFigure(figure, x, y);

        // call the parent method
        openerp.workflow.ToolGeneric.prototype.execute.call(this, x, y);
	}
	
});

