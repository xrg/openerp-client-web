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

var MonthCalendar = function(options) {
    this.__init__(options);
};

MonthCalendar.prototype = {

    __init__ : function(options) {

        this.options = MochiKit.Base.update({
        }, options || {});

        this.starts = MochiKit.DateTime.isoDate(getNodeAttribute('calMonth', 'dtStart'));
        this.first = MochiKit.DateTime.isoDate(getNodeAttribute('calMonth', 'dtFirst'));


        this.month = this.first.getMonth();

        var self = this;

        this.events = {};

        var events = openobject.dom.select('div.calEvent', 'calBodySect');
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

        var tbl = TABLE({'style': 'table-layout: fixed; width: 100%;'},
                TBODY(null,
                        TR(null,
                                TD({'id' : 'calTimeCol', 'class': 'calTimeCol', 'valign': 'top', 'width': '35px'}),
                                TD({'id' : 'calGridCol', 'valign': 'top'}))));

        tbl.cellPadding = 0;
        tbl.cellSpacing = 0;

        appendChildNodes('calBodySect', tbl);
        appendChildNodes('calGridCol', DIV({'id': 'calGrid', 'class': 'calGrid'}));

        this.header = new MonthCalendar.Header(this);
        this.weeks = [];

        var dt = new Date(this.starts);
        var weekcount = dt.getWeek();
        for (var i = 0; i < 6; i++) {

            var week = new MonthCalendar.Week(this, dt);
            this.weeks = this.weeks.concat(week);

			for (var j = 0; j < 7; j ++) {
                if (weekcount >= 52){
					if (dt.getWeek() == 1){
						weekcount = 1;
					}
                }
                dt = dt.getNext();
            }

            var a = MochiKit.DOM.A({href: 'javascript: void(0)', onclick : "getCalendar('" + week.days[0] + "', 'week')"}, weekcount);
            appendChildNodes('calTimeCol', DIV({'style': 'height: 133px'}, a));

			weekcount= weekcount + 1;
        }

        //calEventNew
        var elem = DIV({'id': 'calEventNew', 'class': 'calEventNew', 'style': 'display: none;'});
        appendChildNodes('calGrid', elem);

        this.attachSignals();
        this.makeEvents();
    },

    __delete__ : function() {
        forEach(this.weeks, function(week) {
            week.__delete__();
        });

        this.dettachSignals();
    },

    attachSignals : function() {
        this.eventLoad = MochiKit.Signal.connect(window, 'onload', this, 'onResize');
        this.eventResize = MochiKit.Signal.connect(window, 'onresize', this, 'onResize');
        this.eventMouseUp = MochiKit.Signal.connect('calGrid', 'onmouseup', this, 'onMouseUp');
    },

    dettachSignals : function() {
        MochiKit.Signal.disconnect(this.eventLoad);
        MochiKit.Signal.disconnect(this.eventResize);
        MochiKit.Signal.disconnect(this.eventMouseUp);
    },

    onResize : function(evt) {
        this.header.adjust();
        forEach(this.weeks, function(week) {
            week.adjust();
        });
    },

    onMouseUp : function(evt) {
        if (!evt.mouse().button.left)
            return;

        var $target = jQuery(evt.target());
        if (!$target.hasClass('calMonthDay'))
            return;

        // set datetime info
        var selected_date = MochiKit.DateTime.isoDate($target.attr('dtDay'));

        // cloning date events in JS sucks.
        var default_start_datetime = new Date(selected_date.getTime());
        default_start_datetime.setHours(9);
        var default_end_datetime = new Date(selected_date.getTime());
        default_end_datetime.setHours(17);

        jQuery('#calEventNew').attr({
            dtstart: toISOTimestamp(default_start_datetime),
            dtend: toISOTimestamp(default_end_datetime)
        });

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
        var wd = ds.getWeekDay();
        var events = [];

		if (wd != 6){
			wd = wd + 1;
		} else {
			wd = 0 ;
		}

        while (span > 0) {
            var sp = span + wd > 7 ? 7 - wd : span;
            span -= sp;

            sp = span < 0 ? 7 + span : sp;

            var div = DIV({
                nRecordID : record,
                dtStart : toISOTimestamp(ds),
                dtEnd : toISOTimestamp(de),
                nDaySpan: sp,
                nCreationDate: toISOTimestamp(cdate),
                nCreationId: cuid,
                nWriteDate: toISOTimestamp(wdate),
                nWriteId: wuid
            }, params.text);

            div.className = params.className;
            div.title = params.title;

            div.style.position = 'absolute';
            div.style.backgroundColor = params.bg;
            div.style.color = params.clr;

            try{
                var bg = Color.fromString(div.style.backgroundColor).darkerColorWithLevel(0.2).toHexString();
                div.style.borderColor = bg;
                div.style.textShadow = "0 -1px 0 " + bg;
            }catch(e){}

            events = events.concat(div);

            ds = new Date(ds.getTime() + (7 - wd) * 24 * 60 * 60 * 1000);
            wd = 0;
        }

        return events;
    },

    makeEvents : function() {

        var getWeekIndex = function(dt) {
            // get the first day of the week and return the week number
            while (dt.getWeekDay() < 6) {
                dt = dt.getPrevious();
            }
            return dt.getWeek();
        }

        var self = this;
        var events = openobject.dom.select('div.calEvent', 'calBodySect');

        forEach(events, function(e) {
            removeElement(e);
        });

        events = [];
        forEach(items(this.events), function(e) {
            events = events.concat(self.splitEvent(e[0], e[1]));
        });

        appendChildNodes('calGrid', events);

        var weeks = {};
        forEach(this.weeks, function(w) {
            weeks[getWeekIndex(w.starts)] = [];
        });

        forEach(events, function(e) {
            var starts = isoTimestamp(getNodeAttribute(e, 'dtStart'));
            if (getWeekIndex(starts) in weeks) {
                weeks[getWeekIndex(starts)] = weeks[getWeekIndex(starts)].concat(e);
            }
        });

        forEach(this.weeks, function(w) {
            w.events = weeks[getWeekIndex(w.starts)];
            w.makeEventContainers();
        });
    }
};

MonthCalendar.Header = function(calendar) {
    this.__init__(calendar);
};

MonthCalendar.Header.prototype = {

    __init__ : function(calendar) {

        this.calendar = calendar;
        this.elements = [];

        var self = this;
        var days = openobject.dom.select('div', 'calHeaderSect');
        forEach(days, function(day) {
            var div = DIV({'class' : 'calDayHeader', 'style' : 'position: absolute; top : 0pt;'}, MochiKit.DOM.scrapeText(day));
            self.elements = self.elements.concat(div);
            MochiKit.DOM.swapDOM(day, div);
        });
    },

    adjust : function() {

        var d = elementDimensions('calHeaderSect');

        var w = Math.floor(d.w / 7);
        var h = d.h;

        for (var i = 0; i < 7; i++) {
            var div = this.elements[i];
            var x = i * w;

            div.style.left = x + 'px';
            div.style.width = w + 'px';
            div.style.height = '100%';
        }

    }
};

MonthCalendar.Week = function(calendar, dtStart) {
    this.__init__(calendar, dtStart);
};

MonthCalendar.Week.prototype = {

    __init__ : function(calendar, dtStart) {
        this.calendar = calendar;
        this.starts = dtStart;

        var div = DIV({'class': 'calMonthWeek'});
        appendChildNodes('calGrid', div);

        this.eventCache = []; // cache of event objects
        this.elements = [];

        this.containers = {};
        this.events = [];
        this.days = [];

        var dt = new Date(dtStart);
        for (var i = 0; i < 7; i++) {

            this.days = this.days.concat(toISODate(dt));

            var md = DIV({'class': 'calMonthDay', 'dtDay' : toISODate(dt)},
                    DIV({'class':'calMonthDayTitle'},
                            MochiKit.DOM.A({'href':'javascript: void(0)',
                                'onclick': "getCalendar('" + toISODate(dt) + "', 'day')"}, dt.getDate())));

            if (dt.getMonth() != this.calendar.first.getMonth()) {
                addElementClass(md, 'dayOff');
            }

            var nw = new Date();

            if (dt.getFullYear() == nw.getFullYear() && dt.getMonth() == nw.getMonth() && dt.getDate() == nw.getDate()) {
                addElementClass(md, 'dayThis');
            }

            this.elements = this.elements.concat(md);
            dt = dt.getNext();
        }

        appendChildNodes(div, this.elements);

        this.droppables = [];
        var self = this;

        // make all elements droppable
        forEach(this.elements, function(e) {
            var drop = new Droppable(e, {
                hoverclass: 'droppable',
                accept: ['calEvent'],
                ondrop: bind(self.onDrop, self)
            });
            self.droppables.push(drop);
        });

    },

    __delete__ : function() {

        forEach(this.droppables, function(drop) {
            drop.destroy();
        });

        forEach(this.eventCache, function(evt) {
            evt.__delete__();
        });
    },

    onDrop : function(draggable, droppable, evt) {

        var dt = MochiKit.DateTime.isoDate(getNodeAttribute(droppable, 'dtDay'));
        var id = getNodeAttribute(draggable, 'nRecordID');

        var record = this.calendar.events[id];

        var s = MochiKit.DateTime.isoTimestamp(record.starts);
        var e = MochiKit.DateTime.isoTimestamp(record.ends);

        var t = s.getTime() - s.getHours() * (60 * 60 * 1000) - s.getMinutes() * (60 * 1000) - s.getSeconds() * 1000;

        s = s.getTime() + (dt.getTime() - t);
        e = e.getTime() + (dt.getTime() - t);

        s = toISOTimestamp(new Date(s));
        e = toISOTimestamp(new Date(e))

        var self = this;

        // check that the object was really modified to avoid unnecessary warning popups:
        var recordmoveinfo = getRecordMovability(draggable);
        if (recordmoveinfo.starts != s && recordmoveinfo.ends != e) {
            if (recordmoveinfo.is_not_movable){
                self.calendar.onResize();
                return error_display(_("This calendar object can no longer be moved !"));
            } else {
                var req = saveCalendarRecord(id, s, e);

                req.addCallback(function(obj) {

                    if (obj.error) {
                        return error_display(obj.error);
                    }

                    record.starts = s;
                    record.ends = e;

                    self.calendar.makeEvents();
                });
                req.addBoth(function(obj) {
                    self.calendar.onResize();
                });
            }
        }
        self.calendar.onResize();
    },

    makeEventContainers : function() {

        var self = this;
        var containers = {};

        // release the cache
        forEach(this.eventCache, function(e) {
            e.__delete__();
        });
        this.eventCache = [];

        var events = this.events;

        for (var i = 0; i < 7; i++) {

            var dt = this.days[i];

            containers[dt] = {
                index: i,                       // index of the container
                week: self,                     // reference it this week
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

        // sort events, allDay events should always be first
        e1 = filter(function(e) {
            return !hasElementClass(e, 'calEventInfo');
        }, events);

        e2 = filter(function(e) {
            return hasElementClass(e, 'calEventInfo');
        }, events);

        e1.sort(function(a, b) {
            if (a.dayspan > b.dayspan) return -1;
            if (a.starts == b.starts) return 0;
            if (a.starts < b.starts) return -1;
            return 1;
        });

        e2.sort(function(a, b) {
            if (a.starts == b.starts) return 0;
            if (a.starts < b.starts) return -1;
            return 1;
        });

        events = e1.concat(e2);

        forEach(events, function(e) {
            var dt = toISODate(e.starts);
            var container = containers[dt];
            if (!container) {
                //MochiKit.Logging.log('XXX', dt);
                return;
            }
            var evt = new MonthCalendar.Event(e, container);
            container.events = container.events.concat(evt);
            self.eventCache = self.eventCache.concat(evt);
        });

        // adjust rows
        for (var i = 0; i < 7; i++) {

            var dt = this.days[i];
            var container = containers[dt];
            var element = this.elements[i];

            forEach(container.events, function(evt) {

                if (evt.dayspan < 2) return;

                for (var j = i + 1; j < i + evt.dayspan; j++) {

                    if (j == 7) break;

                    var d = self.days[j];
                    var cnt = containers[d];

                    forEach(cnt.events, function(e) {
                        cnt.rows.push(evt.row);
                        e.row = e.row >= evt.row ? e.row + 1 : e.row;

                        while (cnt.rows.indexOf(e.row) > -1) {
                            e.row = e.row + 1;
                        }
                    });
                }
            });

            // add `+ (n) more...`

            forEach(openobject.dom.select('div.calEventInfo', element), function(e) {
                removeElement(e);
            });

            if (container.events.length > 0) {
                e = container.events[container.events.length - 1];
                if (e.row > 5) {
                    appendChildNodes(element, DIV({'class': 'calEventInfo'},
                            MochiKit.DOM.A({'href':'javascript: void(0)',
                               'onclick': "getCalendar('" + dt + "', 'day')"},
                               '+ (' + (e.row - 5) + ') more...')));
                }
            }
        }

        this.containers = containers;
    },

    adjust : function() {
        var w = elementDimensions('calGrid').w / 7;

        w = Math.floor(w);

        for (var i = 0; i < 7; i++) {
            var e = this.elements[i];

            e.style.position = 'absolute';

            e.style.top = '0px';
            e.style.left = i * w + 'px';

            e.style.width = w + 'px';
            e.style.height = '134px';
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

MonthCalendar.Event = function(element, container) {
    this.__init__(element, container);
};

MonthCalendar.Event.prototype = {

    __init__ : function(element, container) {
        this.element = element;
        this.container = container;

        this.starts = element.starts; //isoTimestamp(getNodeAttribute(element, 'dtStart'));
        this.ends = element.ends; //isoTimestamp(getNodeAttribute(element, 'dtEnd'));

        this.record_id = getNodeAttribute(element, 'nRecordID');
        this.description = element.title;

        this.starts2 = this.container.calendar.events[this.record_id].starts; // original start time
        this.starts2 = isoTimestamp(this.starts2);

        this.dayspan = parseInt(getNodeAttribute(element, 'nDaySpan')) || 1;
        this.row = container.events.length;

        this.draggable = null;
        this.eventMouseUp = MochiKit.Signal.connect(this.element, 'onmouseup', this, 'onClick');
    },

    __delete__ : function() {
        MochiKit.Signal.disconnect(this.eventMouseUp);
        if (this.draggable) this.draggable.destroy();
    },

    onClick : function(evt) {
        if (evt.mouse().button.left && !hasElementClass(this.element, 'dragging')) {
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

        if (this.row > 5) {
            hideElement(this.element);
            return;
        }

        var elements = this.container.week.elements;
        var e = elements[this.container.index];

        var x = elementPosition(e, 'calGrid').x;
        var y = elementPosition(e, 'calGrid').y + 16;

        var w = elementDimensions('calGrid').w / 7;
        var h = elementDimensions(this.element).h + 1;

        y += this.row * h;

        w = Math.floor(w);
        w = w * this.dayspan - 6;
        y += 2;

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

// vim: ts=4 sts=4 sw=4 si et

