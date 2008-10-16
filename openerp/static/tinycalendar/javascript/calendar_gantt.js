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

        var self = this;

        this.events = {};

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

            MochiKit.DOM.removeElement(e);
        });

        appendChildNodes('calBodySect', DIV({'id': 'calGrid', 'class': 'calGrid'}));

        this.header = new GanttCalendar.Header(this);
        this.grid = new GanttCalendar.DayGrid(this);

        this.attachSignals();
    },

    __delete__ : function(){
        this.dettachSignals();
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

        var d = elementDimensions('calHeaderSect');
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

        this.eventCache = []; // cache of event objects
        this.columns = [];

        var headers = calendar.header.elements;
        for(var i = 0; i < headers.length; i++){
            this.columns.push(new GanttCalendar.Column(this.calendar));
        }

    },

    __delete__ : function(){
    },

    adjust : function(){
        
        var w = elementDimensions('calGrid').w / this.columns.length;

        for(var i = 0; i < this.columns.length; i++){

            var e = this.columns[i].element;

            e.style.position = 'absolute';

            e.style.top = '0px';
            e.style.left = i * w + 'px';

            e.style.width = w + 'px';
            e.style.height = '100%';

            this.columns[i].adjust();
        }
    }
}

// Column
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
            for(j = 0; j < 48; j++) {
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

// Event
GanttCalendar.Event = function(element, container){
    this.__init__(element, container);
}

GanttCalendar.Event.prototype = {

    __init__ : function(element, container){
        this.element = element;
        this.container = container;
    },

    __delete__ : function() {
    },

    adjust : function(){
    }
}

var ganttZoomIn = function() {

    var mode = getElement('_terp_selected_mode').value;
    var modes = {
        'day': 'week',
        'week': 'month',
        'month': '3months',
        '3months': 'year'
    };

    return getCalendar(null, modes[mode]);
}

var ganttZoomOut = function() {

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

