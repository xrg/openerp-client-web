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

if (typeof(_) == "undefined") {
    _ = function(key) {return key};
}

var Browser = {

    // Is Internet Explorer?
    isIE : /msie/.test(navigator.userAgent.toLowerCase()),

    // Is Internet Explorer 6?
    isIE6 : /msie 6/.test(navigator.userAgent.toLowerCase()),

    // Is Internet Explorer 7?
    isIE7 : /msie 7/.test(navigator.userAgent.toLowerCase()),

    // Is Gecko(Mozilla) derived?
    isGecko : /gecko\//.test(navigator.userAgent.toLowerCase()),
    isGecko18 : /rv:1.8.*gecko\//.test(navigator.userAgent.toLowerCase()),
    isGecko19 : /rv:1.9.*gecko\//.test(navigator.userAgent.toLowerCase()),

    // Is Apple WebKit derived?
    isWebKit : /webkit/.test(navigator.userAgent.toLowerCase()),

    // Is opera?
    isOpera : /opera/.test(navigator.userAgent.toLowerCase())
};

function elementPosition2(elem) {
    var x = 0, y = 0;
    if (elem.offsetParent) {
        x = elem.offsetLeft;
        y = elem.offsetTop;
        while (elem = elem.offsetParent) {
            x += elem.offsetLeft;
            y += elem.offsetTop
        }
    }
    return {x: x, y: y};
}

///////////////////////////////////////////////////////////////////////////////

jQuery(document).ajaxStop(function () {
    if(window.CAL_INSTANCE) {
        setTimeout(function() {
			jQuery.proxy(window.CAL_INSTANCE, 'onResize')
		}, 100);
    }
});

jQuery(window).bind('before-appcontent-change', function () {
    try{
        window.CAL_INSTANCE.__delete__();
        window.CAL_INSTANCE = null;
    }catch(e){}
});

jQuery(window).bind('after-appcontent-change on-appcontent-resize', function () {
    try{
        window.CAL_INSTANCE.onResize();
    }catch(e){}
});

jQuery(function(){
    window.CALENDAR_WAIT_BOX = new openerp.ui.WaitBox();
});

function getCalendar(day, mode, color_filters) {
    day = day || openobject.dom.get('_terp_selected_day').value;
    mode = mode || openobject.dom.get('_terp_selected_mode').value;

    var act = openobject.http.getURL('/view_calendar/calendar/get', {day: day, mode: mode});

    var form = document.forms['view_form'];
    var contents = formContents(form);
    var params = {};

    for (var i = 0; i < contents[0].length; i++) {
        var k = contents[0][i];
        var v = contents[1][i];

        params[k] = [v];
    }
    if(color_filters) {
        params['_terp_color_filters'] = color_filters;
    }

    // colors
    var values = jQuery('#calGroups input:checked').map(function (i, e) {
        return jQuery(e).val(); }).get();

    params['_terp_colors'] = openobject.dom.get('_terp_colors').value;
    params['_terp_color_values'] = values.join(",");

    CALENDAR_WAIT_BOX.showAfter(300);

    var sTop = jQuery('#calGridC').scrollTop();
    var sLeft = jQuery('#calGridC').scrollLeft();

    var req = openobject.http.postJSON(act, params);

    req.addCallback(function(obj) {
        jQuery('#Calendar').replaceWith(obj.calendar).hide();
        jQuery('#sidebar').replaceWith(obj.sidebar);
        try{
            jQuery('#calGridC').scrollTop(sTop).scrollLeft(sLeft);
        }catch(e){}
        setTimeout(function () {
            CALENDAR_WAIT_BOX.hide();
        }, 0);
    });

    req.addErrback(function(e) {
        log(e);
    });
}

function getMiniCalendar(action) {
    var req = openobject.http.post(action);

    req.addCallback(function(xmlHttp) {
        var newMiniCalendar = jQuery(xmlHttp.responseText);
        jQuery('#calMini > div.minical-a').replaceWith(newMiniCalendar);
    });
}

function saveCalendarRecord(record_id, starts, ends) {
    var params = getFormParams('_terp_concurrency_info');
    MochiKit.Base.update(params, {
        '_terp_id': record_id,
        '_terp_model': openobject.dom.get('_terp_model').value,
        '_terp_fields': openobject.dom.get('_terp_calendar_fields').value,
        '_terp_starts' : starts,
        '_terp_ends' : ends,
        '_terp_context': openobject.dom.get('_terp_context').value
    });

    var req = openobject.http.postJSON('/view_calendar/calendar/save', params);

    return req.addCallback(function(obj) {
        // update concurrency info
        for (var key in obj.info) {
            try {
                var items = openobject.dom.select("[name=_terp_concurrency_info][value*=" + key + "]");
                var value = "('" + key + "', '" + obj.info[key] + "')";
                for (var i = 0; i < items.length; i++) {
                    items[i].value = value;
                }
            } catch(e) {
            }
        }
        return obj;
    });
}

function editCalendarRecord(record_id, date) {
    jQuery.frame_dialog({src:openobject.http.getURL('/view_calendar/calpopup/edit', {
            'id': record_id,
            'model': openobject.dom.get('_terp_model').value,
            'view_mode': openobject.dom.get('_terp_view_mode').value,
            'view_ids': openobject.dom.get('_terp_view_ids').value,
            'domain': openobject.dom.get('_terp_domain').value,
            'context': openobject.dom.get('_terp_context').value,
            'default_date': date
    })});
}

function copyCalendarRecord(record_id) {
    return openobject.http.post('/view_calendar/calendar/duplicate', {
        '_terp_id': record_id,
        '_terp_model': openobject.dom.get('_terp_model').value,
        '_terp_context': openobject.dom.get('_terp_context').value
    });
}

function getRecordMovability(element) {
    return {
        starts: jQuery(element).attr('dtstart'),
        ends : jQuery(element).attr('dtend'),
        is_not_movable: jQuery(element, element.parentNode).hasClass('event-is-not-movable'),
        is_not_resizeable: jQuery(element, element.parentNode).hasClass('event-is-not-resizeable')
    }
}

