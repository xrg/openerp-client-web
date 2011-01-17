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

// Python style Datetime format

Date._days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
Date._months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
Date._datefmt = '%Y-%m-%d';
Date._timefmt = '%H:%M:%S';

Date._pad = function(num, len) {
    len = len ? len : (''+num).length;
    return (new Array(len).join('0') + num).slice(-len);
};

Date.prototype.strftime_callback = function(match0, match1) {

    switch (match1) {
        case 'a': return Date._days[this.getDay()].substr(0, 3);
        case 'A': return Date._days[this.getDay()];
        case 'h':
        case 'b': return Date._months[this.getMonth()].substr(0, 3);
        case 'B': return Date._months[this.getMonth()];
        case 'c': return this.toLocaleString();
        case 'd': return Date._pad(this.getDate(), 2);
        case 'H': return Date._pad(this.getHours(), 2);
        case 'I': return Date._pad(this.getHours() % 12 || 12, 2);
        case 'j': return Date._pad(this.getDayOfYear() + 1, 3);
        case 'm': return Date._pad(this.getMonth() + 1, 2);
        case 'M': return Date._pad(this.getMinutes(), 2);
        case 'p': return this.getHours() < 12 ? 'AM' : 'PM';
        case 'P': return this.getHours() < 12 ? 'am' : 'pm';
        case 'S': return Date._pad(this.getSeconds(), 2);
        case 'U': return this.getWeek();
        case 'w': return this.getDay();
        case 'W': return this.getWeek(1);
        case 'x': return this.format(Date._datefmt);
        case 'X': return this.format(Date._timefmt);
        case 'y': return this.getFullYear().toString().substr(2);
        case 'Y': return this.getFullYear();
        //case 'z':
        //case 'Z':
        default:
            return match0;
    }
};

Date.prototype.getDayOfYear = function() {
    var dt = new Date(this.getFullYear(), 0, 1);
    return Math.floor((this.getTime() - dt.getTime()) / 86400000);
};

/*
# Return week number for dates.
# Week numbers are calculated based on ISO 8601.
*/
Date.prototype.getWeek = function (dowOffset) {
	
	dowOffset = typeof(dowOffset) == 'int' ? dowOffset : 0;
	var newYear = new Date(this.getFullYear(), 0, 1);
	var day = newYear.getDay() - dowOffset; //the day of week the year begins on
	day = (day >= 0 ? day : day + 7);

	var daynum = Math.floor((this.getTime() - newYear.getTime() -
	(this.getTimezoneOffset()-newYear.getTimezoneOffset())*60000)/86400000) + 1;
	var weeknum;
	
	//if the year starts before the middle of a week
	if(day <= 4) {
		weeknum = Math.floor((daynum + day - 1) / 7) + 1;
		if(weeknum > 52) {
			nYear = new Date(this.getFullYear() + 1, 0, 1);
			nday = nYear.getDay() - dowOffset;
			nday = nday >= 0 ? nday : nday + 7;
			/*if the next year starts before the middle of
			the week, it is week #1 of that year*/
			weeknum = nday <= 4 ? 1 : 53;
		}
	}
	else {
		weeknum = Math.floor((daynum + day - 1) / 7);
	}
	return weeknum;
};

Date.prototype.strftime = function(format) {

    if (!format) return this.toLocaleString();

    if (format.indexOf('%%') > -1) { // a literal `%' character
        format = format.split('%%');
        for (var i = 0; i < format.length; i++)
            format[i] = this.strftime(format[i]);
        return format.join('%');
    }

    var dateObj = this;
    return format.replace(/%([aAbBcdhHIjmMpPSUwWxXyYZ])/g, function(match0, match1) {
        return dateObj.strftime_callback(match0, match1);
    });
};

Date.prototype.getWeekDay = function(monday) {
    var wday = this.getDay();
    return monday ? wday : (wday == 0 ? 6 : wday - 1);
};

Date.prototype.getNext = function() {

    //XXX: timezone problem (CEST, CET)
    // return new Date(this.getTime() + 24 * 60 * 60 * 1000);

    var y = this.getFullYear();
    var m = this.getMonth();
    var d = this.getDate();
    var H = this.getHours();
    var M = this.getMinutes();
    var S = this.getSeconds();
    var X = this.getMilliseconds();

    return new Date(y, m, d + 1, H, M, S, X);
};

Date.prototype.getPrevious = function() {
    //XXX: timezone problem (CEST, CET)
    // return new Date(this.getTime() - 24 * 60 * 60 * 1000);

    var y = this.getFullYear();
    var m = this.getMonth();
    var d = this.getDate();
    var H = this.getHours();
    var M = this.getMinutes();
    var S = this.getSeconds();
    var X = this.getMilliseconds();

    return new Date(y, m, d - 1, H, M, S, X);
};

// vim: ts=4 sts=4 sw=4 si et

