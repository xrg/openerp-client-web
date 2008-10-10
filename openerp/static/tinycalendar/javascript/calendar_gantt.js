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
        this.first = MochiKit.DateTime.isoDate(getNodeAttribute('calGantt', 'dtFirst'));
        this.firstWeek = this.first.getWeek(1);

        this.month = this.first.getMonth();

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
        var weeks = getElementsByTagAndClassName('div', null, 'calHeaderSect');

        forEach(weeks, function(week){
            var div = DIV({'class' : 'calDayHeader', 'style' : 'position: absolute; top : 0pt;'}, MochiKit.DOM.scrapeText(week));
            self.elements = self.elements.concat(div);
            MochiKit.DOM.swapDOM(week, div);
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

        this.eventCache = []; // cache of event objects
        this.elements = [];

        this.days = [];

        var dt = this.starts;
        for(var i = 0; i < 42; i++){

            this.days = this.days.concat(toISODate(dt));

            var md = DIV({'class': 'calGanttDay', 'dtDay' : toISODate(dt)});

            if (dt.getMonth() != this.calendar.first.getMonth()){
                addElementClass(md, 'dayOff');
            }

            var nw = new Date();

            if (dt.getFullYear() == nw.getFullYear() && dt.getMonth() == nw.getMonth() && dt.getDate() == nw.getDate()){
                addElementClass(md, 'dayThis');
            }

            this.elements = this.elements.concat(md);
            dt = dt.getNext();
        }

        appendChildNodes('calGrid', this.elements);

        this.droppables = [];
        var self = this;
    },

    __delete__ : function(){
    },

    adjust : function(){
        
        var w = elementDimensions('calGrid').w / 42;

        for(var i = 0; i < 42; i++){
            var e = this.elements[i];

            e.style.position = 'absolute';

            e.style.top = '0px';
            e.style.left = i * w + 'px';

            e.style.width = w + 'px';
            e.style.height = '100%';
        }
    }
}

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

// vim: ts=4 sts=4 sw=4 si et

