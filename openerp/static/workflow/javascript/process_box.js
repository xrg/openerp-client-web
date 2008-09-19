
var InfoBox = function(options) {
    this.__init__(options);
}

InfoBox._id = 0;

InfoBox.nextId = function() {
    var id = 'infoBox' + InfoBox._id++;
    while(getElement(id)) {
        id = InfoBox.nextId();
    }
    return id;
}

InfoBox.prototype = {
	
	__init__ : function(options){

        this.options = MochiKit.Base.update({

        }, options || {});

        var btnClose = BUTTON({'class': 'button', 'type': 'button'}, 'Close');
        MochiKit.Signal.connect(btnClose, 'onclick', this, this.hide);

        var title = options.title || 'Information';
        var desc = options.description || '';

        var buttons = MochiKit.Base.map(function(b){
                var res = BUTTON({'class': 'button', 'type': 'button'}, b.name);
                var btnClick = options.buttonClick || function(){};
                MochiKit.Signal.connect(res, 'onclick', function(evt){
                    btnClick(evt, b);
                });
                return res;
        }, options.buttons || []);

        var info = DIV(null,
                    DIV({'class': 'infoTitle'}, title),
                    DIV({'class': 'infoDesc'}, desc),
                        TABLE({'class': 'infoButtons', 'cellpadding': 2}, 
                            TBODY(null, 
                                TR(null,
                                    TD({'width': '100%', 'nowrap': 'nowrap'}, buttons),
                                    TD({'align': 'right'}, btnClose)))));

        this.layer = DIV({'class': 'infoLayer'});
        MochiKit.DOM.appendChildNodes(document.body, this.layer);
        MochiKit.DOM.setOpacity(this.layer, 0.3);
        MochiKit.Signal.connect(this.layer, 'onclick', this, this.hide);

        this.box = DIV({id: InfoBox.nextId(), 'class': 'infoBox'});
        MochiKit.DOM.appendChildNodes(document.body, this.box);

        this.box.innerHTML = "";
        MochiKit.DOM.appendChildNodes(this.box, info);
	},	
	
	show : function(evt) {
		
        MochiKit.DOM.setElementDimensions(this.layer, elementDimensions(document.body));
        //setElementDimensions(this.layer, getViewportDimensions());

        var w = 350;
        var h = 125;

        MochiKit.DOM.setElementDimensions(this.box, {w: w, h: h});

        var x = evt.mouse().page.x;
        var y = evt.mouse().page.y;

        x -= w / 2;
        y -= h - h / 3;

        var vd = elementDimensions(document.body);
        var md = elementDimensions(this.box);

        if ((x + md.w) > vd.w) {
            x -= x + md.w - vd.w;
        }

        x = Math.max(0, x);
        y = Math.max(0, y);

        MochiKit.DOM.setElementPosition(this.box, {x: x, y: y});

        MochiKit.DOM.showElement(this.layer);
        MochiKit.DOM.showElement(this.box);
    },	
	
    hide : function(evt) {
        MochiKit.DOM.hideElement(this.box);
        MochiKit.DOM.hideElement(this.layer);
    }
}

// vim: ts=4 sts=4 sw=4 si et


