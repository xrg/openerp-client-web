
var SelectionBox = function(elem) {
    this.__init__(elem);
}

SelectionBox.prototype = {

    __init__ : function(elem) {
        this.element = MochiKit.DOM.getElement(elem);
        this.element_text = MochiKit.DOM.getElement('__text_' + this.element.id);
        this.element_opts = MochiKit.DOM.getElement('__selection_' + this.element.id);
    
        this.evtOnClick = MochiKit.Signal.connect(this.element_text, 'onclick', this, this.onClick);
        this.evtOnKeyDown = MochiKit.Signal.connect(this.element_text, 'onkeydown', this, this.onKeyDown);
    
        this.options = new Array();
        this.values = new Array();
        
        this.selectIndex = -1;
        
        var options = MochiKit.DOM.getElementsByTagAndClassName('a', 'selection-value', this.element_opts);
        var self = this;
    
        MochiKit.Iter.forEach(options, function(opt){
            
            MochiKit.Signal.connect(opt, 'onkeydown', self, self.onCycle);
            MochiKit.Signal.connect(opt, 'onclick', self, self.onSelect);
            
            self.options = self.options.concat(MochiKit.DOM.getNodeAttribute(opt, 'value'));
            self.values = self.values.concat(MochiKit.DOM.scrapeText(opt));
        });
        
        this.setValue(this.element.value);
        
        MochiKit.Signal.connect(document, 'onclick', function(evt){
            if (evt.target() != self.element_text) {
                self.element_opts.style.display = 'none';
            } 
        });
    },

    __delete__ : function() {
    },

    onClick : function(evt) {

        if (this.element.readOnly || this.element.disabled) {
            return;
        }
        
        this.element_opts.style.display = this.element_opts.style.display == 'block' ? 'none' : 'block';
        
        if (this.element_opts.style.display == 'block') {
                
            this.element_opts.style.minWidth = MochiKit.DOM.elementDimensions(this.element_text).w + 'px';
              
            this.element_opts.style.top = (MochiKit.DOM.elementPosition(this.element_text).y + 
                                           MochiKit.DOM.elementDimensions(this.element_text).h + 2) + 'px';
            this.element_opts.style.left = (MochiKit.DOM.elementPosition(this.element_text).x + 2) + 'px';
            
            if (this.selectIndex > -1) {
                var options = MochiKit.DOM.getElementsByTagAndClassName('a', 'selection-value', this.element_opts);
                options[this.selectIndex].focus();
            }
        }
    },

    onKeyDown : function(evt) {

        var alt = evt.modifier().alt;
        var key = evt.key().string;
        
        if (alt && (key == "KEY_ARROW_UP" || key == "KEY_ARROW_DOWN")){
            return this.onClick(evt);
        }
    },

    onSelect : function(evt) {
        var opt = evt.src();
        var value = MochiKit.DOM.getNodeAttribute(opt, 'value');
        
        this.setValue(value);
    
        MochiKit.DOM.hideElement(this.element_opts);
        
        this.element_text.focus();
    },
    
    onCycle : function(evt){

        var a = evt.src();
        var k = evt.key().string;
        
        var opts = a.parentNode.getElementsByTagName('a')
        var idx = MochiKit.Base.findIdentical(opts, a);
        
        if (k == "KEY_ARROW_UP") {
            
            try {
                opts[idx-1].focus();
            }catch(e){}    
        }
        
        if (k == "KEY_ARROW_DOWN") {
            try {
                opts[idx+1].focus();
            }catch(e){}
        }  
        
        if (k == "KEY_ENTER") {
            this.onSelect(evt);
        }
        
        if (k == "KEY_ESCAPE") {
            this.element_opts.style.display = 'none';
            this.element_text.focus();
        }
        
        evt.stop();
    },
    
    setValue : function(value) {
        this.selectIndex = MochiKit.Base.findIdentical(this.options, value);
        if (this.selectIndex > -1) {
            this.element.value = value;
            this.element_text.value = this.values[this.selectIndex];
        }
    }
}

SelectionBox.setValue = function(elem, value) {
    
    var element = MochiKit.DOM.getElement(elem);
    var element_text = MochiKit.DOM.getElement('__text_' + element.id);
    var element_opts = MochiKit.DOM.getElement('__selection_' + element.id);
        
    var opts = MochiKit.DOM.getElementsByTagAndClassName('a', 'selection-value', element_opts);
    
    for(var i=0; i<opts.length; i++) {
        
        var opt = opts[i];
        var val = MochiKit.DOM.getNodeAttribute(opt, 'value');
        
        if (val == value) {
            element.value = value;
            element_text.value = MochiKit.DOM.scrapeText(opt);
            break;
        }
    }
}
