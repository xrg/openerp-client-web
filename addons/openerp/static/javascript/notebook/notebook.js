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
    if(!(this instanceof cls)) {
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

        if(!this.element) {
            throw "Invalid argument:" + element;
        }

        if(this.element.notebook) {
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
        MochiKit.Signal.disconnect(this.evtStripClick);
    },

    prepare: function() {
        this.rendered = false;

        this.elemStrip = UL({'class': 'notebook-tabs-strip'});
        this.elemStack = DIV({'class': 'notebook-pages'});

        this.cookie = '_notebook_' + this.element.id + '_active_page';

        this.tabs = [];
        this.pages = [];

        var pages = MochiKit.Base.filter(function(e) {
            return e.tagName == 'DIV';
        }, this.element.childNodes);


        for(var i = 0; i < pages.length; i++) {

            var page = pages[i];
            var text = page.title || "Page " + i;
            var id = page.id || 'none';

            var text_chunks = text.split('|');

            var help = text_chunks.length > 1 ? text_chunks[1] : "";
            var closable = this.options.closable;

            if(text_chunks.length > 2) {
                closable = parseInt(text_chunks[2], 10);
                closable = isNaN(closable) ? this.options.closable : closable;
            }

            this.add(page, {
                text: text_chunks[0],
                id: id,
                help: help,
                closable: closable,
                activate: false,
                css: page.className
            });
        }

        var tabs = DIV({'class': 'notebook-tabs'}, this.elemStrip);
        MochiKit.DOM.appendChildNodes(this.element, tabs, this.elemStack);

        MochiKit.DOM.addElementClass(this.element, 'notebook');

        this.evtStripClick = MochiKit.Signal.connect(this.elemStrip, 'onclick', this, this.onStripClick);
        this.rendered = true;

        var self = this;
        MochiKit.Async.callLater(0, function() {
            var i = self.options.remember ? getElement('_terp_notebook_tab').value || 0 : 0;
            self.show(parseInt(i));
        });

        showElement(this.element);
        var $tabs = jQuery(tabs);
        $tabs.scrollify();
        jQuery(window).bind('on-appcontent-resize', function () {
            $tabs.trigger('altered');
        });
    },

    getTab: function(tab) {

        if(typeof(tab) == "number") {
            if(tab >= this.tabs.length)
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
        } catch(e) {
        }
        return null;
    },

    getNext: function(tab) {
        tab = this.getTab(tab);
        var i = findIdentical(this.tabs, tab);

        for(var j = i + 1; j < this.tabs.length; j++) {
            var t = this.tabs[j];
            if(t.style.display == "none") {
                continue;
            }
            return t;
        }
        return null;
    },

    getPrev: function(tab) {
        tab = this.getTab(tab);
        var i = findIdentical(this.tabs, tab);

        for(var j = i - 1; j >= 0; j--) {
            var t = this.tabs[j];
            if(t.style.display == "none") {
                continue;
            }
            return t;
        }
        return null;
    },

    setClosable: function(tab, closable) {
        tab = this.getTab(tab);
        if(!tab) {
            return;
        }

        var prop = closable ? "addElementClass" : "removeElementClass";
        MochiKit.DOM[prop](tab, 'notebook-tab-closable');

        if(closable && !tab.elemClose) {
            tab.elemClose = SPAN({'href': 'javascript: void(0)', 'class': 'tab-close'});
            MochiKit.DOM.appendChildNodes(tab, tab.elemClose);
        } else if(!closable && tab.elemClose) {
            MochiKit.DOM.removeElement(tab.elemClose);
            tab.elemClose = null;
        }
    },

    add: function(content, options) {
        options = MochiKit.Base.update({
            text: "",                         // text of the tab
            id: "",                              // ID of tab for static menu
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
                SPAN({'href': 'javascript: void(0)', 'class': 'tab-title'},
                        SPAN(null, text)));

        if(typeof(options.css) == "string") {
            MochiKit.DOM.addElementClass(tab, options.css);
        }

        if(options.closable) {
            tab.elemClose = SPAN({'href': 'javascript: void(0)', 'class': 'tab-close'});
            MochiKit.DOM.appendChildNodes(tab, tab.elemClose);

            MochiKit.DOM.addElementClass(tab, 'notebook-tab-closable');
        }

        this.tabs = this.tabs.concat(tab);
        this.pages = this.pages.concat(page);

        MochiKit.DOM.appendChildNodes(this.elemStrip, tab);
        MochiKit.DOM.appendChildNodes(this.elemStack, page);

        this.show(tab, options.activate);
        jQuery('.notebook-tabs', this.element).trigger('altered');
    },

    remove: function(tab) {
        tab = this.getTab(tab);
        if(!tab) {
            return;
        }

        if(typeof(this.options.onclose) == "function" &&
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
        jQuery('.notebook-tabs', this.element).trigger('altered');
    },

    show: function(tab, activate) {
        tab = this.getTab(tab);
        activate = typeof(activate) == "undefined" ? true : activate;

        if(!tab || tab == this.activeTab) {
            return;
        }

        if(activate) {
            if(this.activeTab) {
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

        if(activate) {
            this.setActiveTab(tab);
        }
        jQuery('.notebook-tabs', this.element).trigger('altered');
    },

    hide: function(tab) {
        tab = this.getTab(tab);

        if(!tab) {
            return;
        }

        var i = findIdentical(this.tabs, tab);
        var t = null;

        if(tab == this.activeTab) {
            t = this.getNext(tab) || this.getPrev(tab);
        }

        tab.style.display = "none";

        MochiKit.Signal.signal(this, "hide", this, tab);

        if(t) {
            this.show(t);
        }
        jQuery('.notebook-tabs', this.element).trigger('altered');
    },

    setActiveTab: function(tab) {
        tab = this.getTab(tab);
        if(!tab) {
            return;
        }

        this.activeTab = tab;
        this.activePage = this.getPage(tab);

        if(this.options.remember) {
            openobject.dom.get('_terp_notebook_tab').value = findIdentical(this.tabs, tab);
        }

        MochiKit.Signal.signal(this, "activate", this, tab);
    },

    onStripClick: function(evt) {
        var tab = evt.target();
        var action = MochiKit.DOM.hasElementClass(tab, 'tab-close') ? 'remove' : 'show';

        tab = tab.tagName == "LI" ? tab : getFirstParentByTagAndClassName(evt.target(), 'li');

        if(tab) {
            this[action](tab)
        }

        if(tab && tab == this.activeTab) {
            this.setActiveTab(tab);
        }

        if(action == "show") {
            MochiKit.Signal.signal(this, 'click', this, tab);
        }
        jQuery('.notebook-tabs', this.element).trigger('altered');
    }
};
