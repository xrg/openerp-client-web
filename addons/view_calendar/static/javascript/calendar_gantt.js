/**
 * GanttCalendar
 */
var GanttCalendar = function(options) {
    this.__init__(options);
};

GanttCalendar._ZOOM_SCALE = {
    'day': 30,
    '3days': 15,
    'week': 24,
    '3weeks': 12 * 7,
    'month': 6 * 7,
    '3months': 12,
    'year': 6,
    '3years': 150,
    '5years': 200
};

GanttCalendar.prototype = {

    __init__: function(options) {

        this.options = MochiKit.Base.update({

        }, options || {});

        this.starts = MochiKit.DateTime.isoDate(getNodeAttribute('calGantt', 'dtStart'));

        this.mode = openobject.dom.get('_terp_selected_mode').value;
        this.range = parseInt(getNodeAttribute('calGantt', 'dtRange')) || 7;

        this.scale = 0;
        this.header = new GanttCalendar.Header(this);

        this.events = {};
        this.groups = {};

        this._makeEvents();

        MochiKit.DOM.removeElement('calBodySect');

        var tbl = TABLE(null,
                TBODY(null,
                        TR(null,
                                TD({'width': 200, 'nowrap': 'nowrap'}),
                                TD({}, DIV({'id': 'calHeaderC'}, this.header.elements))),
                        TR(null,
                                TD({'width': 200, 'nowrap': 'nowrap'}, DIV({'id': 'calListC'})),
                                TD({}, DIV({'id': 'calGridC'})))));

        tbl.cellPadding = 0;
        tbl.cellSpacing = 0;

        tbl.style.width = '100%';
        tbl.style.height = '100%';

        MochiKit.DOM.appendChildNodes('calGantt', tbl);

        this.grid = new GanttCalendar.Grid(this);
        this.list = new GanttCalendar.List(this);

        this.gc = openobject.dom.get('calGridC');
        this.hc = openobject.dom.get('calHeaderC');
        this.lc = openobject.dom.get('calListC');

        this.attachSignals();

    },

    __delete__: function() {
        this.dettachSignals();
        this.grid.__delete__();
        this.list.__delete__();
        this.header.__delete__();
    },

    attachSignals: function() {
        this.evtLoad = MochiKit.Signal.connect(window, 'onload', this, 'onResize');
        this.evtResize = MochiKit.Signal.connect(window, 'onresize', this, 'onResize');
        this.evtScrollGrid = MochiKit.Signal.connect('calGridC', 'onscroll', this, 'onScrollGrid');
        this.evtMouseUp = MochiKit.Signal.connect('calGrid', 'onmouseup', this, 'onMouseUp');
        this.evtEventDrag = MochiKit.Signal.connect(MochiKit.DragAndDrop.Draggables, 'drag', this, 'onEventDrag');
        this.evtEventDragged = MochiKit.Signal.connect(MochiKit.DragAndDrop.Draggables, 'end', this, 'onEventDragged');
        this.evtEventResized = MochiKit.Signal.connect(MochiKit.DragAndDrop.Resizables, 'end', this, 'onEventResized');
    },

    dettachSignals: function() {
        MochiKit.Signal.disconnect(this.evtLoad);
        MochiKit.Signal.disconnect(this.evtResize);
        MochiKit.Signal.disconnect(this.evtScrollGrid);

        MochiKit.Signal.disconnect(this.evtEventDrag);
        MochiKit.Signal.disconnect(this.evtEventDragged);
        MochiKit.Signal.disconnect(this.evtEventResized);
    },

    onResize: function(evt) {

        var h1 = getElementDimensions('calGroupC').h;
        var h2 = openobject.dom.get('calGridC').clientHeight;

        setElementDimensions('calList', {h: h1 > h2 ? h1 : h2});
        setElementDimensions('calGrid', {h: h1 > h2 ? h1 : h2});
    },

    onMouseUp: function(evt) {
        if (!evt.mouse().button.left)
            return;

        editCalendarRecord(null, null);
    },

    onScrollGrid: function(evt) {
        this.lc.scrollTop = this.gc.scrollTop;
        this.hc.scrollLeft = this.gc.scrollLeft;
    },

    _makeEvents: function() {

        this.events = {};
        this.groups = {};

        var events = openobject.dom.select('div.calEvent', 'calGantt') || [];
        var groups = openobject.dom.select('div.calGroup', 'calGantt') || [];

        for (var i = 0; i < events.length; i++) {

            var elem = events[i];
            var id = MochiKit.DOM.getNodeAttribute(elem, 'nRecordID');

            var bg = MochiKit.Color.Color.fromBackground(elem);
            this.events[id] = {
                'dayspan': MochiKit.DOM.getNodeAttribute(elem, 'nDaySpan'),
                'starts': MochiKit.DOM.getNodeAttribute(elem, 'dtStart'),
                'ends': MochiKit.DOM.getNodeAttribute(elem, 'dtEnd'),
                'title': elem.title,
                'className': elem.className,
                'bg': bg.lighterColorWithLevel(0.2).toHexString(),
                'clr': elem.style.color,
                'text': MochiKit.DOM.scrapeText(elem),
                'create_date': MochiKit.DOM.getNodeAttribute(elem, 'nCreationDate'),
                'create_uid': MochiKit.DOM.getNodeAttribute(elem, 'nCreationId'),
                'write_date': MochiKit.DOM.getNodeAttribute(elem, 'nWriteDate'),
                'write_uid': MochiKit.DOM.getNodeAttribute(elem, 'nWriteId')
            };

            MochiKit.DOM.removeElement(elem);
        }

        for (var i = 0; i < groups.length; i++) {

            var elem = groups[i];
            var id = MochiKit.DOM.getNodeAttribute(elem, 'nRecordID');
            var items = MochiKit.DOM.getNodeAttribute(elem, 'items');

            if (items) {
                items = eval("(" + items + ")");
            }

            this.groups[id] = {
                'title': elem.title,
                'model': MochiKit.DOM.getNodeAttribute(elem, 'model'),
                'items': items
            };

            MochiKit.DOM.removeElement(elem);
        }

    },

    computeDates: function(element) {

        var ds = MochiKit.DateTime.isoTimestamp(getNodeAttribute(element, 'dtStart'));
        var de = MochiKit.DateTime.isoTimestamp(getNodeAttribute(element, 'dtEnd'));

        var x = parseInt(element.style.left);
        var st = ((x / this.scale) * (60 * 1000)) + this.starts.getTime();

        st = new Date(st);

        var m = st.getMinutes();
        var s = st.getSeconds();

        if (this.mode == 'day') {
            m = m - m % 15;
            s = 0;
        } else if (this.mode == '3days') {
            m = m - m % 30;
            s = 0;
        } else if (this.mode == 'week') {
            m = 0;
            s = 0;
        } else if (this.mode == '3weeks') {
            m = 0;
            s = 0;
        } else {
            m = ds.getMinutes();
            s = ds.getSeconds();
        }

        st.setSeconds(s);
        st.setMinutes(m);

        var et = new Date(de.getTime() + st.getTime() - ds.getTime());

        return {'starts': st, 'ends': et};
    },

    onEventDrag: function(draggable, evt) {

        var element = draggable.element;

        if (hasElementClass(element, 'calEventLabel')) {
            return;
        }

        var dt = this.computeDates(element);

        var pos = getElementPosition(element, 'calGrid');
        var dim = getElementDimensions(element);

        with (this.sTip) {
            style.display = "";
            style.top = pos.y + 'px';
            style.right = getElementDimensions('calGrid').w - pos.x + 2 + 'px';
            innerHTML = dt.starts.strftime('%Y-%m-%d %H:%M');
        }

        with (this.eTip) {
            style.display = "";
            style.top = pos.y + 'px';
            style.left = pos.x + dim.w + 2 + 'px';
            innerHTML = dt.ends.strftime('%Y-%m-%d %H:%M');
        }
    },

    onEventDragged: function(draggable, evt) {

        var element = draggable.element;

        if (hasElementClass(element, 'calEventLabel')) {
            return this.list.onUpdate(draggable, evt);
        }

        hideElement(this.sTip);
        hideElement(this.eTip);

        var id = getNodeAttribute(element, 'nRecordID');
        var dt = this.computeDates(element);

        var self = this;

        var recordmoveinfo = getRecordMovability(element);
        if (recordmoveinfo.starts != toISOTimestamp(dt.starts) && recordmoveinfo.ends != toISOTimestamp(dt.ends)) {
            if (recordmoveinfo.is_not_movable) {
                self.grid.adjust();
                return error_display(_("This calendar object can no longer be moved !"));
            } else {
                var req = saveCalendarRecord(id, toISOTimestamp(dt.starts), toISOTimestamp(dt.ends));

                req.addCallback(function(obj) {

                    if (obj.error) {
                        self.grid.adjust();
                        return error_display(obj.error);
                    }

                    self.events[id].starts = toISOTimestamp(dt.starts);
                    self.events[id].ends = toISOTimestamp(dt.ends);

                    setNodeAttribute(element, 'dtstart', toISOTimestamp(dt.starts));
                    setNodeAttribute(element, 'dtend', toISOTimestamp(dt.ends));
                    self.grid.adjust();
                });
            }
        }
    },

    onEventResized: function(resizable, evt) {
        var element = resizable.element;

        var id = getNodeAttribute(element, 'nRecordID');
        var ds = MochiKit.DateTime.isoTimestamp(getNodeAttribute(element, 'dtStart'));
        var de = MochiKit.DateTime.isoTimestamp(getNodeAttribute(element, 'dtEnd'));

        var x = parseInt(element.style.left) + parseInt(element.style.width);
        var se = ((x / this.scale) * (60 * 1000)) + this.starts.getTime();

        se = new Date(se);

        var m = se.getMinutes();
        var s = se.getSeconds();

        if (this.mode == 'day') {
            m = m - m % 15;
            s = 0;
        } else if (this.mode == '3days') {
            m = m - m % 30;
            s = 0;
        } else if (this.mode == 'week') {
            m = 0;
            s = 0;
        } else if (this.mode == '3weeks') {
            m = 0;
            s = 0;
        } else {
            m = ds.getMinutes();
            s = ds.getSeconds();
        }

        se.setSeconds(s);
        se.setMinutes(m);

        var self = this;

        var recordmoveinfo = getRecordMovability(element);
        if (recordmoveinfo.is_not_resizeable) {
            self.grid.adjust();
            return error_display(_("This calendar object can no longer be resized !"));
        } else {
            var req = saveCalendarRecord(id, toISOTimestamp(ds), toISOTimestamp(se));

            req.addCallback(function(obj) {

                if (obj.error) {
                    self.grid.adjust();
                    return error_display(obj.error);
                }

                self.events[id].ends = toISOTimestamp(se);
                setNodeAttribute(element, 'dtend', toISOTimestamp(se));
                self.grid.adjust();
            });
        }
    }
};

/**
 * GanttCalendar.Header
 */
GanttCalendar.Header = function(calendar) {
    this.__init__(calendar);
};

GanttCalendar.Header.prototype = {

    __init__: function(calendar) {

        var titles = openobject.dom.select('div.calTitle', 'calHeaderSect');
        var subtitles = openobject.dom.select('div.calSubTitle', 'calHeaderSect');

        MochiKit.DOM.removeElement('calHeaderSect');

        this.calendar = calendar;

        // subcolumn specs
        this.specs = [];

        // subcolumn width
        var mode = calendar.mode;
        var scw = GanttCalendar._ZOOM_SCALE[mode];

        var scale = 0;
        var divs = [];
        var subs = [];

        for (var i = 0; i < titles.length; i++) {

            var spec = {
                'count': parseInt(getNodeAttribute(titles[i], 'nCount')),
                'width': scw
            };
            this.specs = this.specs.concat(spec);

            var w = spec.count * spec.width;
            var div = DIV({'class': 'calTitle'}, MochiKit.DOM.scrapeText(titles[i]));
            MochiKit.Style.setStyle(div, {
                'position': 'absolute',
                'width': w + 'px',
                'left': scale + 'px',
                'top': '0px'
            });

            scale += w;
            divs = divs.concat(div);
        }

        var w = scale / subtitles.length;

        for (var i = 0; i < subtitles.length; i++) {
            var _div = DIV({'class': 'calSubTitle'}, MochiKit.DOM.scrapeText(subtitles[i]));
            MochiKit.Style.setStyle(_div, {
                'position': 'absolute',
                'width': w + 'px',
                'left': i * w + 'px',
                'top': '0px'
            });

            subs = subs.concat(_div);
        }

        this.calendar.scale = scale / (this.calendar.range * 24 * 60);

        this.count = divs.length;
        this.elements = [DIV({'class': 'calHeader'}, divs), DIV({'class': 'calHeader'}, subs)];
    },


    __delete__: function() {
    },

    adjust: function() {
    }
};

/**
 * GanttCalendar.List
 */
GanttCalendar.List = function(calendar) {
    this.__init__(calendar);
};

GanttCalendar.List.prototype = {

    __init__: function(calendar) {
        this.calendar = calendar;

        this._signals = [];

        var elements = [];
        var groups = this.calendar.grid.groups;
        var self = this;

        this._get_status();

        forEach(groups, function(group) {

            var elem = DIV({'class': 'calListGroup'});

            var div = DIV({'class': 'calGroupLabel'}, SPAN({}, group.title));

            var e = MochiKit.Signal.connect(div, 'onclick', self, partial(self.onToggle, elem, group));
            MochiKit.DOM.appendChildNodes(elem, div);
            self._signals.push(e);

            // keep the reference of the associated Group object
            elem.__group = group;

            forEach(group.events, function(evt) {
                var div = DIV({'class': 'calEventLabel'}, evt.title);
                var e = MochiKit.Signal.connect(div, 'ondblclick', self, partial(self.onClick, evt));
                MochiKit.DOM.appendChildNodes(elem, div);
                self._signals.push(e);

                // keep the reference of the associated Event object
                div.__event = evt;
            });

            elements = elements.concat(elem);
            self.onToggle(elem, group);
        });

        appendChildNodes('calListC', DIV({'id': 'calList'}, elements));

        //XXX: MochiKit bug #140 (http://trac.mochikit.com/ticket/140)
        MochiKit.Position.includeScrollOffsets = true;

        forEach(elements, function(elem) {
            MochiKit.Sortable.Sortable.create(elem, {
                'tag': 'div',
                'only': ['calEventLabel'],
                'containment': elements
            });
        });
    },

    __delete__: function() {
        forEach(this._signals, function(s) {
            MochiKit.Signal.disconnect(s);
        });
    },

    _get_status: function() {
        this.stat = {};

        var s = openobject.http.getCookie('terp_gantt_status') || '';
        try {
            this.stat = eval('({' + s + '})');
        } catch(e) {
        }
    },

    _set_status: function() {
        var s = [];
        for (var k in this.stat) {
            s.push("'" + k + "':" + this.stat[k]);
        }
        openobject.http.setCookie('terp_gantt_status', s.join(','));
    },

    onToggle: function(element, group, evt) {
        var key = openobject.dom.get('_terp_model').value + '-' + group.model + '-' + group.id;

        var visible = this.stat[key];
        visible = typeof(visible) == "undefined" ? 1 : visible;

        var toggle = jQuery(element).find('span.toggle-button');
        var n = 0;
        if (!toggle.length) {
            jQuery(element).find('div.calGroupLabel > span').before('<span class="toggle-button">- </span>');
            n = 1;
        }

        if (visible) {
            jQuery(element).find('span.toggle-button').replaceWith('<span class="toggle-button">- </span>')
        } else if (n == 0) {
            jQuery(element).find('span.toggle-button').replaceWith('<span class="toggle-button">+ </span>')
        }

        var divs = openobject.dom.select('div.calEventLabel', element);

        forEach(divs, function(div) {
            div.style.display = evt ? (visible ? '' : 'none') : (visible ? 'none' : '');
        });

        forEach(group.events, function(e) {
            e.element.style.display = evt ? (visible ? '' : 'none') : (visible ? 'none' : '');
        });

        if (evt) {
            this.stat[key] = visible ? 0 : 1;
            this._set_status();
        }
    },

    onClick: function(task, evt) {
        task.onClick(evt);
    },

    onUpdate: function(draggable, evt) {

        var group = draggable.element.parentNode.__group;
        var event = draggable.element.__event;

        var items = openobject.dom.select('div.calEventLabel', 'calListC');
        items = MochiKit.Base.map(function(item) {
            return item.__event.record_id;
        }, items);

        var params = {
            '_terp_id': event.record_id,
            '_terp_ids': '[' + items.join(',') + ']',
            '_terp_model': openobject.dom.get('_terp_model').value,
            '_terp_level': openobject.dom.get('_terp_gantt_level').value,
            '_terp_level_value': group.id
        };

        var self = this;
        var req = openobject.http.postJSON('/view_calendar/calendar/gantt_reorder', params);
        req.addCallback(function(obj) {
            if (obj.error) {
                return error_display(obj.error);
            }
        });

        req.addBoth(function(obj) {
            return getCalendar();
        });
    }
};

/**
 * GanttCalendar.Grid
 */
GanttCalendar.Grid = function(calendar) {
    this.__init__(calendar);
};

GanttCalendar.Grid.prototype = {

    __init__: function(calendar) {

        this.calendar = calendar;
        this.starts = calendar.starts;

        this._makeGrid();
        this._makeGroups();

        this.adjust();
    },

    __delete__: function() {

    },

    _makeGrid: function() {

        this.columns = [];

        var divs = [];
        for (var i = 0, left = 0; i < this.calendar.header.count; i++) {

            var spec = this.calendar.header.specs[i];
            var col = new GanttCalendar.GridColumn(this.calendar, spec);
            var div = col.element;

            div.style.left = left + 'px';

            this.columns = this.columns.concat(col);
            divs = divs.concat(div);

            left += col.width;
        }

        this.element = DIV({'id': 'calGrid', 'class': 'calGrid'}, divs, DIV({'id': 'calGroupC'}));
        MochiKit.DOM.appendChildNodes('calGridC', this.element);

        // start/end time tips
        this.calendar.sTip = DIV({'style': 'position: absolute; font-size: 10px; white-space: nowrap;'});
        this.calendar.eTip = DIV({'style': 'position: absolute; font-size: 10px; white-space: nowrap;'});
        MochiKit.DOM.appendChildNodes(this.element, this.calendar.sTip, this.calendar.eTip);
    },

    _makeGroups : function() {

        this.groups = this.groups || [];

        // release the groups
        forEach(this.groups, function(g) {
            g.__delete__();
        });
        this.groups = [];

        for (var id in this.calendar.groups) {
            this.groups = this.groups.concat(new GanttCalendar.GridGroup(id, this.calendar));
        }
    },

    adjust: function() {

        var left = null;
        forEach(this.groups, function(g) {
            g.adjust();
            var x = parseInt(g.bar.style.left) || 0;
            left = left == null ? x : Math.min(left, x);
        });

        // adjust horizontal scrollbar
        openobject.dom.get('calGridC').scrollLeft = left - 50;
    }
};

/**
 * GanttCalendar.GridColumn
 */
GanttCalendar.GridColumn = function(calendar, spec) {
    this.__init__(calendar, spec);
};

GanttCalendar.GridColumn.prototype = {

    __init__: function(calendar, spec) {

        this.calendar = calendar;
        this.spec = spec;

        this.width = spec.count * spec.width;

        this.element = DIV({'class': 'calColumn'});
        this.elements = [];

        for (var i = 0; i < spec.count; i++) {

            var div = DIV({'class': i % 2 == 0 ? 'calVRule even' : 'calVRule odd'});
            MochiKit.Style.setStyle(div, {
                'position': 'absolute',
                'width': spec.width + 'px',
                'left': spec.width * i + 'px',
                'top': '0px'
            });
            this.elements.push(div);
        }

        MochiKit.DOM.appendChildNodes(this.element, this.elements);
    }
};

/**
 * GanttCalendar.GridGroup
 */
GanttCalendar.GridGroup = function(id, calendar) {
    this.__init__(id, calendar);
};

GanttCalendar.GridGroup.prototype = {

    __init__: function(id, calendar) {
        this.calendar = calendar;

        var group = calendar.groups[id];
        var events = calendar.events;

        this.id = id;
        this.title = group.title;
        this.model = group.model;
        this.items = group.items || [];

        this.element = DIV({'class': 'calGroup'});

        this.bar = DIV({'class': 'calEvent calBar'});
        this.events = [];
        var self = this;
        forEach(this.items, function(id) {
            var evt = events[id];

            var div = DIV({
                'nRecordID': id,
                'dtStart': evt.starts,
                'dtEnd': evt.ends,
                'title': evt.title,
                'nCreationDate': evt.create_date,
                'nCreationId': evt.create_uid,
                'nWriteDate': evt.write_date,
                'nWriteId': evt.write_id
            }, DIV({'class': 'calEventGrip2'}));

            div.className = evt.className;
            div.style.backgroundColor = evt.bg;

            try{
                var bg = Color.fromString(div.style.backgroundColor).darkerColorWithLevel(0.2).toHexString();
                div.style.borderColor = bg;
            }catch(e){}

            self.events = self.events.concat(new GanttCalendar.Event(div, self));
        });

        MochiKit.DOM.appendChildNodes(this.element, this.bar, MochiKit.Base.map(function(e) {
            return e.element;
        }, this.events));

        if (this.events.length) {
            MochiKit.DOM.appendChildNodes('calGroupC', this.element);
        }
    },

    __delete__: function() {
        forEach(this.events, function(e) {
            e.__delete__();
        });
    },

    calculate_usages: function() {

        this.bars = [];

        if (!this.events.length) {
            return;
        }

        // clear the bar
        MochiKit.DOM.replaceChildNodes(this.bar);

        // copy events
        var events = Array.prototype.slice.call(this.events);

        // sort them by start time
        events.sort(function(a, b) {
            if (a.starts == b.starts) return 0;
            if (a.starts < b.starts) return -1;
            return 1;
        });

        // prepare usages bar

        var st = events[0].starts;
        var se = events[events.length - 1].ends;

        var bounds = [];

        var self = this;
        forEach(events, function(e) {
            if (MochiKit.Base.findValue(bounds, e.starts) == -1) {
                bounds.push(e.starts);
            }
            if (MochiKit.Base.findValue(bounds, e.ends) == -1) {
                bounds.push(e.ends);
            }
        });

        bounds.sort(function(a, b) {
            if (a == b) return 0;
            if (a < b) return -1;
            return 1;
        });

        var periods = [];

        var cur = bounds.shift();
        while (bounds.length) {
            var last = bounds.shift();
            periods = periods.concat([
                [cur, last]
            ]);
            cur = last;
        }

        var divs = MochiKit.Base.map(function(b) {
            var div = DIV({});
            div.starts = b[0];
            div.ends = b[1];
            div.style.position = "absolute";
            div.style.height = '100%';

            var n = 0;
            forEach(events, function(e) {
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

        // adjust usages bar

        var bx = null;
        var bw = null;

        for (var i = 0; i < events.length; i++) {

            var e = events[i];

            bx = bx == null ? e.left : Math.min(e.left, bx);
            bw = bw == null ? e.width : Math.max(e.left - bx + e.width, bw);
        }

        bx = Math.round(bx || 0);
        bw = Math.round(bw || 0);

        if (this.bar) {
            this.bar.style.left = bx + 'px';
            this.bar.style.width = bw - 2 + 'px';
        }

        for (var i = 0; i < this.bars.length; i++) {
            var e = this.bars[i];
            var x = (e.starts.getTime() - events[0].starts.getTime()) / (60 * 1000);
            var w = (e.ends.getTime() - e.starts.getTime()) / (60 * 1000);
            x = x * this.calendar.scale;
            w = (w * this.calendar.scale) + 1;
            e.style.left = Math.round(x) + 'px';
            e.style.width = Math.round(w) + 'px';
        }
    },

    adjust: function() {

        forEach(this.events, function(e) {
            e.adjust();
        });

        var w = 0;

        forEach(this.calendar.header.specs, function(spec) {
            w += spec.count * spec.width;
        });

        this.element.style.width = w + 'px';
        this.calculate_usages();
    }
};

/**
 * GanttCalendar.Event
 */
GanttCalendar.Event = function(element, container) {
    this.__init__(element, container);
};

GanttCalendar.Event.prototype = {

    __init__: function(element, container) {
        this.element = element;
        this.container = container;
        this.starts = isoTimestamp(getNodeAttribute(element, 'dtStart'));
        this.ends = isoTimestamp(getNodeAttribute(element, 'dtEnd'));
        this.dayspan = parseInt(getNodeAttribute(element, 'nDaySpan')) || 1;
        this.record_id = getNodeAttribute(element, 'nRecordID');
        this.title = element.title;

        this.adjust();

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

        this.evtClick = MochiKit.Signal.connect(this.element, 'onmouseup', this, this.onClick);
    },

    __delete__ : function() {
        MochiKit.Signal.disconnectAll(this.element);
    },

    adjust: function() {

        this.starts = isoTimestamp(getNodeAttribute(this.element, 'dtStart'));
        this.ends = isoTimestamp(getNodeAttribute(this.element, 'dtEnd'));
        this.dayspan = parseInt(getNodeAttribute(this.element, 'nDaySpan')) || 1;

        var x = (this.starts.getTime() - this.container.calendar.starts.getTime()) / (60 * 1000);
        var w = (this.ends.getTime() - this.starts.getTime()) / (60 * 1000);

        x = x * this.container.calendar.scale;
        w = w * this.container.calendar.scale;

        this.left = Math.round(x);
        this.width = Math.round(w);

        this.element.style.left = this.left + 'px';
        this.element.style.width = this.width + 'px';
    },

    onClick: function(evt) {
        if (!hasElementClass(this.element, 'dragging')) {
            new InfoBox({
                dtStart : this.starts,
                dtEnd : this.ends,
                nRecordID: this.record_id,
                title: this.element.title,
                description: this.element.title,
                event_id: jQuery(this.element).attr('nrecordid'),
                create_date: jQuery(this.element).attr('ncreationdate'),
                create_uid: jQuery(this.element).attr('ncreationid'),
                write_date: jQuery(this.element).attr('nwritedate'),
                write_uid: jQuery(this.element).attr('nwriteid')
            }).show(evt);
        }
    },

    doSnap: function(x, y) {

        var mode = this.container.calendar.mode;
        var scale = this.container.calendar.scale;

        var snap = 24 * 60 * scale; // default 1 day

        if (mode == 'day') {
            snap = 15 * scale; // 15 minutes
        } else if (mode == '3days') {
            snap = 30 * scale; // 30 minutes
        } else if (mode == 'week') {
            snap = 60 * scale; // 1 hour
        }

        var x = Math.round(x / snap) * snap;

        return [x + 1, y];
    }
};

// Zoom handlers

var ganttZoomOut = function() {

    var mode = openobject.dom.get('_terp_selected_mode').value;
    var modes = {
        'day': '3days',
        '3days': 'week',
        'week': '3weeks',
        '3weeks': 'month',
        'month': '3months',
        '3months': 'year',
        'year': '3years',
        '3years': '5years'
    };

    return getCalendar(null, modes[mode]);
};

var ganttZoomIn = function() {

    var mode = openobject.dom.get('_terp_selected_mode').value;
    var modes = {
        '5years': '3years',
        '3years': 'year',
        'year': '3months',
        '3months': 'month',
        'month': '3weeks',
        '3weeks': 'week',
        'week': '3days',
        '3days': 'day'
    };

    return getCalendar(null, modes[mode]);
};

