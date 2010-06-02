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


(function() {
    var __ajax_stat_elem = null;

    var onAjaxStart = function() {
        onAjaxStatPosition();
        MochiKit.DOM.showElement(__ajax_stat_elem);
    };

    var onAjaxStop = function() {

        if (openobject.http.AJAX_COUNT > 0)
            return;

        try {
            MochiKit.Async.callLater(0.5, MochiKit.DOM.hideElement, __ajax_stat_elem);
        } catch(e) {
        }
    };

    var onAjaxStatPosition = function() {

        var x = (MochiKit.DOM.getViewportDimensions().w / 2) -
                (MochiKit.DOM.elementDimensions(__ajax_stat_elem).w / 2);
        var y = (window.pageYOffset ||
                parent.document.body.scrollTop ||
                parent.document.documentElement.scrollTop) + 5;

        __ajax_stat_elem.style.left = x + 'px';
        __ajax_stat_elem.style.top = y + 'px';
    };

    jQuery(document).ready(function() {
        __ajax_stat_elem = DIV({'align': 'center'}, _('Loading...'));

        with (__ajax_stat_elem.style) {
            display = "none";
            position = "absolute";
            padding = "2px 8px";
            color = "white";
            backgroundColor = "red";
            fontWeight = "bold";
            zIndex = 1000;
        }

        MochiKit.DOM.appendChildNodes(parent.document.body, __ajax_stat_elem);

        MochiKit.Signal.connect(window, "ajaxStart", onAjaxStart);
        MochiKit.Signal.connect(window, "ajaxStop", onAjaxStop);

        MochiKit.Signal.connect(window, "onresize", onAjaxStatPosition);
        MochiKit.Signal.connect(window, "onscroll", onAjaxStatPosition);
        onAjaxStatPosition();
    });
})();
