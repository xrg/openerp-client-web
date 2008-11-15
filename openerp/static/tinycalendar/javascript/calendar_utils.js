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
}

function elementPosition2(elem) {
    var x = y = 0;
    if (elem.offsetParent) {
        x = elem.offsetLeft
        y = elem.offsetTop
        while (elem = elem.offsetParent) {
            x += elem.offsetLeft
            y += elem.offsetTop
        }
    }
    return {x: x, y: y};
}

///////////////////////////////////////////////////////////////////////////////

var CAL_INSTANCE = null;

var getCalendar = function(day, mode) {

    var day = day || MochiKit.DOM.getElement('_terp_selected_day').value;
    var mode = mode || MochiKit.DOM.getElement('_terp_selected_mode').value;
    
    var act = getURL('/calendar/get', {day: day, mode: mode});

    var form = document.forms['view_form'];
    var contents = formContents(form);
    var params = {};

    for(var i in contents[0]){
        var k = contents[0][i];
        var v = contents[1][i];

        params[k] = [v];
    }

    // colors
    var colors = getElementsByTagAndClassName('input', null, 'calGroups');
    var values = [];

    colors = filter(function(e){return e.checked}, colors);
    forEach(colors, function(e){
        values = values.concat(e.value);
    });

    params['_terp_colors'] = $('_terp_colors').value;
    params['_terp_color_values'] = '[' + values.join(",") + ']';

    showElement('calLoading');

    var req = Ajax.post(act, params);
    req.addCallback(function(xmlHttp){

        var d = DIV();
        d.innerHTML = xmlHttp.responseText;

        var newContainer = d.getElementsByTagName('table')[0];
        
        if (newContainer.id != 'calContainer'){
        log(11111);
            return ;//window.location.href = '/';   
        }

        // release resources
        CAL_INSTANCE.__delete__();

        swapDOM('calContainer', newContainer);

        var ua = navigator.userAgent.toLowerCase();

        if ((navigator.appName != 'Netscape') || (ua.indexOf('safari') != -1)) {
            // execute JavaScript
            var scripts = getElementsByTagAndClassName('script', null, newContainer);
            forEach(scripts, function(s){
                eval(s.innerHTML);
            });
        }

        callLater(0, bind(CAL_INSTANCE.onResize, CAL_INSTANCE));
    });

    req.addErrback(function(e){
        log(e);
    });
}

var getMiniCalendar = function(action) {
    var req = Ajax.post(action);

    req.addCallback(function(xmlHttp){

        var d = DIV();
        d.innerHTML = xmlHttp.responseText;

        var newMiniCalendar = d.getElementsByTagName('div')[0];

        swapDOM('MiniCalendar', newMiniCalendar);
    });
}

var saveCalendarRecord = function(record_id, starts, ends){

    var params = {
        '_terp_id': record_id,
        '_terp_model': $('_terp_model').value,
        '_terp_fields': $('_terp_calendar_fields').value,
        '_terp_starts' : starts,
        '_terp_ends' : ends,
        '_terp_context': $('_terp_context').value
    }

    return Ajax.JSON.post('/calendar/save', params);
}

var editCalendarRecord = function(record_id){

    var params = {
        'id': record_id,
        'model': $('_terp_model').value,
        'view_mode': $('_terp_view_mode').value,
        'view_ids': $('_terp_view_ids').value,
        'domain': $('_terp_domain').value,
        'context': $('_terp_context').value
    }

    var act = getURL('/calpopup/edit', params);
    openWindow(act);
}

var copyCalendarRecord = function(record_id){

    var params = {
        '_terp_id': record_id,
        '_terp_model': $('_terp_model').value,
        '_terp_context': $('_terp_context').value
    }

    return Ajax.post('/calpopup/duplicate', params);
}

// vim: ts=4 sts=4 sw=4 si et

