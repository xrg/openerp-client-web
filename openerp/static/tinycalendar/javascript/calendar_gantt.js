////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
//
// $Id$
//
// Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
//
// WARNING: This program as such is intended to be used by professional
// programmers who take the whole responsibility of assessing all potential
// consequences resulting from its eventual inadequacies and bugs
// End users who are looking for a ready-to-use solution with commercial
// guarantees and support are strongly advised to contract a Free Software
// Service Company
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
////////////////////////////////////////////////////////////////////////////////

var GanttCalendar = function(options){
    this.__init__(options);
}

GanttCalendar.prototype = {

    __init__ : function(options){

        this.options = MochiKit.Base.update({
        }, options || {});

        this.starts = MochiKit.DateTime.isoDate(getNodeAttribute('calGantt', 'dtStart'));
        this.range = parseInt(getNodeAttribute('calGantt', 'dtRange')) || 1;

        appendChildNodes('calBodySect', DIV({'id': 'calGrid', 'class': 'calGrid'}));

        this.events = {};

        var self = this;
        var events = getElementsByTagAndClassName('div', 'calEvent', 'calBodySect');
        forEach(events, function(e){
            var id = getNodeAttribute(e, 'nRecordID');
            self.events[id] = {
                dayspan : getNodeAttribute(e, 'nDaySpan'),
                starts : getNodeAttribute(e, 'dtStart'),
                ends : getNodeAttribute(e, 'dtEnd'),
                title : e.title,
                className: e.className,
                bg : e.style.backgroundColor,
                clr: e.style.color,
                text: MochiKit.DOM.scrapeText(e)
            };
        });

        this.header = new GanttCalendar.Header(this);
        this.grid = new GanttCalendar.DayGrid(this);

        this.attachSignals();

        // cache for bar & group elements
        this.barCache = {};
    },

    __delete__ : function(){
        this.dettachSignals();
        this.grid.__delete__();
    },

    attachSignals : function(){
        this.eventLoad = MochiKit.Signal.connect(window, 'onload', this, 'onResize');
        this.eventResize = MochiKit.Signal.connect(window, 'onresize', this, 'onResize');
    },

    dettachSignals : function(){
        MochiKit.Signal.disconnect(this.eventLoad);
        MochiKit.Signal.disconnect(this.eventResize);
    },

    onResize : function(evt){
        this.header.adjust();
        this.grid.adjust();
    }
}

GanttCalendar.Header = function(calendar){
    this.__init__(calendar);
}

GanttCalendar.Header.prototype = {

    __init__ : function(calendar){

        this.calendar = calendar;
        this.elements = [];

        var self = this;
        var days = getElementsByTagAndClassName('div', null, 'calHeaderSect');

        forEach(days, function(day){
            var div = DIV({'class' : 'calDayHeader', 'style' : 'position: absolute; top : 0pt;'}, MochiKit.DOM.scrapeText(day));
            self.elements = self.elements.concat(div);
            MochiKit.DOM.swapDOM(day, div);
        });
    },

    adjust : function(){

        var d = elementDimensions('calGrid');
        var n = this.elements.length;

        var w = (d.w - 2) / n;
        var h = d.h;

        for(var i=0; i < n; i++){

            var div = this.elements[i];
            var x = i * w;

            div.style.left = x + 'px';
            div.style.width = w + 'px';
            div.style.height = '100%';
        }
    }
}

GanttCalendar.DayGrid = function(calendar, dtStart){
    this.__init__(calendar);
}

GanttCalendar.DayGrid.prototype = {

    __init__ : function(calendar){

        this.calendar = calendar;
        this.starts = calendar.starts;
        this.range = calendar.range;

        this.columns = [];
        var headers = calendar.header.elements;
        for(var i = 0; i < headers.length; i++){
            this.columns.push(new GanttCalendar.Column(this.calendar));
        }

        this.groups = [];
        this.makeGroups();
    },

    __delete__ : function(){

        forEach(this.groups, function(g){
            g.__delete__();
        });
    },

    makeGroups : function(){

        var self = this;

        var events = getElementsByTagAndClassName('div', 'calEvent', 'calBodySect');
        forEach(events, function(e){
            MochiKit.DOM.removeElement(e);
        });

        var groups = getElementsByTagAndClassName('div', 'calGroup', 'calBodySect');
        forEach(groups, function(g){
            MochiKit.DOM.removeElement(g);
        });

        if (groups.length == 0) {
            groups = [DIV({'class': 'calGroup'})]; // dummy group
        }
        
        forEach(groups, function(g){
            self.groups = self.groups.concat(new GanttCalendar.Group(g, events, self.calendar));
        });
    },

    adjust : function(){
        
        var w = elementDimensions('calGrid').w / this.columns.length;

        for(var i = 0; i<this.columns.length; i++){

            var e = this.columns[i].element;

            e.style.position = 'absolute';

            e.style.top = '0px';
            e.style.left = i * w + 'px';

            e.style.width = w + 'px';
            e.style.height = '100%';

            this.columns[i].adjust();
        }

        var h = 0;

        forEach(this.groups, function(g){
            g.adjust();
            h += getElementDimensions(g.element).h;
        });

        var gh = getElementDimensions('calGrid').h;
        if (h > gh) {
            setElementDimensions('calGrid', {h: h});
        }
    }
}

// Grid Column
GanttCalendar.Column = function(calendar) {
    this.__init__(calendar);
}

GanttCalendar.Column.prototype = {

    __init__: function(calendar) {

        this.range = calendar.range;

        this.element = DIV({'class': 'calGanttCol'});
        MochiKit.DOM.appendChildNodes('calGrid', this.element);

        this.elements = [];

        // day mode
        if (this.range == 1) {
            for(j = 0; j < 2; j++) {
                var cell = DIV({'class': j % 2 == 0 ? 'calVRule even' : 'calVRule odd'});
                this.elements.push(cell);
                appendChildNodes(this.element, cell);
            }
        }

        // week mode
        else if (this.range == 7) {
            for(j = 0; j < 12; j++) {
                var cell = DIV({'class': j % 2 == 0 ? 'calVRule even' : 'calVRule odd'});
                this.elements.push(cell);
                appendChildNodes(this.element, cell);
            }
        }

        // other modes
        else {
            MochiKit.DOM.addElementClass(this.element, 'calVRule');
        }

    },

    adjust: function() {
        
        var w = getElementDimensions(this.element).w;
        w = w / this.elements.length;

        for(var i=0; i<this.elements.length; i++){
            var e = this.elements[i];

            e.style.width = w + 'px';
            e.style.left = i * w + 'px';
        }
    }
}

// Group
GanttCalendar.Group = function(elem, events, calendar) {
    this.__init__(elem, events, calendar);
}

GanttCalendar.Group.prototype = {

    __init__: function(elem, events, calendar){

        this.calendar = calendar;
        this.element = elem;
        
        this.id = MochiKit.DOM.getNodeAttribute(elem, 'nRecordID');
        this.model = MochiKit.DOM.getNodeAttribute(elem, 'model');
        this.title = MochiKit.DOM.getNodeAttribute(elem, 'title');
        this.items = MochiKit.DOM.getNodeAttribute(elem, 'items');

        if (this.items) {
            this.items = eval("(" + this.items + ")");
        }

        this.isDummy = !this.id;
        
        if (this.isDummy) {
            this.items = MochiKit.Base.map(function(e){
                return parseInt(MochiKit.DOM.getNodeAttribute(e, 'nRecordID'));
            }, events);
        }

        this.bar = this.isDummy ? null : DIV({'class': 'calEvent calBar'});
        this.events = [];

        var self = this;
        forEach(this.items, function(id){
            var evt = self.calendar.events[id];
            var div = DIV({
                    'nRecordID': id,
                    'dtStart': evt.starts,
                    'dtEnd': evt.ends,
                    'title': evt.title
                });

            div.className = evt.className;
            div.style.backgroundColor = evt.bg;

            self.events = self.events.concat(new GanttCalendar.Event(div, self));
        });

        /*
        this.events.sort(function(a, b){
            if (a.starts == b.starts) return 0;
            if (a.starts < b.starts) return -1;
            return 1;
        });
        */

        this.calculate_usages();

        MochiKit.DOM.appendChildNodes(this.element, this.bar, MochiKit.Base.map(function(e){
            return e.element;
        }, this.events));

        MochiKit.DOM.appendChildNodes('calGrid', this.element);
    },

    __delete__: function(){
        forEach(this.events, function(e){
            e.__delete__();
        });
    },

    calculate_usages: function() {

        this.bars = [];
        
        if (!this.events.length) {
            return;
        }

        var st = this.events[0].starts;
        var se = this.events[this.events.length-1].ends;

        var bounds = [];

        var self = this;
        forEach(this.events, function(e){
            if (MochiKit.Base.findValue(bounds, e.starts) == -1) {
                bounds.push(e.starts);
            }
            if (MochiKit.Base.findValue(bounds, e.ends) == -1) {
                bounds.push(e.ends);
            }
        });

        bounds.sort(function(a, b){
            if (a == b) return 0;
            if (a < b) return -1;
            return 1;
        });

        var periods = [];

        var cur = bounds.pop();
        while(bounds.length) {
            var last = bounds.pop();
            periods = periods.concat([[last, cur]]);
            cur = last;
        }

        periods.reverse();

        var divs = MochiKit.Base.map(function(b){
            var div = DIV({});
            div.starts = b[0];
            div.ends = b[1];
            div.style.position = "absolute";
            div.style.height = '100%';

            var n = 0;
            forEach(self.events, function(e){
                if ((div.starts >= e.starts && div.starts <= e.ends) &&
                    (div.ends <= e.ends && div.ends >= e.starts)) {
                    n += 1;
                }
            });
            
            div.style.backgroundColor = n == 1 ? "blue" : n > 1 ? "red" : "";

            return div;
        }, periods);

        appendChildNodes(this.bar, divs);
        this.bars = divs;
    },

    adjust: function(){

        var minutes = this.calendar.range * 24 * 60;
        var scale = getElementDimensions('calGrid').w / minutes;

        this.element.style.width = (getElementDimensions('calGrid').w - 2) + 'px';

        var bx = 0;
        var bw = 0;

        for(var i=0; i<this.events.length; i++){

            var e = this.events[i];
            var elem = e.element;

            var x = (e.starts.getTime() - this.calendar.starts.getTime()) / (60 * 1000);
            var w = (e.ends.getTime() - e.starts.getTime()) / (60 * 1000);

            x = x * scale;
            w = w * scale;

            elem.style.left = parseInt(x) + 'px';
            elem.style.width = parseInt(w) + 'px';

            bx = bx == 0 ? x : Math.min(x, bx);
            bw = bw == 0 ? w : Math.max(x - bx + w, bw);
        }

        bx = parseInt(bx);
        bw = parseInt(bw);

        if (this.bar) {
            this.bar.style.left = bx + 'px';
            this.bar.style.width = bw - 2 + 'px';
        }

        for(var i=0; i<this.bars.length; i++){
            var e = this.bars[i];
            var x = (e.starts.getTime() - this.events[0].starts.getTime()) / (60 * 1000);
            var w = (e.ends.getTime() - e.starts.getTime()) / (60 * 1000);
            x = x * scale;
            w = (w * scale) + 1;
            e.style.left = parseInt(x) + 'px';
            e.style.width = parseInt(w) + 'px';
        }
    }
}

// Event
GanttCalendar.Event = function(element, container){
    this.__init__(element, container);
}

GanttCalendar.Event.prototype = {

    __init__ : function(element, container){
        this.element = element;
        this.container = container;

        this.starts = isoTimestamp(getNodeAttribute(element, 'dtStart'));
        this.ends = isoTimestamp(getNodeAttribute(element, 'dtEnd'));
        this.dayspan = parseInt(getNodeAttribute(element, 'nDaySpan')) || 1;
        this.record_id = getNodeAttribute(element, 'nRecordID');

        this.evtClick = MochiKit.Signal.connect(this.element, 'onclick', this, this.onClick);
    },

    __delete__ : function() {
        MochiKit.Signal.disconnectAll(this.element);
    },

    onClick: function(evt) {
        if (!hasElementClass(this.element, 'dragging')){
            new InfoBox({
                dtStart : this.starts,
                dtEnd : this.ends,
                nRecordID: this.record_id,
                title: this.element.title,
                description: this.element.title
            }).show(evt);
        }
    },

    adjust : function(){
    }
}

// Zoom handler

var ganttZoomOut = function() {

    var mode = getElement('_terp_selected_mode').value;
    var modes = {
        'day': 'week',
        'week': 'month',
        'month': '3months',
        '3months': 'year'
    };

    return getCalendar(null, modes[mode]);
}

var ganttZoomIn = function() {

    var mode = getElement('_terp_selected_mode').value;
    var modes = {
        'year': '3months',
        '3months': 'month',
        'month': 'week',
        'week': 'day'
    };

    return getCalendar(null, modes[mode]);
}

// Tree event handlers

var onTreeExpand = function(tree, node) {

    if (!node.childNodes.length){
        return;
    }

    var barCache = CAL_INSTANCE.barCache;

    // create a cache of bar elements when tree gets expanded
    var key = 'gr' + node.name;
    if (!barCache[key]){
        var s = new MochiKit.Selector.Selector('div.calGroup[nRecordID='+node.name+']').findElements();
        if (s.length){
            var bar = s[0];
            barCache[key] = bar;
            bar.treeNode = node;
            MochiKit.Signal.connect(bar, 'onclick', onBarClick);
        }
    }

    forEach(node.childNodes, function(ch){
                    
        var id = ch.name;
        var key = 'ch'+id;
        var bar = barCache[key];

        if (!bar) {
            var s = new MochiKit.Selector.Selector('div.calEvent[nRecordID='+id+']').findElements();
            if (s.length){
                bar = s[0];
                barCache[key] = bar;
                bar.treeNode = ch;
                MochiKit.Signal.connect(bar, 'onclick', onBarClick);
            }
        }
        if (bar){
            MochiKit.Style.showElement(bar);
        }
    });
}

var onTreeCollapse = function(tree, node) {

    if (!node.childNodes.length){
        return;
    }

    var barCache = CAL_INSTANCE.barCache;

    forEach(node.childNodes, function(ch){
                    
        var key = 'ch'+ch.name;
        var bar = barCache[key];

        if (bar){
            MochiKit.Style.hideElement(bar);
        }

    });
}

var onTreeSelect = function(evt, node) {

    if (!node.name || !evt)
        return;

    var barCache = CAL_INSTANCE.barCache;

    var key = node.childNodes.length ? 'gr'+node.name : 'ch'+node.name;
    var bar = barCache[key];
                
    var hb = getElement('calBarHighlighter');
    if (!hb) {
        hb = DIV({});
        hb.style.position = 'absolute';
        hb.style.height = '14px';
        hb.style.width = '100%';
        hb.style.zIndex = 0;
        MochiKit.Style.setOpacity(hb, 0.50);
        appendChildNodes('calGrid', hb);
    }

    if (bar) {
        hb.style.top = getElementPosition(bar, 'calGrid').y + 'px';
        hb.style.height = getElementDimensions(bar).h + 'px';
        MochiKit.Visual.Highlight(hb, {startcolor: '#990000'});
    }
}

var onBarClick = function(evt){
    var e = evt.src();
    var t = evt.target();

    if (t.treeNode) {
        t.treeNode.onSelect();
    } else if (hasElementClass(e, 'calGroup') && t != e) {
        e.treeNode.onSelect();
    }

}

// vim: ts=4 sts=4 sw=4 si et

