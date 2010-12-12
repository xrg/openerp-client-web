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

var ManyToOne = function(name) {
    var elem = openobject.dom.get(name);
    if(elem._m2o) {
        return elem._m2o;
    }

    var cls = arguments.callee;
    if(!(this instanceof cls)) {
        return new cls(name);
    }

    this.__init__(name);
};

ManyToOne.prototype.__init__ = function(name) {
    this.name = name;

    this.field = openobject.dom.get(name);
    this.text = openobject.dom.get(name + '_text');
    this.editable = this.field.tagName.toLowerCase() != 'span';
    //for autocomplete
    this.auto_hidden_id = openobject.dom.get('_hidden_' + name);

    this.selectedResultRow = 0;
    this.numResultRows = 0;
    this.specialKeyPressed = false;
    this.lastKey = null;
    this.delayedRequest = null;
    this.completeDelay = 1;
    this.lastTextResult = null;
    this.lastSearch = null;
    this.hasFocus = false;
    this.suggestionBoxMouseOver = false;
    this.selectedResult = false;
    this.eval_domain = null;
    this.eval_context = null;

    this.select_img = openobject.dom.get(name + '_select');
    this.open_img = openobject.dom.get(name + '_open');
    this.reference = openobject.dom.get(name + '_reference'); // reference widget

    this.callback = jQuery(this.field).attr('callback');
    this.relation = jQuery(this.field).attr('relation');
    jQuery(this.text).attr('autocomplete', 'OFF');

    if(this.editable) {
        jQuery(this.field).change(jQuery.proxy(this, 'on_change'));
        jQuery(this.text).bind({
            keydown: jQuery.proxy(this, 'on_keydown'),
            keypress: jQuery.proxy(this, 'on_keypress'),
            keyup: jQuery.proxy(this, 'on_keyup'),
            focus: jQuery.proxy(this, 'gotFocus'),
            blur: jQuery.proxy(this, 'lostFocus')
        });

        this.lastTextResult = this.text.value;

        if(this.select_img)
            jQuery(this.select_img).click(jQuery.proxy(this, 'select'));
        if(this.open_img)
            jQuery(this.open_img).click(jQuery.proxy(function(evt) {
                on_context_menu(evt, this.text);
            }, this));

        if(this.reference) {
            jQuery(this.reference).change(jQuery.proxy(this, 'on_reference_changed'));
        }

        this.is_inline = name.indexOf('_terp_listfields/') == 0;

        this.field._m2o = this;

        this.change_icon();
    }
};

ManyToOne.prototype.gotFocus = function(evt) {
    this.hasFocus = true;
};

ManyToOne.prototype.lostFocus = function() {
    this.hasFocus = false;

    if(this.selectedResult) {
        this.lastKey = null;
        this.clearResults();
    }

    if(!this.suggestionBoxMouseOver || this.lastKey == 9) {
        this.lastKey = null;
        this.clearResults();
    }
};

ManyToOne.prototype.select = function() {
    if(this.field.disabled) {
        return;
    }
    if(!jQuery(this.field).hasClass('readonlyfield')) {
        this.get_matched();
    }
};

ManyToOne.prototype.open_record = function() {
    this.field.value = this.field.value || jQuery(this.field).attr('value');
    if(this.field.value) {
        this.open(this.field.value);
    }
};

ManyToOne.prototype.create = function() {
    this.open();
};

ManyToOne.prototype.open = function(id) {
    var domain = jQuery(this.field).attr('domain');
    var context = jQuery(this.field).attr('context');

    var model = this.relation;
    var source = this.name;

    var editable = this.editable;
    if(editable && jQuery(this.field).hasClass('readonlyfield')) {
        editable = false;
    }

    eval_domain_context_request({
        source: source,
        domain: domain,
        context: context
    }).addCallback(function(obj) {
        $.m2o({
            record: true,
            _terp_model: model,
            _terp_id: id,
            _terp_domain: obj.domain,
            _terp_context: obj.context,
            _terp_m2o: source,
            _terp_editable: editable ? 'True' : 'False'
        });
    });
};

ManyToOne.prototype.get_text = function() {
    if(!this.text) { return; }
    if(!this.field.value) {
        this.text.value = '';
    } else {
        var text_field = this.text;

        jQuery.post('/openerp/search/get_name', {
            model: this.relation,
            id : this.field.value
        }, function(obj) {
            text_field.value = obj.name;
        }, 'json');
    }
};

ManyToOne.prototype.on_change = function(evt) {
    this.get_text(evt);

    if(this.callback) {
        onChange(this.name);
    }

    this.change_icon();
};

ManyToOne.prototype.on_change_text = function(evt) {
    if(this.text.value == '') {
        this.field.value = '';
        this.on_change(evt);
    } else {
        this.get_text();
    }
};

ManyToOne.prototype.on_reference_changed = function() {
    this.text.value = '';
    this.field.value = '';

    this.relation = this.reference.value;
    this.clearResults();
    jQuery([this.field, this.text]).attr('relation', this.relation);

    this.change_icon();
};

ManyToOne.prototype.change_icon = function() {
    if(!this.field.value && this.open_img) {
        this.open_img.style.cursor = '';
    }

    if(this.is_inline && this.open_img) {
        jQuery(this.select_img).toggle(!this.field.value);
        jQuery(this.open_img).toggle(!!this.field.value);
    }
};

ManyToOne.prototype.on_keyup = function() {
    // Stop processing if a special key has been pressed. Or if the last search requested the same string
    if(this.specialKeyPressed || (this.text.value == this.lastSearch)) return false;

    if(!this.text.value.length) {
        if(this.delayedRequest) {
            this.delayedRequest.cancel();
            this.clearResults();
            return false;
        }
    }
    if(this.delayedRequest) this.delayedRequest.cancel();

    this.delayedRequest = callLater(this.completeDelay, jQuery.proxy(this, 'doDelayedRequest'));
    if(this.auto_hidden_id) {
        if(this.lastTextResult == this.text.value)
            this.auto_hidden_id.value = this.lastTextResult;
        else
            this.auto_hidden_id.value = '';
    }
    return true;
};

ManyToOne.prototype.setCompletionText = function ($selectedRow) {
    var $cell = $selectedRow.find('td');

    var autoCompleteText = $cell.find('span').text();

    this.field.value = $cell.attr('data-id');
    this.text.value = autoCompleteText;
    this.lastTextResult = autoCompleteText;
};

ManyToOne.prototype.on_keydown = function(evt) {
    this.lastKey = evt.which;
    // Used to stop processing of further key functions
    this.specialKeyPressed = false;
    if(evt.currentTarget) {
        if(evt.target.tagName.toLowerCase() == 'input') {
            var w;
            if(jQuery('#search_filter_data').is(':visible')) {
                w = jQuery(evt.currentTarget).width()
            } else {
                w = jQuery(evt.currentTarget).width() + jQuery(idSelector(this.name + '_select')).width();
            }
            jQuery('div.autoTextResults[id$="' + this.name + '"]').width(w)
        }
    }

    if(this.numResultRows > 0) {
        switch (evt.which) {
            // Enter Key
            //Single Click
            case 13:
            case 1:
                var $selectedRow = jQuery(idSelector("autoComplete" + this.name + "_" + this.selectedResultRow));

                this.setCompletionText($selectedRow);

                if(this.callback) {
                    onChange(this.name);
                }
                this.change_icon();
                this.clearResults();
                break;

            // Escape Key
            case 27:
                this.clearResults();
                break;

            // Up Key
            case 38:
                if(this.selectedResultRow > 0) this.selectedResultRow--;
                this.updateSelectedResult();
                break;

            // Down Key
            case 40:
                if(this.selectedResultRow < this.numResultRows - (this.selectedResultRow == null ? 0 : 1)) {
                    if(this.selectedResultRow == null)
                        this.selectedResultRow = 0;
                    else
                        this.selectedResultRow++;
                }
                this.selectedResult = true;
                this.updateSelectedResult();
                break;

            default:
            //pass
        }

        if(evt.which == 13 || evt.which == 27 || evt.which == 38 || evt.which == 40)
            this.specialKeyPressed = true;
    }

    if((evt.which == 8 || evt.which == 46) && this.field.value) {
        this.text.value = '';
        this.field.value = '';
        this.on_change(evt);
    }

    //Tab
    if((evt.which == 9) && this.text.value && !this.field.value) {
        this.get_matched();
    }

    // F1
    if(evt.which == 112) {
        this.create(evt);
        evt.stopPropagation();
        evt.preventDefault();
    }

    // F2
    if(evt.which == 113 || (evt.which == 13 && !this.text.value && !jQuery(this.text).hasClass('listfields'))) {
        this.select(evt);
        evt.stopPropagation();
        evt.preventDefault();
    }

    return !this.specialKeyPressed;
};

ManyToOne.prototype.on_keypress = function(evt) {
    if(evt.which == 9 || evt.ctrlKey) {
        return;
    }

    if((this.field.value && String.fromCharCode(evt.which)) || evt.which == 13) {
        evt.stopPropagation();
        evt.preventDefault();
    }
};

ManyToOne.prototype.get_matched = function() {
    if(openobject.http.AJAX_COUNT > 0) {
        return callLater(1, this.get_matched);
    }

    if(!this.relation) {
        return;
    }

    var m2o = this;

    var domain = jQuery(this.field).attr('domain');
    var context = jQuery(this.field).attr('context');

    eval_domain_context_request({
        source: this.name,
        domain: domain,
        context: context
    }).addCallback(function(obj) {
        var text = m2o.field.value ? '' : m2o.text.value;

        jQuery.post(
            '/openerp/search/get_matched', {
                model: m2o.relation,
                text: text,
                _terp_domain: obj.domain,
                _terp_context: obj.context
            }, function(matches) {
                if(matches.error) {
                    return error_display(matches.error);
                }
                if(text && matches.values.length == 1) {
                    var val = matches.values[0];
                    m2o.field.value = val[0];
                    m2o.text.value = val[1];
                    m2o.on_change();
                } else {
                    open_search_window(m2o.relation, domain, context, m2o.name, 1, text);
                }
            }, 'json');
    });
};

ManyToOne.prototype.setReadonly = function(readonly) {
    jQuery([this.field, this.text])
            .attr({'readOnly': readonly,
                   'disabled': readonly})
            .toggleClass('readonly', !!readonly);
};

ManyToOne.prototype.clearResults = function() {
    // Hide all the results
    jQuery(idSelector("autoCompleteResults_" + this.name)).hide();
    // Clear out our result tracking
    this.selectedResultRow = 0;
    this.numResultRows = 0;
    this.lastSearch = null;
    this.eval_domain = null;
    this.eval_context = null;
};

ManyToOne.prototype.doDelayedRequest = function () {
    this.delayedRequest = null;
    var s = this.text.value;
    var val = s.lastIndexOf(',') >= 0 ? s.substring(s.lastIndexOf(',') + 1).replace(/^\s+|\s+$/g, "") : s.replace(/^\s+|\s+$/g, "");

    // Check again if less than required chars, then we won't search.
    if(!val.length) {
        this.clearResults();
        return false;
    }

    // Get what we are searching for
    this.lastSearch = this.text.value;
    if (this.numResultRows==0) {
        var self = this;
        var req = eval_domain_context_request({source: this.name, domain: getNodeAttribute(this.field, 'domain'), context: getNodeAttribute(this.field, 'context')});
        req.addCallback(function(obj) {
            self.eval_domain = obj.domain;
            self.eval_context = obj.context

            jQuery.getJSON('/openerp/search/get_matched', {
                text: val,
                model: self.relation,
                _terp_domain: self.eval_domain,
                _terp_context: self.eval_context
            }, jQuery.proxy(self, 'displayResults'));
        });
    }
    else {
        jQuery.getJSON('/openerp/search/get_matched', {
                text: val,
                model: this.relation,
                _terp_domain: this.eval_domain,
                _terp_context: this.eval_context
            }, jQuery.proxy(this, 'displayResults'));
    }
    return true;
};

ManyToOne.prototype.displayResults = function(result) {
    try {
        if(!this.hasFocus) {
            this.updateSelectedResult();
            return false;
        }

        var $fancyTable = jQuery('<table>', {
            "class": "autoTextTable",
            "name": "autoCompleteTable" + this.name,
            "id": "autoCompleteTable" + this.name});
        this.numResultRows = result.values.length;

        this.selectedResultRow = 0;

        var mouseOver = jQuery.proxy(this, 'getMouseover');
        var onClick = jQuery.proxy(this, 'getOnclick');
        var rowName = "autoComplete" + this.name + "_";
        var $resultsTable = jQuery('<tbody>').appendTo($fancyTable);
        jQuery.each(result.values, function (i, currentObject) {
            jQuery('<tr>', {
                "class": "autoTextNormalRow",
                "name": rowName + i,
                "id": rowName + i,
                "mouseover": mouseOver,
                "click": onClick
            }).append(jQuery('<td>', {
                'data-id':currentObject[0],
                'class': 'm2o_coplition'
            }).append(jQuery('<span>', {
                'style':'text-transform:none; white-space: nowrap',
                'title': currentObject[1],
                'text': currentObject[1]
            }))).appendTo($resultsTable);
        });
        // Swap out the old results with the newly created table
        var $resultsHolder = jQuery(idSelector("autoCompleteResults_" + this.name));
        if($resultsTable.children().length) {
            $resultsHolder.empty().append($fancyTable);
            this.updateSelectedResult();
            $resultsHolder.show();
        } else {
            $resultsHolder.hide();
        }

        return true;
    }
    catch(e) {
        error_display('error in display::' + e)
    }
};

ManyToOne.prototype.updateSelectedResult = function() {
    // Set classes to show currently selected row
    for(var i = 0; i < this.numResultRows; i++) {
        var $selectedRow = jQuery(idSelector('autoComplete' + this.name + '_' + i));
        if(this.selectedResultRow == i) {
            $selectedRow.swapClass("autoTextNormalRow", "autoTextSelectedRow");

            if (this.selectedResult) {
                this.setCompletionText($selectedRow);
            }
        } else {
            $selectedRow.swapClass("autoTextSelectedRow", "autoTextNormalRow");
        }
    }
};

ManyToOne.prototype.getMouseover = function(evt) {
    var target = evt.currentTarget.id;
    var id = target.split(this.name + "_")[1];
    this.selectedResult = false;
    this.suggestionBoxMouseOver = true;
    this.selectedResultRow = id;
    this.updateSelectedResult();
};

ManyToOne.prototype.getOnclick = function(evt) {
    evt.which = 13;
    this.on_keydown(evt);
};

(function ($) {
    /**
     * Opens an m2o dialog linked to the provided <code>$this</code> window,
     * with the selected options.
     *
     * @param $this the parent window of the opened dialog, contains the
     * input to fill with the selected m2o value if any
     * @param options A map of options to provide to the xhr call.
     * The <code>source</code> key is also used for the id of the element
     * (in <code>$this</code>) on which any selected m2o value should be set.
     * The <code>record</code> key indicates whether a record should be opened
     * instead of a search view
     */
    function open($this, options) {
        var url;
        if(options.record) {
            url = '/openerp/openm2o/edit'
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
     * Closes the m2o dialog it was called from (represented by
     * <code>$this</code>, setting the related m2o input to the provided
     * <code>value</code>, if any.
     *
     * @param $this the window of the dialog to close
     * @param value optional, the value to set the m2o input to if it is
     * provided
     */
    function close($this, value) {
        var $frame = $($this.attr('frameElement'));
        if(value) {
            // the m2o input to set is in the source_window, which is set as
            // a `data` of the dialog iframe
            var jQ = $frame.data('source_window').jQuery;
            var source_id = $frame.data('source_id');
            jQ(idSelector(source_id + '_text')).val('');
            var $m2o_field = jQ(idSelector(source_id)).val(value);

            if($m2o_field[0].onchange) {
                $m2o_field[0].onchange();
            } else {
                $m2o_field.change();
            }
        }
        $frame.dialog('close');
        return null;
    }

    /**
     * Manage m2o dialogs for this scope
     * <ul>
     *  <li><p>Called with only options, opens a new m2o dialog linking to the
     *         current scope.</p></li>
     *  <li><p>Called with the <code>"close"</code> command, closes the m2o
     *         dialog it was invoked from and focuses its parent scope.
     *  </p></li>
     *  <li><p>Called with the <code>"close"</code> command and an argument,
     *         sets that argument as the m2o value of the parent widget and
     *         closes the m2o dialog it was invoked from as above.
     *  </p></li>
     * </ul>
     *
     * @returns the m2o container (iframe) if one was created
     */
    $.m2o = function () {
        // $this should be the holder for the window from which $.m2o was
        // originally called, even if $.m2o() was bubbled to the top of
        // the window stack.
        var $this;
        if(this == $) $this = $(window);
        else $this = $(this);
        if(window != window.top) {
            return window.top.jQuery.m2o.apply($this[0], arguments);
        }
        // We're at the top-level window, $this is the window from which the
        // original $.m2o call was performed, window being the current window
        // level.
        if(arguments[0] === "close") {
            return close($this, arguments[1]);
        } else {
            return open($this, arguments[0]);
        }
    };
})(jQuery);
