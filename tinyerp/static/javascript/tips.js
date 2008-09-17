// Based on Tips.js of Mootools (http://mootools.net) which is again based on 
// Bubble Tooltips (http://web-graphics.com/mtarchive/001717.php) 
// by Alessandro Fulcitiniti (http://web-graphics.com)

var Tips = function(elements, options) {
    this.__init__(elements, options);
}

Tips.prototype = {

__init__ : function(elements, options) {

    this.options = MochiKit.Base.update({
        wait: 1,            // wait for n seconds
        maxTitleChars: 255  // number of chars in title
    }, options || {});

    this.deferred = null;
    this.elements = elements;

    this.toolTitle = SPAN({'class': 'tipTitle'});
    this.toolText = P({'class': 'tipText'});
    
    this.toolTip = TABLE({'class': 'tooltip'},
                        TBODY(null,
                            TR(null,
                                TD({'class': 'tip-tl', 'nowrap': 'nowrap'}),
                                TD({'class': 'tip-t'}),
                                TD({'class': 'tip-tr', 'nowrap': 'nowrap'})),
                            TR(null,
                                TD({'class': 'tip-l'}),
                                TD({'class': 'tip-text'}, 
                                    this.toolTitle, this.toolText),
                                TD({'class': 'tip-r'})),
                            TR(null,
                                TD({'class': 'tip-bl'}),
                                TD({'class': 'tip-b'}),
                                TD({'class': 'tip-br'}))));
                                
                            
    this.toolTip.cellPadding = 0;
    this.toolTip.cellSpacing = 0;
    
    MochiKit.DOM.appendChildNodes(document.body, this.toolTip);

    MochiKit.Iter.forEach(elements, function(el) {
        
        el = MochiKit.DOM.getElement(el);
        el.myText = MochiKit.DOM.getNodeAttribute(el, 'title');

        if (el.myText) 
            el.removeAttribute('title');

        if (el.href){
            if (el.href.indexOf('http://') > -1) el.myTitle = el.href.replace('http://', '');
            if (el.href.length > this.options.maxTitleChars) el.myTitle = el.href.substr(0,this.options.maxTitleChars-3)+"...";
        }
        
        if (el.myText && el.myText.indexOf('::') > -1){
            var dual = el.myText.split('::');
            el.myTitle = MochiKit.Format.strip(dual[0]);
            el.myText = MochiKit.Format.strip(dual[1]);
        }
        
        MochiKit.Signal.connect(el, 'onmouseover', this, this.showLater);
        MochiKit.Signal.connect(el, 'onmousemove', this, this.locate);
        MochiKit.Signal.connect(el, 'onmouseout', this, this.hide)

    }, this);
},

    showLater: function(evt){
        this.deferred = MochiKit.Async.callLater(this.options.wait, MochiKit.Base.bind(this.show, this), evt);
    },

    show: function(evt){

        var el = evt.src();
        var text = el.myText;
        var title = el.myTitle;
        
        // if plain text then replace \n with <br>
        if (! /<\w+/.test(text)) {
            text = text.replace(/\n|\r/g, '<br>');
        }
        
        title = text ? title : '';

        this.toolTitle.innerHTML = title;
        this.toolText.innerHTML = text ? text : el.myTitle;
        
        this.toolTitle.style.display = title ? 'block' : 'none';

        MochiKit.DOM.showElement(this.toolTip);
    },

    locate: function(evt){
        var doc = document.documentElement;
        var el = evt.src();

        var ps = MochiKit.DOM.elementPosition(el)
        var vd = MochiKit.DOM.getViewportDimensions();
        var md = MochiKit.DOM.elementDimensions(this.toolTip);

        var x = evt.mouse().client.x + doc.scrollLeft - 30;
        var y = evt.mouse().client.y + doc.scrollTop + 15;

        if ((x + md.w) > vd.w - 30) {
            x -= x + md.w - vd.w;
            x -= 20;
        }

        this.toolTip.style.top = y + 'px';
        this.toolTip.style.left = x + 'px';
    },

    hide: function(){
        if (this.deferred) {
            this.deferred.cancel();
        }
        MochiKit.DOM.hideElement(this.toolTip);
    }
}

MochiKit.DOM.addLoadEvent(function(evt){

    if (window.browser.isOpera){
        return;
    }

    var elements = MochiKit.Base.filter(function(e){

        var text = MochiKit.DOM.getNodeAttribute(e, 'title');
        if (!text)
            return false;
        
        var title = MochiKit.DOM.scrapeText(e).replace(/^\s*\?\s*|\s*\:\s*$/g, '');
        MochiKit.DOM.setNodeAttribute(e, 'title', title + '::' + text);

        return true;

    }, MochiKit.DOM.getElementsByTagAndClassName('td', 'label', document));
    
    new Tips(elements);
});

// vim: ts=4 sts=4 sw=4 si et


