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

var WeekCalendar = function(options) {
    this.__init__(options);
};

WeekCalendar.prototype = {

    __init__ : function(options) {

        this.options = MochiKit.Base.update({

            // height of an hour row (in pixels)
            hourHeight : 40,

            // initial hour
            hourStarts : 8

        }, options || {});

        this.colWidth = 0; // width of a column
        this.colCount = 0; // number of columns
        this.colDays = []; // days

        this.header = new WeekCalendar.Header(this);
        this.allDayGrid = new WeekCalendar.AllDayGrid(this);
        this.dayGrid = new WeekCalendar.DayGrid(this);

        this.attachSignals();
    },

    __delete__ : function() {
        this.dettachSignals();
        this.allDayGrid.__delete__();
        this.dayGrid.__delete__();
    },

    attachSignals : function() {
        this.eventLoad = MochiKit.Signal.connect(window, 'onload', this, 'onResize');
        this.eventResize = MochiKit.Signal.connect(window, 'onresize', this, 'onResize');
        this.eventResizeEnd = MochiKit.Signal.connect(MochiKit.DragAndDrop.Resizables, 'end', this, 'onResizeEnd');
    },

    dettachSignals : function() {
        MochiKit.Signal.disconnect(this.eventLoad);
        MochiKit.Signal.disconnect(this.eventResize);
        MochiKit.Signal.disconnect(this.eventResizeEnd);
    },

    onResize : function(evt) {
        this.colWidth = Math.round(elementDimensions('calGridCol').w / this.colCount);
        this.colWidth = Math.max(0, this.colWidth);

        this.header.adjust();
        this.allDayGrid.adjust();
        this.dayGrid.adjust();

    },

    onResizeEnd : function(resizable, evt) {
        var element = resizable.element;

        if (!hasElementClass(element, 'calEvent')) return;

        var h = parseInt(element.style.height) + 2;
        var dt = MochiKit.DateTime.isoTimestamp(getNodeAttribute(element, 'dtStart'));
        var id = getNodeAttribute(element, 'nRecordID');

        e = dt.getTime() + h * (30 / 20) * (60 * 1000);
        e = new Date(e);

        var self = this;

        // check that the object was really modified to avoid unnecessary warning popups:
        var recordmoveinfo = getRecordMovability(element);
        if (recordmoveinfo.is_not_resizeable) {
            self.dayGrid.adjust();
            return error_display(_("This calendar object can no longer be resized !"));
        }

        var req = saveCalendarRecord(id, toISOTimestamp(dt), toISOTimestamp(e));

        req.addCallback(function(obj) {
            if (obj.error) {
                return error_display(obj.error);
            }

            setNodeAttribute(element, 'dtend', toISOTimestamp(e));
            self.dayGrid.makeEventContainers();
        });

        req.addBoth(function(obj) {
            self.dayGrid.adjust();
        });
    }
};

WeekCalendar.Header = function(calendar) {
    this.__init__(calendar);
};

WeekCalendar.Header.prototype = {

    __init__ : function(calendar) {

        this.calendar = calendar;
        this.elements = [];

        var self = this;
        var days = getElementsByTagAndClassName('div', null, 'calHeaderSect');
        forEach(days, function(day) {

            var div = DIV({'class' : 'calDayHeader', 'style' : 'position: absolute; top : 0pt;'},
                    MochiKit.DOM.A({'href': 'javascript: void(0)',
                        'onclick': "getCalendar('" + getNodeAttribute(day, 'dtDay') + "', 'day'); return false;"}, MochiKit.DOM.scrapeText(day)));

            self.elements = self.elements.concat(div);
            self.calendar.colDays = self.calendar.colDays.concat(getNodeAttribute(day, 'dtDay'));

            MochiKit.DOM.swapDOM(day, div);
        });

        this.calendar.colCount = days.length;
    },

    adjust : function() {

        var d = elementDimensions('calHeaderSect');

        var w = this.calendar.colWidth;
        var h = d.h;

        for (var i = 0; i < this.calendar.colCount; i++) {
            var div = this.elements[i];
            var x = i * w;

            div.style.left = x + 'px';
            div.style.width = w + 'px';
            div.style.height = '100%';
        }

    }
};

WeekCalendar.AllDayGrid = function(calendar) {
    this.__init__(calendar);
};

WeekCalendar.AllDayGrid.prototype = {

    __init__ : function(calendar) {

        this.calendar = calendar;
        this.elements = [];

        for (var i = 0; i < this.calendar.colCount; i++) {
            var dt = this.calendar.colDays[i];
            var div = DIV({'dtDay': dt, 'class': 'calVRule', 'style' : 'position: absolute; top: 0pt'});
            this.elements = this.elements.concat(div);
            appendChildNodes('calAllDaySect', div);
        }

        this.events = {};

        var self = this;
        var events = getElementsByTagAndClassName('div', 'calEvent', 'calAllDaySect');

        forEach(events, function(e) {
            var id = getNodeAttribute(e, 'nRecordID');

            self.events[id] = {
                dayspan : getNodeAttribute(e, 'nDaySpan'),
                starts : getNodeAttribute(e, 'dtStart'),
                ends : getNodeAttribute(e, 'dtEnd'),
                title : e.title,
                className: e.className,
                bg : e.style.backgroundColor,
                clr: e.style.color,
                text: MochiKit.DOM.scrapeText(e),
                create_date: getNodeAttribute(e, 'nCreationDate'),
                create_uid: getNodeAttribute(e, 'nCreationId'),
                write_date: getNodeAttribute(e, 'nWriteDate'),
                write_uid: getNodeAttribute(e, 'nWriteId')
            };

            MochiKit.DOM.removeElement(e);
        });

        this.eventCache = []; // cache of event objects

        // make events
        this.makeEvents();

        this.droppables = [];
        var self = this;

        // make all elements droppable
        forEach(this.elements, function(e) {
            var drop = new Droppable(e, {
                hoverclass: 'droppable',
                accept: ['allDay'],
                ondrop: bind(self.onDrop, self)
            });
            self.droppables.push(drop);
        });

        this.eventMouseDown = MochiKit.Signal.connect('calAllDaySect', 'onmousedown', this, 'onMouseDown');
        this.eventMouseUp = MochiKit.Signal.connect('calAllDaySect', 'onmouseup', this, 'onMouseUp');
    },

    __delete__ : function() {

        forEach(this.droppables, function(drop) {
            drop.destroy();
        });

        forEach(this.eventCache, function(evt) {
            evt.__delete__();
        });

        // calEventNew
        MochiKit.Signal.disconnect(this.eventMouseDown);
        MochiKit.Signal.disconnect(this.eventMouseUp);
    },

    onDrop : function(draggable, droppable, evt) {
        var dt = MochiKit.DateTime.isoDate(getNodeAttribute(droppable, 'dtDay'));
        var id = getNodeAttribute(draggable, 'nRecordID');

        var record = this.events[id];

        var s = MochiKit.DateTime.isoTimestamp(record.starts);
        var e = MochiKit.DateTime.isoTimestamp(record.ends);

        var t = s.getTime() - s.getHours() * (60 * 60 * 1000) - s.getMinutes() * (60 * 1000) - s.getSeconds() * 1000;

        s = s.getTime() + (dt.getTime() - t);
        e = e.getTime() + (dt.getTime() - t);

        s = toISOTimestamp(new Date(s));
        e = toISOTimestamp(new Date(e))

        var self = this;

        var recordmoveinfo = getRecordMovability(draggable);

        // check that the object was really modified to avoid unnecessary warning popups:
        if (recordmoveinfo.starts != s && recordmoveinfo.ends != e) {
            if (recordmoveinfo.is_not_movable) {
                self.adjust();
                return error_display(_("This calendar object can no longer be moved !"));
            } else {
                var req = saveCalendarRecord(id, s, e);

                req.addCallback(function(obj) {

                    if (obj.error) {
                        return error_display(obj.error);
                    }

                    record.starts = s;
                    record.ends = e;

                    self.makeEvents();
                });
                req.addBoth(function(obj) {
                    self.adjust();
                });
            }
        }
        self.adjust();
    },

    onMouseDown : function(evt) {
        if (!evt.mouse().button.left)
            return;

        var target = evt.target();
        if (!hasElementClass(target, 'calVRule'))
            return;

        var elem = openobject.dom.get('calEventNew');

        // set datetime info
        var dt = MochiKit.DateTime.isoDate(getNodeAttribute(target, 'dtDay'));
        var s = (9 * 40) * (30 / 20) * (60 * 1000);
        var e = (17 * 40) * (30 / 20) * (60 * 1000);

        s = dt.getTime() + s;
        e = dt.getTime() + e;

        s = new Date(s);
        e = new Date(e);

        setNodeAttribute(elem, 'dtstart', toISOTimestamp(s));
        setNodeAttribute(elem, 'dtend', toISOTimestamp(e));

    },

    onMouseUp : function(evt) {
        if (!evt.mouse().button.left)
            return;

        var target = evt.target();
        if (!hasElementClass(target, 'calVRule'))
            return;

        var elem = getElement('calEventNew');
        var dt = MochiKit.DateTime.isoTimestamp(getNodeAttribute(elem, 'dtStart'));

        editCalendarRecord(null);
    },

    splitEvent : function(record, params) {

        var ds = isoTimestamp(params.starts);
        var de = isoTimestamp(params.ends);
        var cdate = isoTimestamp(params.create_date);
        var wdate = isoTimestamp(params.write_date);

        var cuid = params.create_uid;
        var wuid = params.write_uid;
        var span = parseInt(params.dayspan) || 1;

        while (ds < isoDate(this.calendar.colDays[0])) {
            ds = ds.getNext();
            span -= 1;
        }

        span = Math.min(span, this.calendar.colCount);

        var div = DIV({
            nRecordID : record,
            dtStart : toISOTimestamp(ds),
            dtEnd : toISOTimestamp(de),
            nDaySpan: span,
            nCreationDate: toISOTimestamp(cdate),
            nCreationId: cuid,
            nWriteDate: toISOTimestamp(wdate),
            nWriteId: wuid
        }, params.text);

        div.className = params.className;
        div.title = params.title;

        with (div.style) {
            backgroundColor = params.bg;
            color = params.clr;
            borderColor = Color.fromString(params.bg).darkerColorWithLevel(0.2).toHexString();
            textShadow = "0 -1px 0 " + borderColor;
        }

        return [div];
    },

    makeEvents : function() {

        var self = this;
        var events = getElementsByTagAndClassName('div', 'calEvent', 'calAllDaySect');

        forEach(events, function(e) {
            removeElement(e);
        });

        events = [];
        forEach(items(this.events), function(e) {
            events = events.concat(self.splitEvent(e[0], e[1]));
        });

        appendChildNodes('calAllDaySect', events);

        this.makeEventContainers();
    },

    makeEventContainers : function() {

        var self = this;
        var containers = {};

        // release the cache
        forEach(this.eventCache, function(e) {
            e.__delete__();
        });
        this.eventCache = [];

        var events = getElementsByTagAndClassName('div', 'calEvent', 'calAllDaySect');

        for (var i = 0; i < this.calendar.colDays.length; i++) {

            var dt = this.calendar.colDays[i];

            containers[dt] = {
                index: i,                       // index of the container
                grid: this,                     // reference to the grid
                calendar: self.calendar,        // reference to the calendar
                events: [],                     // events in the day container
                rows: []                        // mark used rows
            }
        }

        forEach(events, function(e) {
            e.starts = isoTimestamp(getNodeAttribute(e, 'dtStart'));
            e.ends = isoTimestamp(getNodeAttribute(e, 'dtEnd'));
            e.dayspan = parseInt(getNodeAttribute(e, 'nDaySpan')) || 1;
        });

        events.sort(function(a, b) {
            if (a.dayspan > b.dayspan) return -1;
            if (a.starts == b.starts) return 0;
            if (a.starts < b.starts) return -1;
            return 1;
        });

        forEach(events, function(e) {
            var dt = toISODate(e.starts);
            var end_dt = toISODate(e.ends);
            if (!(dt in containers) || (end_dt < dt)){
                 e.style.display = 'none';
                 return;
            }

            var container = containers[dt];

            var evt = new WeekCalendar.AllDayEvent(e, container);
            container.events = container.events.concat(evt);
            self.eventCache = self.eventCache.concat(evt);
        });

        // adjust rows
        for (var i = 0; i < this.calendar.colCount; i++) {

            var dt = this.calendar.colDays[i];
            var container = containers[dt];

            forEach(container.events, function(evt) {

                if (evt.dayspan < 2) return;

                for (var j = i + 1; j < i + evt.dayspan; j++) {

                    if (j == self.calendar.colCount) break;

                    var dt = self.calendar.colDays[j];
                    var cnt = containers[dt];

                    forEach(cnt.events, function(e) {
                    	cnt.rows.push(evt.row);
                        e.row = e.row >= evt.row ? e.row + 1 : e.row;

                        while (cnt.rows.indexOf(e.row) > -1) {
                            e.row = e.row + 1;
                        }
                    });
                }
            });
        }

        // adjust grid height
        var rowcount = 0;
        for (var i = 0; i < this.calendar.colCount; i++) {
            var dt = this.calendar.colDays[i];
            var container = containers[dt];

            forEach(container.events, function(evt) {
                rowcount = rowcount < evt.row ? evt.row : rowcount;
            });
        }
        openobject.dom.get('calAllDaySect').style.height = ((rowcount + 1) * 15) + 15 + 'px';

        this.containers = containers;
    },

    adjust : function() {
        var w = this.calendar.colWidth;

        for (var i = 0; i < this.calendar.colCount; i++) {
            var div = this.elements[i];

            div.style.left = i * w + 'px';
            div.style.width = w + 'px';
            div.style.height = '100%';
        }

        for (var dt in this.containers) {
            var container = this.containers[dt];
            for (var i = 0; i < container.events.length; i++) {
                var evt = container.events[i];
                evt.adjust();
            }
        }
    }
};

WeekCalendar.DayGrid = function(calendar) {
    this.__init__(calendar);
};

WeekCalendar.DayGrid.prototype = {

    __init__ : function(calendar) {
        this.calendar = calendar;

        var tbl = TABLE({'style': 'table-layout: fixed; width: 100%;'},
                TBODY(null,
                        TR(null,
                                TD({'id' : 'calTimeCol', 'class': 'calTimeCol', 'valign': 'top', 'width': '70px'}),
                                TD({'id' : 'calGridCol', 'valign': 'top'}))));

        tbl.cellPadding = 0;
        tbl.cellSpacing = 0;

        appendChildNodes('calBodySect', tbl);

        for (var i = 0; i < 24; i++) {
            var h = i + ':00';

            appendChildNodes('calTimeCol', DIV(null, h));
        }

        this.grid = DIV({
            'id': 'calGrid',
            'class': 'calGrid',
            'style': 'position: relative;'
        });

        appendChildNodes('calGridCol', this.grid);

        for (j = 0; j < 48; j++) {

            var cls = j % 2 == 0 ? 'calHRule even' : 'calHRule odd';

            var cell = DIV({
                'class': cls
            });

            appendChildNodes(this.grid, cell);
        }

        this.eventCache = []; // cache of event objects
        this.elements = [];

        for (var i = 0; i < this.calendar.colCount; i++) {
            var dt = this.calendar.colDays[i];
            var div = DIV({'dtDay': dt, 'class': 'calVRule'});

            this.elements = this.elements.concat(div);

            appendChildNodes(this.grid, div);
        }

        // move events to the grid
        var events = getElementsByTagAndClassName('div', 'calEvent', 'calBodySect');
        appendChildNodes(this.grid, events);

        // make event containers
        this.makeEventContainers();

        // adjust right margins (accoring to the scrollbar size)
        var sw = (openobject.dom.get('calBodySect').offsetWidth - tbl.offsetWidth) || 17;

        sw = sw - 2;

        openobject.dom.get('calHeaderSect').style.marginRight = sw + 'px';
        openobject.dom.get('calAllDaySect').style.marginRight = sw + 'px';

        if (Browser.isIE7) {
            openobject.dom.get('calHeaderSect').style.marginRight = '16px';
            openobject.dom.get('calAllDaySect').style.marginRight = '16px';
            openobject.dom.get('calBodySect').style.paddingRight = '16px';
        }

        if (Browser.isIE6) {
            openobject.dom.get('calBodySect').style.marginRight = sw + 'px';
            openobject.dom.get('calBodySect').parentNode.style.paddingRight = '4px';
        }

        var st = this.calendar.options.hourStarts * this.calendar.options.hourHeight;

        // set initial scroll position
        window.setTimeout("openobject.dom.get('calBodySect').scrollTop=" + st, 0);

        this.droppables = [];
        var self = this;

        // make all elements droppable
        forEach(this.elements, function(e) {
            var drop = new Droppable(e, {
                accept: ['noAllDay'],
                ondrop: bind(self.onDrop, self)
            });
            self.droppables.push(drop);
        });

        //calEventNew
        this.eventMouseDown = MochiKit.Signal.connect(this.grid, 'onmousedown', this, 'onMouseDown');
        this.eventMouseUp = MochiKit.Signal.connect(this.grid, 'onmouseup', this, 'onMouseUp');

        var elem = DIV({'id': 'calEventNew', 'class': 'calEventNew', 'style': 'border-color: #696969; background-color: #C0C0C0; display: none;'},
                DIV({'class': 'calEventTitle', 'style' : 'height: 10px; background-color: #696969;'}, ''),
                DIV({'class': 'calEventDesc'}, ''),
                DIV({'class': 'calEventGrip'}));

        elem.style.position = 'absolute';
        appendChildNodes(this.grid, elem);

        // make resizable
        this.resizable = new MochiKit.DragAndDrop.Resizable(elem, {
            constraint: 'vertical',
            snap: 20
        });
    },

    __delete__ : function() {

        forEach(this.droppables, function(drop) {
            drop.destroy();
        });

        forEach(this.eventCache, function(evt) {
            evt.__delete__();
        });

        // calEventNew
        if (this.resizable) this.resizable.destroy();
        MochiKit.Signal.disconnect(this.eventMouseDown);
        MochiKit.Signal.disconnect(this.eventMouseUp);
    },

    onDrop : function(draggable, droppable, evt) {
        var dt = MochiKit.DateTime.isoDate(getNodeAttribute(droppable, 'dtDay'));
        var id = getNodeAttribute(draggable, 'nRecordID');


        var y = parseInt(draggable.style.top);
        var h = parseInt(draggable.style.height) + 2;

        var s = y * (30 / 20) * (60 * 1000);
        var e = (y + h) * (30 / 20) * (60 * 1000);

        s = dt.getTime() + s;
        e = dt.getTime() + e;

        s = new Date(s);
        e = new Date(e);

        var self = this;


        // check that the object was really modified to avoid unnecessary warning popups:
        var recordmoveinfo = getRecordMovability(draggable);
        if (recordmoveinfo.starts != toISOTimestamp(s) && recordmoveinfo.ends != toISOTimestamp(e)) {
            if (recordmoveinfo.is_not_movable) {
                self.adjust();
                return error_display(_("This calendar object can no longer be moved !"));
            }
        }

        var req = saveCalendarRecord(id, toISOTimestamp(s), toISOTimestamp(e));

        req.addCallback(function(obj) {

            if (obj.error) {
                return error_display(obj.error);
            }

            setNodeAttribute(draggable, 'dtstart', toISOTimestamp(s));
            setNodeAttribute(draggable, 'dtend', toISOTimestamp(e));

            self.makeEventContainers();

            // update the event title
            var title = getElementsByTagAndClassName('div', 'calEventTitle', draggable)[0];
            var t = strip(MochiKit.DOM.scrapeText(title));

            t = t.split(' - ');
            t.shift();
            t = t.join(' - ');

            title.innerHTML = s.strftime('%H:%M') + ' - ' + t;
        });

        req.addBoth(function(obj) {
            self.adjust();
        });

    },

    onMouseDown : function(evt) {
        if (!evt.mouse().button.left)
            return;

        var target = evt.target();
        if (!hasElementClass(target, 'calVRule'))
            return;

        var elem = openobject.dom.get('calEventNew');

        var x = getNodeAttribute(target, 'dtDay');

        x = this.containers[x].index * this.calendar.colWidth + 2;
        var y = evt.mouse().page.y - elementPosition(target).y;

        if (Browser.isOpera) {
            y = evt.mouse().page.y - elementPosition2(target).y + openobject.dom.get('calBodySect').scrollTop;
        }

        var w = this.calendar.colWidth;
        var h = 38;

        w = Math.max(w - 6, 0);

        y -= y % 20;

        elem.style.left = x + 'px';
        elem.style.top = y + 'px';
        elem.style.width = w + 'px';
        elem.style.height = h + 'px';

        // set datetime info
        var dt = MochiKit.DateTime.isoDate(getNodeAttribute(target, 'dtDay'));
        var s = y * (30 / 20) * (60 * 1000);
        var e = (y + 40) * (30 / 20) * (60 * 1000);

        s = dt.getTime() + s;
        e = dt.getTime() + e;

        s = new Date(s);
        e = new Date(e);

        setNodeAttribute(elem, 'dtstart', toISOTimestamp(s));
        setNodeAttribute(elem, 'dtend', toISOTimestamp(e));

        showElement('calEventNew');

        // initialise drag
        this.resizable.initDrag(evt);
    },

    onMouseUp : function(evt) {
        if (!evt.mouse().button.left)
            return;

        var elem = openobject.dom.get('calEventNew');
        if (!elem || elem.style.display == 'none') return;

        // set end time
        var h = parseInt(elem.style.height) + 2;
        var dt = MochiKit.DateTime.isoTimestamp(getNodeAttribute(elem, 'dtStart'));

        var e = dt.getTime() + h * (30 / 20) * (60 * 1000);
        e = new Date(e);

        setNodeAttribute(elem, 'dtend', toISOTimestamp(e));

        editCalendarRecord(null);

        hideElement('calEventNew');
    },

    makeEventContainers : function() {

        var self = this;
        var containers = {};

        // release the cache
        forEach(this.eventCache, function(e) {
            e.__delete__();
        });
        this.eventCache = [];

        var events = getElementsByTagAndClassName('div', 'calEvent', this.grid);

        for (var i = 0; i < this.calendar.colDays.length; i++) {

            var dt = this.calendar.colDays[i];

            containers[dt] = {
                index: i,                       // index of the container
                calendar: self.calendar,        // reference to the calendar
                columns : 1,                    // number of columns in container
                events: []                      // events in the day container
            }
        }

        forEach(events, function(e) {
            e.starts = isoTimestamp(getNodeAttribute(e, 'dtStart'));
            e.ends = isoTimestamp(getNodeAttribute(e, 'dtEnd'));
        });

        events.sort(function(a, b) {
            if (a.starts == b.starts) return 0;
            if (a.starts < b.starts) return -1;
            return 1;
        });

        // move events to the grid
        appendChildNodes(this.grid, events);

        forEach(events, function(e) {
            var dt = toISODate(e.starts);
            var container = containers[dt];
            if (!container) {
                //MochiKit.Logging.log('XXX', dt);
                return;
            }
            var evt = new WeekCalendar.DayEvent(e, container);
            container.events = container.events.concat(evt);

            self.eventCache = self.eventCache.concat(evt);
        });

        this.containers = containers;
    },

    adjust : function() {

        var w = this.calendar.colWidth;
        var h = this.calendar.options.hourHeight * 24;

        for (var i = 0; i < this.calendar.colCount; i++) {
            var div = this.elements[i];

            div.style.position = 'absolute';

            div.style.top = '0px';
            div.style.left = i * w + 'px';
            div.style.width = w + 'px';
            div.style.height = h + 'px';
        }

        for (var dt in this.containers) {
            var container = this.containers[dt];
            for (var i = 0; i < container.events.length; i++) {
                var evt = container.events[i];
                evt.adjust();
            }
        }
    }
};

WeekCalendar.AllDayEvent = function(element, container) {
    this.__init__(element, container);
};

WeekCalendar.AllDayEvent.prototype = {

    __init__ : function(element, container) {
        this.element = element;
        this.container = container;

        this.starts = element.starts; //isoTimestamp(getNodeAttribute(element, 'dtStart'));
        this.ends = element.ends; //isoTimestamp(getNodeAttribute(element, 'dtEnd'));

        this.record_id = getNodeAttribute(element, 'nRecordID');
        this.description = element.title;

        this.starts2 = container.grid.events[this.record_id].starts; // original start time
        this.starts2 = isoTimestamp(this.starts2);

        this.dayspan = parseInt(getNodeAttribute(element, 'nDaySpan')) || 1;
        this.row = container.events.length;

        this.draggable = false;

        this.eventMouseUp = MochiKit.Signal.connect(this.element, 'onmouseup', this, 'onClick');
    },

    __delete__ : function() {
        MochiKit.Signal.disconnect(this.eventMouseUp);
        if (this.draggable) this.draggable.destroy();
    },

    onClick : function(evt) {
        if (!hasElementClass(this.element, 'dragging')) {
            new InfoBox({
                dtStart : this.starts2,
                dtEnd : this.ends,
                nRecordID: this.record_id,
                title: MochiKit.DOM.scrapeText(this.element),
                description: this.description,
                event_id: jQuery(this.element).attr('nrecordid'),
                create_date: jQuery(this.element).attr('ncreationdate'),
                create_uid: jQuery(this.element).attr('ncreationid'),
                write_date: jQuery(this.element).attr('nwritedate'),
                write_uid: jQuery(this.element).attr('nwriteid')
            }).show(evt);
        }
    },

    adjust : function() {
    	var w;
		var dspan = this.dayspan;

		if (dspan == 1) {
			w =  elementDimensions('calGrid').w;
		} else {
        	w =  elementDimensions('calGrid').w / 7;
        }
        var x = this.container.index * this.container.calendar.colWidth;
        var h = elementDimensions(this.element).h + 1;
        var y = this.row * h;

        var d = elementDimensions('calAllDaySect');

        w = Math.floor(w) * this.dayspan - 4;

        x += 1;
        y += 1;

        w = Math.max(0, w);

        this.element.style.top = y + 'px';
        this.element.style.left = x + 'px';
        this.element.style.width = w + 'px';

        // XXX: safari hack
        if (!this.draggable) {
            // make draggalble
            this.draggable = new Draggable(this.element, {
                selectclass: 'dragging'
            });
        }
    }
};

WeekCalendar.DayEvent = function(element, container) {
    this.__init__(element, container);
};

WeekCalendar.DayEvent.prototype = {

    __init__ : function(element, container) {
        this.element = element;
        this.container = container;

        this.starts = element.starts; //isoTimestamp(getNodeAttribute(element, 'dtStart'));
        this.ends = element.ends; //isoTimestamp(getNodeAttribute(element, 'dtEnd'));

        this.record_id = getNodeAttribute(element, 'nRecordID');
        this.description = MochiKit.DOM.scrapeText(getElementsByTagAndClassName('div', 'calEventDesc', element)[0]);

        // set colors
        var color = Color.fromString(element.style.backgroundColor);
        var tl = getElementsByTagAndClassName('div', 'calEventTitle', element)[0];

        try{
            element.style.borderColor = color.darkerColorWithLevel(0.2).toHexString();
            element.style.textShadow = "0 -1px 0 " + element.style.borderColor;
            tl.style.textShadow = "0 1px 0 " + color.lighterColorWithLevel(0.2).toHexString();
        }catch(e){}

        this.title = MochiKit.DOM.scrapeText(tl);

        this.column = 0;        // in which column I'm placed
        this.expand = true;     // expand to entire container

        var collides = this.getCollidingEvents();

        if (collides.length + 1 > this.container.columns) {
            this.container.columns += 1;
        }

        if (collides.length > 0) {
            var available = [];

            for (var i = 0; i < this.container.columns; i++) {
                available.push(i);
            }

            for (var i = 0; i < collides.length; i++) {
                var evt = collides[i];

                // the colliding events must not fill the container
                evt.expand = false;

                var j = findValue(available, evt.column);
                available.splice(j, 1);
            }

            this.expand = false;
            this.column = available[0];

            // find the best column
            for (var i = 0; i < available.length; i++) {
                var c = available[i];
                this.column = c + 1 == evt.column ? c : this.column;
            }
        }

        this.draggable = null;
        this.resizable = null;

        this.eventMouseUp = MochiKit.Signal.connect(this.element, 'onmouseup', this, 'onClick');
    },

    __delete__ : function() {
        MochiKit.Signal.disconnect(this.eventMouseUp);
        if (this.draggable) this.draggable.destroy();
        if (this.resizable) this.resizable.destroy();
    },

    onClick : function(evt) {
        if (evt.mouse().button.left && !hasElementClass(this.element, 'dragging')) {
            new InfoBox({
                dtStart : this.starts,
                dtEnd : this.ends,
                nRecordID: this.record_id,
                title: this.title,
                description: this.description,
                event_id: jQuery(this.element).attr('nrecordid'),
                create_date: jQuery(this.element).attr('ncreationdate'),
                create_uid: jQuery(this.element).attr('ncreationid'),
                write_date: jQuery(this.element).attr('nwritedate'),
                write_uid: jQuery(this.element).attr('nwriteid')
            }).show(evt);
        }
    },

    doSnap : function(x, y) {

        var snap = [this.container.calendar.colWidth, 20];
        var bound = [0, 0, 0, 0];

        bound[2] = snap[0] * this.container.calendar.colCount - snap[0];
        bound[3] = elementDimensions('calGrid').h - elementDimensions(this.element).h;

        var p = [x, y];

        p[0] = Math.round(p[0] / snap[0]) * snap[0];
        p[1] = Math.round(p[1] / snap[1]) * snap[1];

        p[0] = Math.max(p[0], bound[0]);
        p[1] = Math.max(p[1], bound[1]);

        p[0] = Math.min(p[0], bound[2]);
        p[1] = Math.min(p[1], bound[3]);

        p[0] += 2;

        return p;
    },

    getCollidingEvents : function() {
        var events = [];

        for (var i = 0; i < this.container.events.length; i++) {
            var evt = this.container.events[i];

            if (evt == this) continue;

            // IMP: ignore seconds

            var ts = new Date(this.starts);
            var te = new Date(this.ends);

            var es = new Date(evt.starts);
            var ee = new Date(evt.ends);

            ts = ts.getTime() - ts.getSeconds() * 1000;
            te = te.getTime() - te.getSeconds() * 1000;

            es = es.getTime() - es.getSeconds() * 1000;
            ee = ee.getTime() - ee.getSeconds() * 1000;

            if (ts < ee && ts > es) {
                events = events.concat(evt);
            }

            if (ts == es) {
                events = events.concat(evt);
            }
        }

        return events;
    },

    adjust : function() {
        var w = this.container.calendar.colWidth;
        var h = ((this.ends.getTime() - this.starts.getTime()) / (60 * 1000)) / (30 / 20);

        var x = this.container.index * this.container.calendar.colWidth + 2;
        var y = ((this.starts.getHours() * 60) + this.starts.getMinutes()) / (30 / 20);

        w -= 2;
        w = this.expand ? w : w / this.container.columns;

        x = this.column == 0 ? x : x + (this.column * w);

        if (!this.expand && (Browser.isIE || Browser.isWebKit)) {
            w += 1;
        }

        this.element.style.top = y + 'px';
        this.element.style.left = x + 'px';

        w = Math.max(w - 2, 0);
        h = Math.max(h - 2, 0);

        this.element.style.width = w + 'px';
        this.element.style.height = h + 'px';

        //XXX: safari hack
        if (!this.draggable) {
            // make draggable
            this.draggable = new MochiKit.DragAndDrop.Draggable(this.element, {
                handle: 'calEventTitle',
                selectclass: 'dragging',
                snap: bind(this.doSnap, this)
            });

            // make resizable
            this.resizable = new MochiKit.DragAndDrop.Resizable(this.element, {
                handle: 'calEventGrip',
                selectclass: 'dragging',
                constraint: 'vertical',
                snap: 20
            });
        }
    }
};

// vim: ts=4 sts=4 sw=4 si et

