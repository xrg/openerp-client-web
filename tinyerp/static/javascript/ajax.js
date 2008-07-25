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
// This program is Free Software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the 
// Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
// Boston, MA  02111-1307, USA.
//
////////////////////////////////////////////////////////////////////////////////

var Ajax = function(){
}

Ajax.COUNT = 0;
Ajax._status = null;

MochiKit.DOM.addLoadEvent(function(){

    Ajax._status = DIV({'style': 'display: none; position: absolute; padding: 2px 4px; color: white; background-color: red; font-weight: bold;'}, 'Loading...');
    MochiKit.DOM.appendChildNodes(document.body, Ajax._status);
});

Ajax.showStatus = function() {
    
    if (Ajax._status) {

        var x = (MochiKit.DOM.getViewportDimensions().w / 2) - (MochiKit.DOM.elementDimensions(Ajax._status).w / 2);
        var y = (window.pageYOffset || document.body.scrollTop || document.documentElement.scrollTop) + 5;

        Ajax._status.style.left = x + 'px';
        Ajax._status.style.top = y + 'px';

        MochiKit.DOM.showElement(Ajax._status);
    }
}

Ajax.hideStatus = function() {

    if (Ajax.COUNT > 0) 
        return;

    try {
      MochiKit.Async.callLater(0.1, MochiKit.DOM.hideElement, Ajax._status);
    } catch(e){
    }
}

Ajax.prototype = {

    get: function(url, params){

        Ajax.COUNT += 1;
        Ajax.showStatus();

        var req = MochiKit.Async.doSimpleXMLHttpRequest(url, params || {});

        return req.addBoth(function(xmlHttp){
            Ajax.COUNT -= 1;
            Ajax.hideStatus();
            return xmlHttp;
        });
    },

    post: function(url, params){

        Ajax.COUNT += 1;
        Ajax.showStatus();

       // prepare queryString for url and/or params
        var qs = url.slice(url.indexOf('?')).slice(1);
        var url = url.split('?')[0];

        if (params) {
            qs = (qs ? qs + '&' : '') + MochiKit.Base.queryString(params);
        }

        var req = MochiKit.Async.getXMLHttpRequest();
        req.open("POST", url, true);

        req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        req.setRequestHeader("Connection", "close");

        if (qs) {
           req.setRequestHeader("Content-length", qs.length);
        }
        
        req = MochiKit.Async.sendXMLHttpRequest(req, qs);
        
        return req.addBoth(function(xmlHttp){
            Ajax.COUNT -= 1;
            Ajax.hideStatus();
            return xmlHttp;
        });
    }
}

Ajax.get = function(url, params){
    return new Ajax().get(url, params);
}

Ajax.post = function(url, params){
    return new Ajax().post(url, params);
}

var JSON = function(){
}

JSON.prototype = {

    get: function(url, params){
        var req = Ajax.get(url, params);
        return req.addCallback(MochiKit.Async.evalJSONRequest);
    },

    post: function(url, params){
        var req = Ajax.post(url, params);
        return req.addCallback(MochiKit.Async.evalJSONRequest);
    }
}

JSON.get = function(url, params){
    return new JSON().get(url, params);
}

JSON.post = function(url, params){
    return new JSON().post(url, params);
}

Ajax.JSON = new JSON();

// vim: sts=4 st=4 et
