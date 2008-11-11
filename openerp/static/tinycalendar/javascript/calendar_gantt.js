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
        this.scale = 0;

        this.events = {};
        this.makeEvents(); 

        this.header = new GanttCalendar.Header(this);
        this.grid = new GanttCalendar.DayGrid(this);

        this.attachSignals();
    },

    __delete__ : function(){
        this.dettachSignals();
        this.grid.__delete__();
    },

    attachSignals : function(){
        this.evtLoad = MochiKit.Signal.connect(window, 'onload', this, 'onResize');
        this.evtResize = MochiKit.Signal.connect(window, 'onresize', this, 'onResize');
        this.evtEventDrag = MochiKit.Signal.connect(MochiKit.DragAndDrop.Draggables, 'end', this, 'onEventDrag');
        this.evtEventResize = MochiKit.Signal.connect(MochiKit.DragAndDrop.Resizables, 'end', this, 'onEventResize');
    },

    dettachSignals : function(){
        MochiKit.Signal.disconnect(this.evtLoad);
        MochiKit.Signal.disconnect(this.evtResize);
        MochiKit.Signal.disconnect(this.evtEventDrag);
        MochiKit.Signal.disconnect(this.evtEventResize);
    },

    makeEvents: function() {
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
    },

    onResize : function(evt){
        this.scale = getElementDimensions('calGrid').w / (this.range * 24 * 60);

        this.header.adjust();
        this.grid.adjust();
    },

    onEventDrag: function(draggable, evt) {

        var element = draggable.element;

        var id = getNodeAttribute(element, 'nRecordID');
        var ds = MochiKit.DateTime.isoTimestamp(getNodeAttribute(element, 'dtStart'));
        var de = MochiKit.DateTime.isoTimestamp(getNodeAttribute(element, 'dtEnd'));

        var x = parseInt(element.style.left);
        var st = ((x / this.scale) * (60 * 1000)) + this.starts.getTime();

        st = new Date(st);

        var m = st.getMinutes();
        var s = st.getSeconds();

        if (this.range == 1) {
            m = m - m % 15;
            s = 0;
        } else if (this.range == 7) {
            m = 0;
            s = 0;
        } else {
            m = ds.getMinutes();
            s = ds.getSeconds();
        }

        st.setSeconds(s);
        st.setMinutes(m);

        var et = new Date(de.getTime() + st.getTime() - ds.getTime());

        var self = this;
        var req = saveCalendarRecord(id, toISOTimestamp(st), toISOTimestamp(et));
        
        req.addCallback(function(obj){
            
            if (obj.error) {
                return alert(obj.error);
            }
            
            setNodeAttribute(element, 'dtstart', toISOTimestamp(st));
            setNodeAttribute(element, 'dtend', toISOTimestamp(et));
            
            self.makeEvents();
            self.grid.makeGroups();
        });
        
        req.addBoth(function(obj){
            self.grid.adjust();
        });

    },

    onEventResize: function(resizable, evt) {
        var element = resizable.element;

        var id = getNodeAttribute(element, 'nRecordID');
        var ds = MochiKit.DateTime.isoTimestamp(getNodeAttribute(element, 'dtStart'));
        var de = MochiKit.DateTime.isoTimestamp(getNodeAttribute(element, 'dtEnd'));

        var x = parseInt(element.style.left) + parseInt(element.style.width);
        var se = ((x / this.scale) * (60 * 1000)) + this.starts.getTime();

        se = new Date(se);

        var m = se.getMinutes();
        var s = se.getSeconds();

        if (this.range == 1) {
            m = m - m % 15;
            s = 0;
        } else if (this.range == 7) {
            m = 0;
            s = 0;
        } else {
            m = ds.getMinutes();
            s = ds.getSeconds();
        }

        se.setSeconds(s);
        se.setMinutes(m);

        var self = this;
        var req = saveCalendarRecord(id, toISOTimestamp(ds), toISOTimestamp(se));
        
        req.addCallback(function(obj){
            
            if (obj.error) {
                return alert(obj.error);
            }

            setNodeAttribute(element, 'dtend', toISOTimestamp(se));
            
            self.makeEvents();
            self.grid.makeGroups();
        });
        
        req.addBoth(function(obj){
            self.grid.adjust();
        });
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

        var tbl = TABLE({'style': 'table-layout: fixed; width: 100%;'},
                    TBODY(null,
                        TR(null,
                            TD({'id' : 'calLabelCol', 'class': 'calLabelCol', 'valign': 'top', 'width': '70px'}),
                            TD({'id' : 'calGridCol', 'valign': 'top'}))));

        tbl.cellPadding = 0;
        tbl.cellSpacing = 0;

        appendChildNodes('calBodySect', tbl);
        appendChildNodes('calGridCol', DIV({'id': 'calGrid', 'class': 'calGrid'}));

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

        getElement('calLabelCol').innerHTML = "";

        // release the groups
        forEach(this.groups, function(g){
            g.__delete__();
        });
        this.groups = [];

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
            e.style.height = '900px';

            this.columns[i].adjust();
        }

        var h = 0;

        forEach(this.groups, function(g){
            g.adjust();
            h += getElementDimensions(g.element).h;
        });

        var gh = getElementDimensions('calBodySect').h - 2;
        setElementDimensions('calGrid', {h: h > gh ? h : gh});
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
                }, DIV({'class': 'calEventGrip2'}));

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

        // make labels
        if (!this.isDummy){
            appendChildNodes('calLabelCol', DIV({'class': 'calGroupLabel'}, this.title));
        }

        forEach(this.events, function(e){
            appendChildNodes('calLabelCol', DIV({'class': 'calEventLabel'}, e.element.title));
        });
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

        this.element.style.width = (getElementDimensions('calGrid').w - 2) + 'px';

        var bx = 0;
        var bw = 0;

        for(var i=0; i<this.events.length; i++){

            var e = this.events[i]; e.adjust();

            bx = bx == 0 ? e.left : Math.min(e.left, bx);
            bw = bw == 0 ? e.width : Math.max(e.left - bx + e.width, bw);
        }

        bx = Math.round(bx);
        bw = Math.round(bw);

        if (this.bar) {
            this.bar.style.left = bx + 'px';
            this.bar.style.width = bw - 2 + 'px';
        }

        for(var i=0; i<this.bars.length; i++){
            var e = this.bars[i];
            var x = (e.starts.getTime() - this.events[0].starts.getTime()) / (60 * 1000);
            var w = (e.ends.getTime() - e.starts.getTime()) / (60 * 1000);
            x = x * this.calendar.scale;
            w = (w * this.calendar.scale) + 1;
            e.style.left = Math.round(x) + 'px';
            e.style.width = Math.round(w) + 'px';
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

        this.evtClick = MochiKit.Signal.connect(this.element, 'ondblclick', this, this.onClick);
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

    doSnap: function(x, y) {

        var range = this.container.calendar.range;
        var scale = this.container.calendar.scale;

        var snap = 24 * 60 * scale; // default 1 day

        if (range == 1) {
            snap = 15 * scale; // 15 minutes
        } else if (range == 7) {
            snap = 60 * scale; // 1 hour
        }

        var x = Math.round(x/snap) * snap;
        
        return [x + 1, y];
    },

    adjust : function(){

        var x = (this.starts.getTime() - this.container.calendar.starts.getTime()) / (60 * 1000);
        var w = (this.ends.getTime() - this.starts.getTime()) / (60 * 1000);

        x = x * this.container.calendar.scale;
        w = w * this.container.calendar.scale;

        this.left = Math.round(x);
        this.width = Math.round(w);

        this.element.style.left = this.left + 'px';
        this.element.style.width = this.width + 'px';

        //XXX: safari hack
        if (!this.draggable){

            // make draggable
            this.draggable = new MochiKit.DragAndDrop.Draggable(this.element, {
                selectclass: 'dragging',
                snap: bind(this.doSnap, this),
                constraint: 'horizontal'
            });

            // make resizable
            this.resizable = new MochiKit.DragAndDrop.Resizable(this.element, {
                handle: 'calEventGrip2',
                selectclass: 'dragging',
                constraint: 'horizontal',
                snap: bind(this.doSnap, this)
            });
        }
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

// vim: ts=4 sts=4 sw=4 si et

