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

if (typeof(jQuery) == "undefined") {
    throw "jQuery is required by 'openobject.dom'.";
}

/**
 * Escapes a DOM id so it's suitable for usage as a CSS selector
 * @param id the DOM id
 */
function escapeId(id) {
    return id.replace(/[^\r\n\f0-9a-z_-]/ig, "\\$&");
}
/**
 * Transforms a node id in the corresponding CSS selector: escapes the id and prefixes with '#'.
 * @param nodeId the DOM id to transform into selector
 */
function idSelector(nodeId) {
    if (!(typeof nodeId === 'string')) {
        return nodeId;
    }

    return '#' + escapeId(nodeId);
}

(function ($) {
    /**
     * Replaces a class by an other one, if and only if it is present
     *
     * The code
     *
     * <code>$e.toggleClass(from, to)</code>
     *
     * is equivalent to the following code jQuery code:
     *
     * <code>if($e.hasClass(from)) { $e.toggleClass(from + ' ' + to); }</code>
     *
     * @param from the class to remove from the object
     * @param to the class to add on the object if <code>was present</code>
     */
    $.fn.swapClass = function (from, to) {
        if(!this.hasClass(from)) { return this; }
        this.removeClass(from).addClass(to);
        return this;
    }
})(jQuery);

(function ($) {
    function open($this, frame_attrs, data, options) {
        var options = $.extend(true, {
            modal: true,
            close: function () {
                this.close = null;
                $(this).dialog('destroy').remove();
            }
        }, options);

        options.width = get_width(options.width || "700px");
        options.min_width = get_width(options.min_width || 0);
        options.max_width = get_width(options.max_width || "100%");
        options.height = get_height(options.height || "500px");
        options.min_height = get_height(options.min_height || 0);
        options.max_height = get_height(options.max_height || "100%");

        if (options.width > options.max_width) options.width = options.max_width;
        if (options.width < options.min_width) options.width = options.min_width;
        if (options.height > options.max_height) options.height = options.max_height;
        if (options.height < options.min_height) options.height = options.min_height;

        var $frame = $('<iframe>', $.extend({
            frameborder: 0
        }, frame_attrs || {}))
            .appendTo(document.documentElement)
            .data('source-window', $this[0])
            .data(data || {})
            .dialog({
                modal: options.modal,
                width: options.width,
                height: options.height,
                close:  options.close
            });
        $frame[0].set_title = function (title) {
            $frame.prev().find('.ui-dialog-title').text(title);
        };
        $frame[0].close = function () {
            $frame.dialog('close');
        };
        return $frame;
    }

    function get_width(val) {
        return get_size(val.toString(), $(window.top).width());
    }

    function get_height(val) {
        return get_size(val.toString(), $(window.top).height());
    }

    function get_size(val, available_size) {
        if (val.slice(-1) == "%") {
            return Math.round(available_size / 100 * parseInt(val.slice(0, -1)));
        } else {
            return parseInt(val);
        }
    }
    /**
     * Creates an iframe-based jquery-ui dialog.
     *
     * Currently, the size of the dialog is hardcoded to 640x480, needs to
     * be fixed.
     *
     * The dialog is also modal, and destroyed on close.
     *
     * @param frame_attrs The attributes to provide to the iframe being
     * generated, should hold at least an <code>src</code> key
     * @param data <code>jQuery.data</code> to be set on the iframe element
     *  (<code>window.frameElement</code> from within the iframe)
     * @param options Options/Properties of the dialog
     *  width, height, min_width, max_width, min_height, max_height (in px or %)
     */
    $.frame_dialog = function (frame_attrs, data, options) {
        // $this should be the holder for the window from which
        // $.frame_dialog was originally called, even if $.frame_dialog()
        // was bubbled to the top of the window stack.
        var $this;
        if(this == $) $this = $(window);
        else $this = $(this);
        if(window != window.top) {
            return window.top.jQuery.frame_dialog.apply($this[0], arguments);
        }
        return open($this, frame_attrs, data, options);
    }
})(jQuery);

openobject.dom = {

    /**
     * Get element by id.
     *
     * @param elem: element id
     *
     */
    get: function(elem) {
        return MochiKit.DOM.getElement(elem);
    },

    /**
     * Get list of elements matching the given selector.
     *
     * @param selector: the selector
     * @param context: the context
     *
     */
    select: function(selector, context) {

        if (selector == window || selector == document) {
            return [selector];
        }

        if (typeof(selector) != "string") {
            return MochiKit.Base.isArrayLike(selector) ? selector : [selector];
        }

        return jQuery(selector, MochiKit.DOM.getElement(context)).get();
    },

    /**
     * Toggle visibility of the elements matching the given selector.
     *
     * @param selector: the selector
     * @param forced: forced visibility (supported by the tag)
     *
     */
    toggle: function(selector, forced) {
        var elems = this.select(selector);
        openobject.base.each(elems, function(e) {
            e.style.display = forced ? forced : (e.style.display == "none" ? "" : "none");
        });
    },

    /**
     * Get/Set attributes of the maching elements.
     *
     * @param selector: the selector
     * @param attr: attribute name or attribute=value mapping
     * @param value: attribute value of `attr` is string
     */
    attr: function(selector, attr, value) {

        var elems = this.select(selector);
        var attrs = attr;

        if (elems.length == 0) {
            return null;
        }

        if (typeof(attr) == "string") {

            if (typeof(value) == "undefined")
                return MochiKit.DOM.getNodeAttribute(elems[0], attr);

            attrs = {attr: value};
        }

        MochiKit.Iter.forEach(elems, function(e) {
            MochiKit.DOM.updateNodeAttributes(e, attrs);
        });
    },

    /**
     * Get/Set css style to the maching elements.
     *
     * @param selector: the selector
     * @param css: the css name or css=value mapping
     * @param value: value of `css` is a string
     *
     */
    css: function(selector, css, value) {

        var elems = this.select(selector);

        if (elems.length == 0) {
            return null;
        }

        if (typeof(css) == "undefined") {
            return MochiKit.Style.getStyle(elems[0], css);
        }

        var css = typeof(css) == "string" ? {css: value} : css;

        MochiKit.Iter.forEach(elems, function(e) {
            MochiKit.Style.setStyle(e, css);
        });
    },

    /**
     * Get/Set size of the matching elements
     *
     * @param selector: the selector
     * @param size: the size ({w: w, h: h})
     *
     */
    size: function(selector, size) {

        var elems = this.select(selector);

        if (elems.length == 0) {
            return {w: 0, h: 0};
        }

        if (elems[0] === window) {
            return MochiKit.Style.getViewportDimensions();
        }

        if (elems[0] === document) {
            var w = Math.max(document.body.scrollWidth, document.body.clientWidth);
            var h = Math.max(document.body.scrollHeight, document.body.clientHeight);
            return {w: w, h: h};
        }

        if (typeof(size) == "undefined") {
            //TODO: consider border + padding
            return MochiKit.Style.getElementDimensions(elems[0]);
        }

        var w = size.w || size.width;
        var h = size.h || size.height;

        var dim = {};

        if (w >= 0) {
            dim.w = w;
        }

        if (h >= 0) {
            dim.h = h;
        }

        MochiKit.Iter.forEach(elems, function(e) {
            MochiKit.Style.setElementDimensions(e, dim);
        });
    },

    /**
     * Get/Set position of the matching elements.
     *
     * @param selector: the selector
     * @param position: the position ({x: x, y: y})
     * @param relateiveTo: the position relative to this element
     */
    pos: function(selector, position, relativeTo) {

        var elems = this.select(selector);

        if (elems.length == 0) {
            return {x: 0, y: 0};
        }

        if (typeof(position) == "undefined") {
            return MochiKit.Style.getElementPosition(elems[0], relativeTo);
        }

        var x = position.x || position.left;
        var y = position.y || position.top;

        var pos = {};

        if (x >= 0) {
            pos.x = x;
        }

        if (y >= 0) {
            pos.y = y;
        }

        MochiKit.Iter.forEach(elems, function(e) {
            MochiKit.Style.setElementPosition(e, pos, relativeTo);
        });
    },

    /**
     * Get/Set width of the matching elements.
     *
     * @param selector: the selector
     * @param width: width to set
     */
    width: function(selector, width) {
        var size = this.size(selector, width);
        return size ? size.w : null;
    },

    /**
     * Get/Set height of the matching elements.
     *
     * @param selector: the selector
     * @param height: height to set
     */
    height: function(selector, height) {
        var size = this.size(selector, height);
        return size ? size.h : null;
    },

    /**
     * Get/Set top position of the matching elements
     *
     * @param selector: the selector
     * @param top: the top position
     */
    top: function(selector, top) {
        var pos = this.pos(selector, top);
        return pos ? pos.y : null;
    },

    /**
     * Get/Set left position of the matching elements
     *
     * @param selector: the selector
     * @param left: the left position
     */
    left: function(selector, left) {
        var pos = this.pos(selector, left);
        return pos ? pos.x : null;
    },

    /**
     * Show the matching elements
     *
     * @param selector: the selector
     */
    show: function(selector) {
        MochiKit.Iter.forEach(this.select(selector), function(e) {
            e.style.display = "";
        });
    },

    /**
     * Hide the matching elements
     *
     * @param selector: the selector
     */
    hide: function(selector) {
        MochiKit.Iter.forEach(this.select(selector), function(e) {
            e.style.display = "none";
        });
    },

    /**
     * Get/Set innerHTML of the matching elements.
     *
     * It also ensures to execute emebed JavaScript within
     * the given html text.
     *
     * @param selector: the selector
     * @params html: the html to set
     */
    html: function(selector, html) {
        var elems = this.select(selector);

        if (elems.length == 0) {
            return "";
        }

        if (typeof(html) != "string") {
            return elems[0].innerHTML;
        }

        MochiKit.Iter.forEach(elems, function(e) {
            e.innerHTML = html;
            //TODO: evaluate embeded javascript
        });
    },

    /**
     * Get/Set text by stripping out DOM tags of the matching elements
     *
     * @param selector: the selector
     * @param text: the text value
     */
    text: function(selector, text) {
        var elems = this.select(selector);

        if (elems.length == 0) {
            return "";
        }

        if (typeof(text) != "string") {
            return MochiKit.DOM.scrapeText(elems[0]);
        }

        MochiKit.Iter.forEach(elems, function(e) {
            e.innerHTML = MochiKit.DOM.escapeHTML(text);
        });
    }
};


// vim: ts=4 sts=4 sw=4 si et


