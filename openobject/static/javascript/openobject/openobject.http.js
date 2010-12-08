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
// -   All names, links and logos of Tiny, OpenERP and Axelor must be 
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

openobject.http = {

    SCRIPT_PATH: "",
    
    AJAX_COUNT: 0,

    get: function(uri, params) {
        
        if (this.AJAX_COUNT == 0) {
            MochiKit.Signal.signal(window, "ajaxStart");
        }
        
        this.AJAX_COUNT += 1;
        
        var req = MochiKit.Async.doSimpleXMLHttpRequest(this.getURL(uri), params || {});
        
        return req.addBoth(function(xmlHttp){
            openobject.http.AJAX_COUNT -= 1;
            if (openobject.http.AJAX_COUNT == 0) {
                MochiKit.Signal.signal(window, "ajaxStop");
            }
            return xmlHttp;
        });
    },
    
    post: function(uri, params) {
    
        if (this.AJAX_COUNT == 0) {
            MochiKit.Signal.signal(window, "ajaxStart");
        }
        
        this.AJAX_COUNT += 1;
        
       // prepare queryString for uri and/or params
        var qs = uri.slice(uri.indexOf('?')).slice(1);
        var uri = uri.split('?')[0];

        if (params) {
            qs = (qs ? qs + '&' : '') + MochiKit.Base.queryString(params);
        }

        var req = MochiKit.Async.getXMLHttpRequest();
        req.open("POST", this.getURL(uri), true);

        req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        
        req = MochiKit.Async.sendXMLHttpRequest(req, qs);
        
        return req.addBoth(function(xmlHttp){
            openobject.http.AJAX_COUNT -= 1;
            if (openobject.http.AJAX_COUNT == 0) {
                MochiKit.Signal.signal(window, "ajaxStop");
            }
            return xmlHttp;
        });
    },
    
    getJSON: function(uri, params) {
        var req = this.get(uri, params);
        return req.addCallback(MochiKit.Async.evalJSONRequest);
    },
    
    postJSON: function(uri, params) {
        var req = this.post(uri, params);
        return req.addCallback(MochiKit.Async.evalJSONRequest);
    },
        
    getURL: function(uri, params) {
    
        var qs = params ? MochiKit.Base.queryString(params) : null;
        var sp = this.SCRIPT_PATH;
        
        if (sp && uri && uri[0] == "/" && uri.indexOf(sp) != 0) {
            uri = sp + uri;
        }
    
        return qs ? uri + "?" +  qs : uri;
    },
    
    redirect: function(uri, params) {
        window.location.href = this.getURL(uri, params);
    },
       
    setCookie: function(name, value, expires, path, domain, secure) {
    
        var path = path ? this.getURL(path) : this.SCRIPT_PATH;
        
        var cookie = name + "=" + escape(value) +
            ((expires) ? "; expires=" + expires.toGMTString() : "") +
            ((path) ? "; path=" + path : "") +
            ((domain) ? "; domain=" + domain : "") +
            ((secure) ? "; secure" : "");
            
        document.cookie = cookie;
    },
    
    getCookie: function(name) {
    
        var dc = document.cookie;
        var prefix = name + "=";
        var begin = dc.indexOf("; " + prefix);
        
        if (begin == -1) {
            begin = dc.indexOf(prefix);
            if (begin != 0) { return null; }
        } else {
            begin += 2;
        }
        
        var end = document.cookie.indexOf(";", begin);
        
        if (end == -1) {
            end = dc.length;
        }
        
        return unescape(dc.substring(begin + prefix.length, end));
    },
    
    delCookie: function(name, path, domain) {
    
        var path = path ? this.getURL(path) : this.SCRIPT_PATH;
        
        if (this.getCookie(name)) {
            document.cookie = name + "=" +
                ((path) ? "; path=" + path : "") +
                ((domain) ? "; domain=" + domain : "") +
                "; expires=Thu, 01-Jan-70 00:00:01 GMT";
        }    
    }
};

(function ($) {
    /**
     * Extract the current hash-url from the page's location
     *
     * @returns the current hash-url if any, otherwise returns `null`
     */
    function getHashUrl() {
        var newUrl = null;
        // would use window.location.hash but...
        // https://bugzilla.mozilla.org/show_bug.cgi?id=483304
        var hashValue = window.location.href.split('#')[1] || '';
        jQuery.each(hashValue.split('&'), function (i, element) {
            var e = element.split("=");
            if(e[0] === 'url') {
                newUrl = decodeURIComponent(e[1]);
            }
        });
        return newUrl;
    }

    /**
     * Sets the current hash-url, as well as the $.hash.currentUrl member
     *  variable
     *
     * @param url the hash-url to set
     */
    function setHashUrl(url) {
        $.hash.currentUrl = url;
        var hash = '#' + jQuery.param({'url': url});
        try {
            window.location.hash = hash;
        } catch (e) {
            // MSIE throws an Access Denied error when trying to set hash,
            // but in other browsers this breaks wizards closing with a
            // `current` target: they set the whole URL and navigate to it.
            window.location.href = hash;
        }
    }

    /**
     * If a URL is provided, sets that url as the hash-url for the current
     * page. Otherwise, returns the current hash-url.
     *
     * Sets the current URL as an attribute of itself for hash-checking
     * purposes
     *
     * @param url the url to set
     *
     * @field currentUrl the last URL set by a <code>$.hash(url)</code>
     * call specifically
     */
    $.hash = function (url) {
        if(!url) {
            return getHashUrl();
        }
        setHashUrl(url);
    }
})(jQuery);
