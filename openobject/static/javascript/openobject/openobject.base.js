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

if (typeof(MochiKit) == "undefined") {
    throw "MochiKit is required.";
}

var openobject;
if (typeof(openobject) == "undefined") {
    openobject = {};
    window.openobject = openobject;
}

openobject.base = {
    filter: function(items, callback, instance) {
        if (instance) {
            callback = MochiKit.Base.bind(callback, instance);
        }
        return MochiKit.Base.filter(callback, items);
    },

    map: function(items, callback, instance) {
        if (instance) {
            callback = MochiKit.Base.bind(callback, instance);
        }
        return MochiKit.Base.map(callback, items);
    },

    each: function(items, callback, instance) {
        return MochiKit.Iter.forEach(items, callback, instance);
    },

    find: function(items, value, start, end) {
        return MochiKit.Base.findIdentical(items, value, start, end);
    }
};

// browser information
openobject.browser = {
    // Internet Explorer
    isIE: /msie/.test(navigator.userAgent.toLowerCase()),

    // Internet Explorer 6
    isIE6: /msie 6/.test(navigator.userAgent.toLowerCase()),

    // Internet Explorer 7
    isIE7: /msie 7/.test(navigator.userAgent.toLowerCase()),

    // Gecko(Mozilla) derived
    isGecko: /gecko\//.test(navigator.userAgent.toLowerCase()),

    isGecko18: /rv:1.9.*gecko\//.test(navigator.userAgent.toLowerCase()),

    isGecko19: /rv:1.9.*gecko\//.test(navigator.userAgent.toLowerCase()),

    // Apple WebKit derived
    isWebKit: /webkit/.test(navigator.userAgent.toLowerCase()),

    // Opera
    isOpera: /opera/.test(navigator.userAgent.toLowerCase())
};

window.browser = openobject.browser;

// hack to prevent cross-domain security errors, if window is opened
// from different domain.
MochiKit.DOM.addLoadEvent(function() {
    try {
        window.opener.document.domain;
    } catch (e) {
        window.opener = null;
    }
});

/**
 * Tries to fit the size of the #appFrame frame to better fit its current
 * content.extend
 * Has to be called from the document outside of the frame itself.
 *
 * Probably won't get it exactly right, you might want to call it
 * several times
 */
function adjustAppFrame() {

    var appFrame = jQuery('#appFrame');
    var menuBar = jQuery("#menubar");
    var frameContents = appFrame.contents();
    var body = frameContents.find('body');
    var frameBody = frameContents.find('#main_form_body');
    var formBody = frameContents.find('#view_form');
    var treeBody = frameContents.find('#treeview');

	var frameHeight = [];
	
	frameHeight.push(jQuery(body).height());
    frameHeight.push(jQuery(frameBody).height());
    frameHeight.push(jQuery(formBody).height());
    frameHeight.push(jQuery(treeBody).height());

	appFrame.height(Math.max.apply(Math, frameHeight));
    var frameWidth = frameContents.width();

    appFrame.height(Math.max(0, frameHeight));

    var windowWidth = jQuery(window).width();
    var totalWidth = menuBar.width() + frameWidth;
    var rw = windowWidth - menuBar.width();

    var newWidth = totalWidth > windowWidth ? frameWidth : rw - 16;

    appFrame.width(Math.max(0, newWidth));
    jQuery("#contents").height(Math.max(frameHeight, menuBar.width()));
}
function adjust(count) {
    if (!count) {
        count = 0;
    }
    if (count < 3) {
        try {
            adjustAppFrame();
        } catch (e) {
            // don't do anything when adjustment blows up.
        }
        setTimeout(adjust, 10, count + 1);
    }
}
if (window !== window.parent) {
    MochiKit.DOM.addLoadEvent(function () {
        // Gecko blows up if we try to directly call window.parent.adjust()
        // and cross-frame events don't seem to work either
        // so use intermediate function.
        var do_adjust = function () {
            window.parent.adjust();
        };
        setTimeout(do_adjust, 10);
        // bind on all modifying events of notebooks
        forEach($$('.notebook'), function (notebook_element) {
            forEach(['remove', 'show', 'hide', 'activate', 'click'], function (event) {
                MochiKit.Signal.connect(notebook_element.notebook,
                        event, do_adjust);
            });
        });
        // bind to resize event of text area
        forEach($$('.resizable-textarea'), function (textarea_element) {
            MochiKit.Signal.connect(textarea_element.textarea, 'onresize', do_adjust);
        });
        // bind to alterations of the list views
        forEach($$('.gridview'), function (listview_element) {
            var name = listview_element.getAttribute('id');
            MochiKit.Signal.connect(ListView(name), 'onreload', do_adjust);
        });
        // bind to addition and removal of filter rows in search widget
        var filter_table = $('filter_table');
        if (filter_table) {
            MochiKit.Signal.connect(filter_table, 'onaddfilter',
                    do_adjust);
            MochiKit.Signal.connect(filter_table, 'onremovefilter',
                    do_adjust);
        }
        // bind to change of the groupby display state in search widget
        var search_filter = $('search_filter_data');
        if (search_filter) {
            MochiKit.Signal.connect(search_filter, 'groupby-toggle', do_adjust);
        }

        // bind to changes sidebar/toolbar
        var sidebar = openobject.dom.get('sidebar');
        if (sidebar) {
            MochiKit.Signal.connect(window.document, 'toggle_sidebar', do_adjust);
        }
        // bind to changes to treegrids and treenodes
        MochiKit.Signal.connect(window.document, 'treegrid-render', do_adjust);
        MochiKit.Signal.connect(window.document, 'treenode-expand', do_adjust);
        MochiKit.Signal.connect(window.document, 'treenode-collapse', do_adjust);
        // bind to "onchange" attributes on view/form fields, maybe
        MochiKit.Signal.connect(window.document, 'onfieldchange', do_adjust);
        // bind to expansion/collapse of grouped fields (in list/search views)
        MochiKit.Signal.connect(window.document, 'toggle-group-data', do_adjust);
    });
}
