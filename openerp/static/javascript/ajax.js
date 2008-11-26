////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
//
// $Id$
//
// Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
//
// The OpenERP web client is distributed under the "OpenERP Public License".
// It's based on Mozilla Public License Version (MPL) 1.1 with following 
// restrictions:
//
// -   All names, links and logos of Tiny, Open ERP and Axelor must be 
//     kept as in original distribution without any changes in all software 
//     screens, especially in start-up page and the software header, even if 
//     the application source code has been changed or updated or code has been 
//     added.
//
// -   All distributions of the software must keep source code with OEPL.
// 
// -   All integrations to any other software must keep source code with OEPL.
//
// If you need commercial licence to remove this kind of restriction please
// contact us.
//
// You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
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

// vim: ts=4 sts=4 sw=4 si et

