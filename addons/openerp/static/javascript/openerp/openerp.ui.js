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

var openobject;
if (!openobject && !openobject.dom) {
    throw "openobject.dom is required by 'openerp.ui'.";
}
var openerp;
if (!openerp) {
    openerp = {};
}

openerp.ui = {};

(function ($) {
    $.fn.toggler = function toggler(to_toggle/*, callback_on_toggle*/) {
        console.log('toggler', this.get(), $(to_toggle).get());
        var on_toggle = arguments[1];
        this.bind('click.toggler', function () {
            var linked = $(to_toggle);
            $(this).add(linked).toggleClass('open closed');
            if(on_toggle) {
                $.proxy(on_toggle, this)(linked);
            }
            $(window).trigger('on-appcontent-resize')
        });
        return this;
    }
})(jQuery);

function header_actions(url) {
    // For shortcuts
    if(arguments[1]) {
            url = openobject.http.getURL(url, {'id': arguments[1], 'model': arguments[2]});
    }
    
    if(jQuery('#appContent').length) {
        openLink(url)
    }
    else {
        window.location.href = openobject.http.getURL('/openerp/menu', {'next': url})
    }
}

jQuery(document).bind('shortcuts-alter', function () {
    var shortcuts = jQuery('#shortcuts > ul');
    var shortcuts_row = jQuery('#shortcuts');
    if(!shortcuts.length) { return; }
    var totalWidth = shortcuts.get(0).scrollWidth;
    var visibleWidth = shortcuts.outerWidth();

    if(totalWidth > visibleWidth) {
        if (!shortcuts_row.hasClass('scrolling')) {
            shortcuts_row.addClass('scrolling');
        }
        /*
            When resizing the window, if the bar is scrolled far to the right,
            we're going to display emptiness on the right even though we have hidden content on the left.
            Unscroll to fix that.
         */
        if(shortcuts.scrollLeft() > (totalWidth - visibleWidth)) {
            shortcuts.scrollLeft(totalWidth - visibleWidth);
        }
    } else {
        if(shortcuts_row.hasClass('scrolling')) {
            shortcuts_row.removeClass('scrolling');
            shortcuts.scrollLeft(0);
        }
    }
});

// trigger on window load so all other handlers (including resizer) have executed
// further stuff will be handled when adding/removing shortcuts anyway (theoretically)
jQuery(window).load(function () {
    var shortcuts = jQuery('#shortcuts');
    var scrolling_left, scrolling_right;
    var scroll_right = jQuery('<div id="shortcuts-scroll-left" class="scroller">').hover(
        function () {
            var scrollable = shortcuts.children('ul');
            scrolling_left = setInterval(function () {
                if(scrollable.scrollLeft() == 0) {
                    clearInterval(scrolling_left);
                }
                scrollable.scrollLeft(scrollable.scrollLeft() - 3);
            }, 30);
        }, function () {
            clearInterval(scrolling_left);
    });
    var scroll_left = jQuery('<div id="shortcuts-scroll-right" class="scroller">').hover(
        function () {
            var scrollable = shortcuts.children('ul');
            scrolling_right = setInterval(function () {
                if((scrollable.scrollLeft() + scrollable.outerWidth()) == scrollable.get(0).scrollWidth) {
                    clearInterval(scrolling_right);
                }
                scrollable.scrollLeft(scrollable.scrollLeft() + 3);
            }, 30);
        }, function () {
            clearInterval(scrolling_right);
    });
    shortcuts.prepend(scroll_right).prepend(scroll_left);
    jQuery(document).trigger('shortcuts-alter');
});
jQuery(window).resize(function () {
    jQuery(document).trigger('shortcuts-alter');
});
