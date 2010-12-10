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

var Many2Many = function(name) {

    var elem = openobject.dom.get(name);
    if (elem._m2m) {
        return elem._m2m;
    }

    var cls = arguments.callee;
    if (!(this instanceof cls)) {
        return new cls(name);
    }

    this.__init__(name);
};

Many2Many.prototype = {

    __init__: function(name) {

        this.name = name;

        this.id = openobject.dom.get(name + '_id');
        this.text = openobject.dom.get(name + '_set');

        this.terp_ids = openobject.dom.get(name + '/_terp_ids');

        this.hasList = !!openobject.dom.get(name + '_container');

        jQuery([this.id, this.text]).change(jQuery.proxy(this, 'onChange'));

        jQuery(idSelector('_m2m_' + this.name)).delegate(
            idSelector(this.name + '_add_records'), 'click', jQuery.proxy(this, 'addRecords')
        ).delegate(
            idSelector(this.name + '_delete_record'), 'click', jQuery.proxy(this, 'remove')
        );

        if (!this.hasList) {
            jQuery(this.text).keydown(jQuery.proxy(function(evt) {
                switch (evt.which) {
                    case 8:
                    case 46:
                        this.id.value = '';
                        this.onChange();
                        return false;
                    case 113:
                        this.addRecords();
                        return false;
                }
            }, this));
        }

        // save the reference
        openobject.dom.get(name)._m2m = this;
    },

    onChange: function() {
        this.setValue(this.id.value);
    },

    selectAll: function() {
        if (this.hasList) {
            ListView(this.name).checkAll();
        }
    },

    setValue: function(ids) {
        ids = /^\[.*\]/.test(ids) ? ids : '[' + ids + ']';
        ids = eval(ids);

        var $id = jQuery(this.id).val('[' + ids.join(',') + ']');
        if (this.hasList) {
            jQuery(this.terp_ids).val('[' + ids.join(',') + ']');
            ListView(this.name).reload();
        } else {
            jQuery(this.text).val('(' + ids.length + ')');
            jQuery(idSelector(this.name)).val(ids);
        }

        if ($id.attr('callback')) {
            onChange(this.id);
        }
    },

    getValue: function() {
        var ids = this.hasList ? this.terp_ids.value : this.id.value;
        try {
            var res = eval(ids);
            if (res.length)
                return res;
        } catch(e) {
        }

        return [];
    },

    remove: function(remove_id) {
        var ids = eval(this.terp_ids.value) || [];
        var $selectedItems = ListView(this.name).$getSelectedItems();

        if (!(remove_id || $selectedItems.length)) {
            return;
        }

        var ids_to_remove = remove_id ? [remove_id]
                                      : $selectedItems.map(function() {return parseInt(this.value, 10);}).get();

        ids = jQuery.grep(ids, function(id) {
            return jQuery.inArray(id, ids_to_remove) == -1;
        });

        jQuery([this.id, this.terp_ids]).val('[' + ids.join(',') + ']');
        this.onChange();
        return false;
    },

    setReadonly: function(readonly) {
        var $field = jQuery(idSelector(this.name));
        if(!$field.length) $field = jQuery(this.id);
        $field.add(this.text)
                .attr('readOnly', readonly)
                .toggleClass('readonlyfield', readonly);
    },

    addRecords: function () {
        var $this = jQuery(idSelector('_m2m_' + this.name));
        open_search_window(
                $this.attr('relation'),
                $this.attr('domain'),
                $this.attr('context'),
                this.name, 2,
                jQuery(idSelector(this.name + '_set')).val());
        return false;
    }
};

(function ($) {
    /**
     * Opens an m2m dialog linked to the provided <code>$this</code> window,
     * with the selected options.
     *
     * @param $this the parent window of the opened dialog, contains the
     * input to fill with the selected m2m value if any
     * @param options A map of options to provide to the xhr call.
     * The <code>source</code> key is also used for the id of the element
     * (in <code>$this</code>) on which any selected m2o value should be set.
     * The <code>record</code> key indicates whether a record should be opened
     * instead of a search view
     */
    function open($this, options) {
        var url;
        if(options.record) {
            url = '/openerp/openm2m/create'
        } else {
            url = '/openerp/search/new';
        }
        return $('<iframe>', {
            src: openobject.http.getURL(url, options),
            frameborder: 0
        }).data('source_window', $this[0])
          .data('source_id', options.source || null)
          .appendTo(document.documentElement)
          .dialog({
              modal: true,
              width: 640,
              height: 480,
              close: function () {
                  jQuery(this).dialog('destroy').remove();
              }
          });
    }

    /**
     * Closes the m2m dialog it was called from (represented by
     * <code>$this</code>, setting the related m2m input to the provided
     * <code>value</code>, if any.
     *
     * @param $this the window of the dialog to close
     * @param values optional, the values to add to the m2m
     */
    function close($this, values) {
        var $frame = $($this.attr('frameElement'));

        if(values && values.length) {
            var original_window = $frame.data('source_window');
            // the m2m input to set is in the source_window, which is set as
            // a `data` of the dialog iframe
            var Many2Many = original_window.Many2Many;
            var source_id = $frame.data('source_id');

            var m2m = Many2Many(source_id);
            var ids = m2m.getValue();
            m2m.setValue(
                ids.concat(jQuery.grep(values, function (value) {
                    return (jQuery.inArray(value, ids) == -1);
            })));
        }

        $frame.dialog('close');
        return null;
    }

    /**
     * Manage m2m dialogs for this scope
     * <ul>
     *  <li><p>Called with only options, opens a new m2m dialog linking to the
     *         current scope.</p></li>
     *  <li><p>Called with the <code>"close"</code> command, closes the m2m
     *         dialog it was invoked from and focuses its parent scope.
     *  </p></li>
     *  <li><p>Called with the <code>"close"</code> command and an argument,
     *         sets that argument as the m2m value of the parent widget and
     *         closes the m2m dialog it was invoked from as above.
     *  </p></li>
     * </ul>
     *
     * @returns the m2m container (iframe) if one was created
     */
    $.m2m = function () {
        // $this should be the holder for the window from which $.m2m was
        // originally called, even if $.m2m() was bubbled to the top of
        // the window stack.
        var $this;
        if(this == $) $this = $(window);
        else $this = $(this);
        if(window != window.top) {
            return window.top.jQuery.m2m.apply($this[0], arguments);
        }
        // We're at the top-level window, $this is the window from which the
        // original $.m2m call was performed, window being the current window
        // level.
        if(arguments[0] === "close") {
            return close($this, arguments[1]);
        } else {
            return open($this, arguments[0]);
        }
    };
})(jQuery);
