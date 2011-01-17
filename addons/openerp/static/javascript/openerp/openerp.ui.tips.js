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

// Based on Tips.js of Mootools (http://mootools.net) which is again based on 
// Bubble Tooltips (http://web-graphics.com/mtarchive/001717.php) 
// by Alessandro Fulcitiniti (http://web-graphics.com)

var openerp;
if (!openerp && !openerp.ui) {
    throw "openerp.ui is required by openerp.ui.tips.";
}
openerp.ui.Tips = function(elements, options) {
    this.__init__(elements, options);
};

openerp.ui.Tips.prototype = {

    __init__ : function(elements, options) {
        jQuery('.tooltip').remove();

        this.options = MochiKit.Base.update({
            wait: 1,            // wait for n seconds
            maxTitleChars: 255  // number of chars in title
        }, options || {});

        this.deferred = null;
        this.elements = elements;

        this.toolTitle = SPAN({'class': 'tipTitle'});
        this.toolText = P({'class': 'tipText'});
        this.toolModel = SPAN({'class': 'tipExtra'});
        this.toolField = SPAN({'class': 'tipExtra'});
        this. modelTitle = SPAN({'style': 'font-weight:bold;'}, _('Object')+' :: ')
        this.fieldTitle = SPAN({'style': 'font-weight:bold;'}, _('Field')+' :: ')
        this.toolTip = TABLE({'class': 'tooltip'},
                        TBODY(null,
                            TR(null,
                                TD({'class': 'tip-text'}, 
                                    this.toolTitle, this.toolText),
                                TD({'class': 'tip-r'})),
                            TR(null,
                                TD({'class': 'tipExtra'},
                                    this. modelTitle, this.toolModel, this.fieldTitle, this.toolField))                                
                            ));
                                
                            
        this.toolTip.cellPadding = 0;
        this.toolTip.cellSpacing = 0;
    
        MochiKit.DOM.appendChildNodes(document.body, this.toolTip);

        MochiKit.Iter.forEach(elements, function(el) {
        
            el = openobject.dom.get(el);
            el.myText = MochiKit.DOM.getNodeAttribute(el, 'title');
            el.tipModel = MochiKit.DOM.getNodeAttribute(el, 'model');
            el.tipField = MochiKit.DOM.getNodeAttribute(el, 'fname');

            if (el.myText)
                el.removeAttribute('title');
                el.removeAttribute('model');
                el.removeAttribute('fname');
            //if (el.href){
            //    if (el.href.indexOf('http://') > -1) el.myTitle = el.href.replace('http://', '');
            //    if (el.href.length > this.options.maxTitleChars) el.myTitle = el.href.substr(0,this.options.maxTitleChars-3)+"...";
            //}
        
            if (el.myText && el.myText.indexOf('::') > -1) {
                var dual = el.myText.split('::');
                el.myTitle = MochiKit.Format.strip(dual[0]);
                el.myText = MochiKit.Format.strip(dual[1]);
            }
        
          MochiKit.Signal.connect(el, 'onmouseover', this, this.showLater);
          MochiKit.Signal.connect(el, 'onmouseout', this, this.hide);

        }, this);
    },

    showLater: function(evt) {
        
        var e = evt.src();
        var x = evt.mouse().client.x;
        var y = evt.mouse().client.y;

        this.deferred = MochiKit.Async.callLater(this.options.wait, MochiKit.Base.bind(this.show, this), e, x, y);
    },

    show: function(el, x, y) {

        var text = el.myText;
        var title = el.myTitle;
        var model = el.tipModel || ''
        var fieldname = el.tipField || ''

        // if plain text then replace \n with <br>
        if (! /<\w+/.test(text)) {
            text = text.replace(/\n|\r/g, '<br/>');
        }
        
        title = text ? title : '';

        this.toolTitle.innerHTML = title;
        this.toolModel.innerHTML = model;
        this.toolField.innerHTML = fieldname;

        if (/msie/.test(navigator.userAgent.toLowerCase())) { // hack for strange IE error
            var div = document.createElement('div');
            div.innerHTML = text ? text : el.myTitle;
            this.toolText.innerHTML = '';        
            MochiKit.DOM.appendChildNodes(this.toolText, div.childNodes);
        } else {
            this.toolText.innerHTML = text ? text : el.myTitle;
        }
        
        this.toolTitle.style.display = title ? 'block' : 'none';
        
        if (browser.isIE) {
            this.toolTip.style.display = 'block';
        } else {
            MochiKit.Visual.appear(this.toolTip, {duration: 0.5, from: 0});
        }

        // adjust position

        var doc = document.documentElement;
        var body = document.body;

        var ps = MochiKit.Style.getElementPosition(el);
        var vd = MochiKit.DOM.getViewportDimensions();
        var md = MochiKit.Style.getElementDimensions(this.toolTip);

        var x = x + (doc.scrollLeft || body.scrollLeft) - 30;
        var y = y + (doc.scrollTop || body.scrollTop) + 15;

        if ((x + md.w) > vd.w - 30) {
            x -= x + md.w - vd.w;
            x -= 20;
        }

        this.toolTip.style.top = y + 'px';
        this.toolTip.style.left = x + 'px';
    },

    hide: function() {
        if (this.deferred) {
            this.deferred.cancel();
        }
        if (browser.isIE) {
            this.toolTip.style.display = 'none';
        } else {
            MochiKit.Visual.fade(this.toolTip, {duration: 0.2, queue: 'end'});
        }
    }
};

function setup_tips(){

    if (window.browser.isOpera){
        return;
    }
    var elements = MochiKit.Base.filter(function(e){
        var text = MochiKit.DOM.getNodeAttribute(e, 'title');
        var model = MochiKit.DOM.getNodeAttribute(e, 'model');
        var fname = MochiKit.DOM.getNodeAttribute(e, 'fname') || '';
        var fieldname = fname && fname.indexOf('/') == -1 ? fname : fname.split(/[/ ]+/).pop();
        if(!text)
            text = '';
            
        if (!model)
            return false;

        var title;
        var search_table = jQuery(e).find('.search_table');
        if(search_table.length) {
            title = jQuery(search_table).find('td:first span').text().split(":")[0];
        } else {
            title = MochiKit.DOM.scrapeText(e).replace(/^\s*\?\s*|\s*:\s*$/g, '');
        }

        MochiKit.DOM.setNodeAttribute(e, 'title', title + '::' + text);
        MochiKit.DOM.setNodeAttribute(e, 'model', model);
        MochiKit.DOM.setNodeAttribute(e, 'fname', fieldname);
        return true;

    }, openobject.dom.select('td.label', document));
    if (elements.length) {
        new openerp.ui.Tips(elements);
    }
}
jQuery(document).ready(setup_tips);
jQuery(document).ajaxStop(setup_tips);
