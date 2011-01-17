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
        var on_toggle = arguments[1];
        this.bind('click.toggler', function () {
            var linked = $(to_toggle);
            $(this).add(linked).toggleClass('open closed');
            if(on_toggle) {
                $.proxy(on_toggle, this)(linked);
            }
            $(window).trigger('on-appcontent-resize');
            return false;
        });
        return this;
    }
})(jQuery);

(function ($) {
    /**
     * @event altered to send to the element when something happened which
     *  might alter its visible or actual widths (addition or removal of an
     *  item). <code>window.resize</code> is managed by the plugin, you do
     *  not have to register it yourself.
     */
    var DEFAULTS = {
        "speed": 3
    };

    function scrollable_alteration() {
        var $scrollable = jQuery(this);
        var $scrollable_list = $scrollable.children('ul');

        var totalWidth = $scrollable_list.get(0).scrollWidth;
        var visibleWidth = $scrollable_list.outerWidth();

        if(totalWidth <= visibleWidth) {
            if($scrollable.hasClass('scrolling')) {
                $scrollable.removeClass('scrolling');
                $scrollable_list.scrollLeft(0);
            }
            return;
        }

        if(!$scrollable.hasClass('scrolling')) {
            $scrollable.addClass('scrolling');
        }
        /*
         When widening the window, if the bar is scrolled far to the right,
         we're going to display emptiness on the right even though we have
         hidden content on the left. Unscroll to fix that.
         */
        if($scrollable_list.scrollLeft() > (totalWidth - visibleWidth)) {
            $scrollable_list.scrollLeft(totalWidth - visibleWidth);
        }
    }

    /**
     * Makes an element scrollable (left-right) when the element's content is
     * too big for the container.
     *
     * Should be invoked on a container (of any type) holding a list element
     * as its direct child (untested with more than one child).
     *
     * Will create two elements with the class <code>.scroller</code> as
     * direct children of the context, one with the class <code>.left</code>
     * and one with the class <code>.right</code>.
     *
     * @param options An object containing configuration options for the
     *                plugin
     *
     * @config {Number} speed Scrolling speed of the scrollable, in pixels per iteration, when hovering the side scrollers.
     */
    $.fn.scrollify = function scrollify(options) {
        var settings = $.extend({}, DEFAULTS, options || {});
        this.each(function () {
            var $scrollable = $(this);
            var $scrollable_list = $scrollable.children('ul');
            if($scrollable.data('scrollified')
               || !($scrollable.length && $scrollable_list.length)) {
                return;
            }
            $scrollable.data('scrollified', true);
            var scrolling_left, scrolling_right;
            var $left_scroller = $('<div class="left scroller">').hover(
                function () {
                    scrolling_left = setInterval(function () {
                        if($scrollable_list.scrollLeft() == 0) {
                            clearInterval(scrolling_left);
                        }
                        $scrollable_list.scrollLeft(
                                $scrollable_list.scrollLeft()
                                - settings.speed);
                    }, 30);
                }, function () {
                    clearInterval(scrolling_left);
            });
            var $right_scroller = $('<div class="right scroller">').hover(
                function () {
                    scrolling_right = setInterval(function () {
                        var scrolledMax = (
                                ( $scrollable_list.scrollLeft()
                                + $scrollable_list.outerWidth())
                            == $scrollable_list.get(0).scrollWidth);
                        if(scrolledMax) {
                            clearInterval(scrolling_right);
                        }
                        $scrollable_list.scrollLeft(
                                $scrollable_list.scrollLeft()
                                + settings.speed);
                    }, 30);
                }, function () {
                    clearInterval(scrolling_right);
            });
            $scrollable.prepend($left_scroller).prepend($right_scroller);

            $scrollable.bind('altered.scrollify', scrollable_alteration);
            $(window).bind('resize.scrollify', function () {
                $scrollable.trigger('altered');
            });
            $scrollable.trigger('altered');
        });
        return this;
    }
})(jQuery);

jQuery(document).ready(function () {
    jQuery('#applications_menu').scrollify();
    jQuery('#shortcuts').scrollify();
});
