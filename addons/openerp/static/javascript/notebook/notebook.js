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
// -   All names, links and logos of Tiny, Open ERP and Axelor must be 
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

/**
 *
 * @event show triggered when a tab of the notebook is displayed
 *  @argument notebook the notebook instance this
 *                     event was triggered from
 *  @argument tab the (DOM element) tab being showed
 * @event hide triggered when a tab of the notebook is hidden
 *  @arguments 'see show'
 * @event activate triggered when a tab is set as the active tab
 *  @arguments 'see show'
 * @event remove triggered when a tab is removed from the notebook
 *  @arguments 'see show'
 * @event click triggered when the notebook's tab bar is clicked
 *  @arguments 'see show'
 *
 */
var Notebook = function(element, options) {

    var cls = arguments.callee;
    if (!(this instanceof cls)) {
        return new cls(element, options);
    }

    return this.__init__(element, options);
};

Notebook.prototype = {

    __class__: Notebook,

    repr : function() {
        return "[Notebook]";
    },
    
    toString: MochiKit.Base.forwardCall("repr"),
    
    __init__ : function(element, options) {
        this.element = openobject.dom.get(element);
        
        if (!this.element) {
            throw "Invalid argument:" + element;
        }
        
        if (this.element.notebook) {
            return this.element.notebook;
        }
        
        this.options = MochiKit.Base.update({
            'closable': true,
            'scrollable': true,
            'remember': true,
            'onclose': null
        }, options || {});
        
        this.prepare();
                
        this.element.notebook = this;
        return this;
    },
    
    destroy: function() {
        MochiKit.Signal.disconnect(this.evtResize);
        MochiKit.Signal.disconnect(this.evtLeftClick);
        MochiKit.Signal.disconnect(this.evtRightClick);
        MochiKit.Signal.disconnect(this.evtStripClick);
    },

    prepare: function() {
    
        this.rendered = false;
        
        this.elemLeft = DIV({'class': 'notebook-tabs-left'});
        this.elemRight = DIV({'class': 'notebook-tabs-right'});
        this.elemWrap = DIV({'class': 'notebook-tabs-wrap'});
        this.elemStrip = UL({'class': 'notebook-tabs-strip'});
        this.elemStack = DIV({'class': 'notebook-pages'});
        
        this.cookie = '_notebook_' +  this.element.id + '_active_page';
        
        this.tabs = [];
        this.pages = [];
               
        var pages = MochiKit.Base.filter(function(e){
            return e.tagName == 'DIV';
        }, this.element.childNodes);
        

        for(var i=0; i<pages.length; i++) {
        
            var page = pages[i];
            var text = page.title || "Page " + i;
            var id = page.id || 'none';
            
            text = text.split('|');
            
            var help = text.length > 1 ? text[1] : "";            
            var closable = this.options.closable;
            
            if (text.length > 2) {
                closable = parseInt(text[2]);
                closable = isNaN(closable) ? this.options.closable : closable;
            }
            
            text = text[0];
            
            this.add(page, {
                text: text,
                id: id,
                help: help,
                closable: closable,
                activate: false,
                css: page.className
            });
        }
        
        MochiKit.DOM.appendChildNodes(this.elemWrap, this.elemStrip);        
        MochiKit.DOM.appendChildNodes(this.element, 
            DIV({'class': 'notebook-tabs'},
                this.elemRight,
                this.elemLeft,
                this.elemWrap),
            this.elemStack);
            
        MochiKit.DOM.addElementClass(this.element, 'notebook');
        
        this.evtResize = MochiKit.Signal.connect(window, 'onresize', this, this.onResize);
        this.evtLeftClick = MochiKit.Signal.connect(this.elemLeft, 'onclick', this, this.onScrollLeft);
        this.evtRightClick = MochiKit.Signal.connect(this.elemRight, 'onclick', this, this.onScrollRight);
        
        this.evtStripClick = MochiKit.Signal.connect(this.elemStrip, 'onclick', this, this.onStripClick);
        this.rendered = true;
        
        this.adjustSize();

        var self = this;
        MochiKit.Async.callLater(0, function() {
            var i = self.options.remember ? parseInt(openobject.http.getCookie(self.cookie)) || 0 : 0;
            self.show(i);
        });

        showElement(this.element);
        
        this.adjustSize();
    },
    
    getTab: function(tab) {
    
        if (typeof(tab) == "number") {
            if (tab >= this.tabs.length)
                return null;
            tab = this.tabs[tab];
        }
        
        return tab;
    },
        
    getActiveTab: function() {
        return this.activeTab || null;
    },
    
    getPage: function(tab) {
        try {
            return this.pages[findIdentical(this.tabs, this.getTab(tab))];
        } catch(e){}
        return null;
    },
    
    getNext: function(tab) {
    
        var tab = this.getTab(tab);
        var i = findIdentical(this.tabs, tab);
        
        for(var j=i+1; j<this.tabs.length; j++) {
            var t = this.tabs[j];
            if (t.style.display == "none") {
                continue;
            }
            return t;
        }
        return null;
    },
    
    getPrev: function(tab) {
    
        var tab = this.getTab(tab);
        var i = findIdentical(this.tabs, tab);
        
        for(var j=i-1; j>=0; j--) {
            var t = this.tabs[j];
            if (t.style.display == "none") {
                continue;
            }
            return t;
        }
        return null;
    },
    
    setClosable: function(tab, closable) {
    
        var tab = this.getTab(tab);
        if (!tab) {
            return;
        }
        
        var prop = closable ? "addElementClass" : "removeElementClass";
        MochiKit.DOM[prop](tab, 'notebook-tab-closable');
        
        if (closable && !tab.elemClose) {
            tab.elemClose = SPAN({'href': 'javascript: void(0)', 'class': 'tab-close'});
            MochiKit.DOM.appendChildNodes(tab, tab.elemClose);
        } else if (!closable && tab.elemClose) {
            MochiKit.DOM.removeElement(tab.elemClose);
            tab.elemClose = null;
        }
    },
    
    add: function(content, options) {
    
        var options = MochiKit.Base.update({
            text: "",                         // text of the tab
            id: "",							  // ID of tab for static menu
            help: "",                         // help text for the tab
            closable: this.options.closable,  // make the tab closable
            activate: true,                   // activate the tab or not
            css: null                         // additional css class
        }, options || {});
        
        var text = options.text ? options.text : 'Page ' + this.tabs.length;
        var page = content && content.tagName == "DIV" ? content : DIV({}, content);
        
        page.title = "";
        page.className = "";
        
        MochiKit.DOM.addElementClass(page, 'notebook-page');
        
        var tab = LI({'class': 'notebook-tab', 'title': options.help, 'id': options.id},
                        A({'href': 'javascript: void(0)', 'class': 'tab-title'}, 
                            SPAN(null, text)));
                            
        if (typeof(options.css) == "string") {
            MochiKit.DOM.addElementClass(tab, options.css);
        }
                            
        if (options.closable) {
        
            tab.elemClose = SPAN({'href': 'javascript: void(0)', 'class': 'tab-close'});
            MochiKit.DOM.appendChildNodes(tab, tab.elemClose);
                
            MochiKit.DOM.addElementClass(tab, 'notebook-tab-closable');
        }
        
        this.tabs = this.tabs.concat(tab);
        this.pages = this.pages.concat(page);
        
        MochiKit.DOM.appendChildNodes(this.elemStrip, tab);
        MochiKit.DOM.appendChildNodes(this.elemStack, page);
        
        this.show(tab, options.activate);
    },
    
    remove: function(tab) {
    
        var tab = this.getTab(tab);
        if (!tab) {
            return;
        }
        
        if (typeof(this.options.onclose) == "function" &&
            !this.options.onclose(this, tab)) {
            return;
        }
        
        this.hide(tab);
        
        var i = findIdentical(this.tabs, tab);
        var page = this.pages[i];
        
        this.tabs.splice(i, 1);
        this.pages.splice(i, 1);
        
        MochiKit.DOM.removeElement(tab);
        MochiKit.DOM.removeElement(page);
        
        MochiKit.Signal.signal(this, "remove", this, tab);
    },
    
    show: function(tab, activate) {
    
        var tab = this.getTab(tab);
        var activate = typeof(activate) == "undefined" ? true : activate;
        
        if (!tab || tab == this.activeTab) {
            return;
        }
        
        if (activate) {
        
            if (this.activeTab) {
                var at = this.activeTab;
                var pg = this.activePage;
                
                MochiKit.DOM.removeElementClass(at, 'notebook-tab-active');
                MochiKit.DOM.removeElementClass(pg, 'notebook-page-active');
            }
            
            var i = findIdentical(this.tabs, tab);
            var page = this.pages[i];
            
            MochiKit.DOM.addElementClass(tab, 'notebook-tab-active');
            MochiKit.DOM.addElementClass(page, 'notebook-page-active');
        }
        
        tab.style.display = "";
        
        MochiKit.Signal.signal(this, "show", this, tab);
        
        if (activate) {
            this.setActiveTab(tab);
        }
        this.adjustScroll();
    },
    
    hide: function(tab) {
    
        var tab = this.getTab(tab);
        
        if (!tab) {
            return;
        }
        
        var i = findIdentical(this.tabs, tab);
        var t = null;
        
        if (tab == this.activeTab) {
            t = this.getNext(tab) || this.getPrev(tab);
        }
            
        tab.style.display = "none";
        
        MochiKit.Signal.signal(this, "hide", this, tab);    
        
        if (t) {
            this.show(t);
        }
        this.adjustScroll();
    },
    
    setActiveTab: function(tab) {
    
        var tab = this.getTab(tab);
        if (!tab) {
            return;
        }
        
        if (this.options.scrollable) {
        
            var x = this.elemWrap.scrollLeft;
            var w = this.widthWrap;
            
            var left = getElementPosition(tab, this.elemWrap).x + x;
            var right = left + getElementDimensions(tab).w;
            
            var s = this.elemWrap.scrollLeft;
            
            if (left < x) {
                s = left - this.marginTab;
            } else if (right > (x + w)){
                s = right - w;
            }
            
            this.elemWrap.scrollLeft = s;
            this.activateScrollers();
            /*Scroll(this.elemWrap, {
                to: s,
                afterFinish: bind(this.activateScrollers, this)
            }); */
        }
        
        this.activeTab = tab;
        this.activePage = this.getPage(tab);
        
        if (this.options.remember) {
            openobject.http.setCookie(this.cookie, findIdentical(this.tabs, tab));
        }
        
        MochiKit.Signal.signal(this, "activate", this, tab);
    },
    
    adjustScroll: function() {
    
        if (!this.options.scrollable) {
            return;
        }
        
        if (!this.rendered) {
            return;
        }
    
        var w = MochiKit.Style.getElementDimensions(this.elemWrap).w;
        var t = 0;
        
        var self = this;
        
        this.marginTab = 3;
        this.marginWrap = 0;
                
        MochiKit.Iter.forEach(this.tabs, function(e){
            if (e.style.display != "none")
                t += e.offsetWidth + self.marginTab;
        });
        
        this.widthWrap = w;
        this.widthTabs = t;
                
        if (t <= w) {
        
            MochiKit.DOM.hideElement(this.elemLeft);
            MochiKit.DOM.hideElement(this.elemRight);
            MochiKit.DOM.removeElementClass(this.elemWrap, 'notebook-tabs-wrap-scrollable');
            
            this.elemWrap.scrollLeft = 0;
            
        } else {
        
            MochiKit.DOM.showElement(this.elemLeft);
            MochiKit.DOM.showElement(this.elemRight);            
            MochiKit.DOM.addElementClass(this.elemWrap, 'notebook-tabs-wrap-scrollable');
            
            // adjust size of scrollers
            var h = getElementDimensions(this.elemStrip).h;
            setElementDimensions(this.elemLeft, {h: h - 1});
            setElementDimensions(this.elemRight, {h: h - 1});
            
            var x = this.elemWrap.scrollLeft;
            var l = t - x;
            
            if (l < w) {
                this.elemWrap.scrollLeft = x - (w - l);
                this.activateScrollers();
                /*Scroll(this.elemWrap, {
                    to: x - (w - l),
                    afterFinish: bind(this.activateScrollers, this)
                });*/
            } else {
                this.setActiveTab(this.activeTab);
            }
            
        }
    },
    
    activateScrollers: function() {
    
        var p = this.elemWrap.scrollLeft;
        var w = this.widthTabs - p - this.widthWrap;
                
        if (p > 0) {
            removeElementClass(this.elemLeft, "notebook-tabs-left-disabled");
        } else {
            addElementClass(this.elemLeft, "notebook-tabs-left-disabled");
        }
    
        if (w > 0) {
            removeElementClass(this.elemRight, "notebook-tabs-right-disabled");
        } else {
            addElementClass(this.elemRight, "notebook-tabs-right-disabled");
        }
        
    },

    adjustSize: function() {
    
        //XXX: doesn't work properly under IE
    
        hideElement(this.elemWrap);
        var w = this.element.parentNode.clientWidth;  
         
        w = w < this.widthTabs ? w - 36 : w;
        
        w = Math.max(0, w - 2);
        
        setElementDimensions(this.elemWrap, {w: w});
        showElement(this.elemWrap);
        
        if (browser.isIE) {
            
            with (this.elemRight) {
                style.top = '1px';
                style.right = '4px';
            }
            
            with (this.elemLeft) {
                style.top = '1px';
                style.left = '-18px';
            }
        }
        
        this.adjustScroll();
    },
        
    onResize: function(evt) {    
        this.adjustSize();
    },
    
    onStripClick: function(evt) {
        var tab = evt.target();
        var action = MochiKit.DOM.hasElementClass(tab, 'tab-close') ? 'remove' : 'show';
        
        tab = tab.tagName == "LI" ? tab : getFirstParentByTagAndClassName(evt.target(), 'li');
        
        if (tab) {
            this[action](tab)
        }
        
        if (tab && tab == this.activeTab) {
            this.setActiveTab(tab);
        }
        
        if (action == "show") {
            MochiKit.Signal.signal(this, 'click', this, tab);
        }
    },
    
    onScrollRight: function(evt) {
        var w = this.widthTabs - this.widthWrap;
        var x = this.elemWrap.scrollLeft;
        
        var s = Math.min(w, x + 100);

        this.elemWrap.scrollLeft = s;
        this.activateScrollers();
        /*Scroll(this.elemWrap, {
            to: s,
            afterFinish: bind(this.activateScrollers, this)
        });*/
    },
    
    onScrollLeft: function(evt) {
        var x = this.elemWrap.scrollLeft;
        var s = Math.max(0, x - 100);
        
        this.elemWrap.scrollLeft = s;
        this.activateScrollers();
        /*Scroll(this.elemWrap, {
            to: s,
            afterFinish: bind(this.activateScrollers, this)
        });*/
    }

};

Notebook.adjustSize = function(callback) {

    var elems = MochiKit.Base.filter(function(e){
        return e.notebook;
    }, openobject.dom.select('div.notebook'));
    
    MochiKit.Iter.forEach(elems, function(e){
        hideElement(e.notebook.elemWrap);
    });
    
    if (typeof(callback) == "function")
        callback();
        
    MochiKit.Iter.forEach(elems, function(e){
        e.notebook.adjustSize();
    });
};

//==============================================================================

var Scroll = function (element, options) {
    var cls = arguments.callee;
    if (!(this instanceof cls)) {
        return new cls(element, options);
    }
    this.__init__(element, options);
};

Scroll.prototype = new MochiKit.Visual.Base();

MochiKit.Base.update(Scroll.prototype, {

    __init__: function (element, /* optional */options) {
        var b = MochiKit.Base;
        var s = MochiKit.Style;
        this.element = openobject.dom.get(element);

        options = b.update({
            side: "left",
            duration: 0.5
        }, options);

        this.start(options);
    },

    setup: function () {
        this.options.from = this.element.scrollLeft;
    },

    /** @id MochiKit.Visual.Opacity.prototype.update */
    update: function (position) {
        var prop = this.options.side == "left" ? "scrollLeft" : "scrollTop";
        this.element[prop] = parseInt(position, 10);
    }
});

// vim: ts=4 sts=4 sw=4 si et


