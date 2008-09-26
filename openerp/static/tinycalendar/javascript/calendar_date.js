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

    switch(match1) {
        case 'a': return Date._days[this.getDay()].substr(0,3);
        case 'A': return Date._days[this.getDay()];
        case 'h':
        case 'b': return Date._months[this.getMonth()].substr(0,3);
        case 'B': return Date._months[this.getMonth()];
        case 'c': return this.toLocaleString();
        case 'd': return Date._pad(this.getDate(), 2);
        case 'H': return Date._pad(this.getHours(), 2);
        case 'I': return Date._pad(this.getHours() % 12 || 12, 2);
        case 'j': return Date._pad(this.getDayOfYear()+1, 3);
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
}

Date.prototype.getDayOfYear = function(){
    var dt = new Date(this.getFullYear(), 0, 1);
    return Math.floor((this.getTime() - dt.getTime()) / 86400000);
}

Date.prototype.getWeek = function(monday){

    var yday = this.getDayOfYear();
    var wday = this.getDay();

    if (monday) {
       wday = wday ? wday - 1 : 6;
    }

    return Math.floor((yday + 7 - wday) / 7);
}

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
}

Date.prototype.getWeekDay = function(monday){
    var wday = this.getDay();
    return monday ? wday : (wday == 0 ? 6 : wday - 1);
}

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

    return new Date(y, m, d+1, H, M, S, X);
}

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

    return new Date(y, m, d-1, H, M, S, X);
}

// vim: ts=4 sts=4 sw=4 si et

