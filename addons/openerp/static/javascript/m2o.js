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

    this.hiddenField = null;
    this.selectedResultRow = 0;
    this.numResultRows = 0;
    this.specialKeyPressed = false;
    this.isShowingResults = false;
    this.lastKey = null;
    this.delayedRequest = null;
    this.completeDelay = 1;
    this.hasHiddenValue = false;
    this.lastTextResult = null;
    this.lastHiddenResult = null;
    this.lastSearch = null;
    this.onlySuggest = false;
    this.minChars = 1;
    this.processCount = 0;
    this.takeFocus = false;
    this.hasFocus = false;
    this.suggestionBoxMouseOver = false;
    this.selectedResult = false;

    this.select_img = openobject.dom.get(name + '_select');
    this.open_img = openobject.dom.get(name + '_open');
    this.reference = openobject.dom.get(name + '_reference'); // reference widget

    this.callback = jQuery(this.field).attr('callback');
    this.relation = jQuery(this.field).attr('relation');
    jQuery(this.text).attr('autocomplete', 'OFF');

    if(this.editable) {
        connect(this.field, 'onchange', this, this.on_change);
        //connect(this.text, 'onchange', this, this.on_change_text);
        connect(this.text, 'onkeydown', this, this.on_keydown);
        connect(this.text, 'onkeypress', this, this.on_keypress);
        connect(this.text, 'onkeyup', this, this.on_keyup);
        connect(this.text, 'onfocus', this, this.gotFocus);
        connect(this.text, 'onblur', this, this.lostFocus);

        if(this.hiddenField)
            this.lastHiddenResult = this.field.value;
        this.lastTextResult = this.text.value;

        if(this.select_img)
            connect(this.select_img, 'onclick', this, this.select);
        if(this.open_img)
            connect(this.open_img, 'onclick', this, function(evt) {
                on_context_menu(evt, this.text);
            });

        if(this.reference) {
            connect(this.reference, 'onchange', this, this.on_reference_changed);
        }

        this.is_inline = name.indexOf('_terp_listfields/') == 0;

        this.field._m2o = this;

        this.change_icon();

        if(this.takeFocus) {
            this.text.focus();
            this.gotFocus();
        }
        bindMethods(this);
    }
};

ManyToOne.prototype.gotFocus = function(evt) {
    this.hasFocus = true;
    if(!this.minChars) this.on_keyup(evt);
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
        openobject.tools.openWindow(openobject.http.getURL('/openerp/openm2o/edit', {
            _terp_model: model, _terp_id: id,
            _terp_domain: obj.domain, _terp_context: obj.context,
            _terp_m2o: source, _terp_editable: editable ? 'True' : 'False'}));
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
    jQuery(this.field).attr('relation', this.relation);
    jQuery(this.text).attr('relation', this.relation);

    this.change_icon();
};

ManyToOne.prototype.change_icon = function() {
    if(!this.field.value && this.open_img) {
        this.open_img.style.cursor = '';
    }

    if(this.is_inline && this.open_img) {
        if(this.field.value) {
            jQuery(this.select_img).hide();
            jQuery(this.open_img).show();
        } else {
            jQuery(this.select_img).show();
            jQuery(this.open_img).hide();
        }
    }
};

ManyToOne.prototype.on_keyup = function() {
    // Stop processing if a special key has been pressed. Or if the last search requested the same string
    if(this.specialKeyPressed || (this.text.value == this.lastSearch)) return false;

    if(this.minChars && this.text.value.length < this.minChars) {
        if(this.delayedRequest) {
            this.delayedRequest.cancel();
            this.clearResults();
            return false;
        }
    }
    if(this.delayedRequest) this.delayedRequest.cancel();

    this.delayedRequest = callLater(this.completeDelay, this.doDelayedRequest);
    if(this.auto_hidden_id) {
        if(this.lastTextResult == this.text.value)
            this.auto_hidden_id.value = this.lastHiddenResult;
        else
            this.auto_hidden_id.value = '';
    }
    return true;
};

ManyToOne.prototype.on_keydown = function(evt) {
    var event = evt.event() || window.evt.event();

    var key = event.keyCode || event.which;
    this.lastKey = key;
    // Used to stop processing of further key functions
    this.specialKeyPressed = false;

    if(evt.src()) {
        if(evt.target().tagName == 'INPUT') {
            var w;
            //IMP: jQuery('#this.name_select') will not work because of '/' in id.
            if(jQuery('#search_filter_data').is(':visible')) {
                w = jQuery(evt.src()).width()
            } else {
                w = jQuery(evt.src()).width() + jQuery('[id="' + this.name + '_select' + '"]').width();
            }
            jQuery('div.autoTextResults[id$="' + this.name + '"]').width(w)
        }
    }

    if(this.numResultRows > 0) {
        switch (key) {
            // Enter Key
            //Single Click
            case 13:
            case 1:
                var autoCompleteSelectedRow = openobject.dom.get("autoComplete" + this.name + "_" + this.selectedResultRow);
                if(this.onlySuggest && autoCompleteSelectedRow == null) {
                    this.clearResults();
                    break;
                }

                var theCell = openobject.dom.select("TD", autoCompleteSelectedRow)[0];

                var theCellHidden;
                theCellHidden = openobject.dom.select("TD", null, autoCompleteSelectedRow)[0];

                var autoCompleteText = scrapeText(theCell);
                var autoCompleteHidden = scrapeText(theCellHidden);

                this.field.value = theCell.id;
                this.text.value = autoCompleteText;

                if(this.callback) {
                    onChange(this.name);
                }
                this.change_icon();
                //this.on_change();
                this.lastTextResult = autoCompleteText;
                if(this.hiddenField)
                    this.hiddenField.value = autoCompleteHidden;
                this.lastHiddenResult = autoCompleteHidden;
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

        if(key == 13 || key == 27 || key == 38 || key == 40)
            this.specialKeyPressed = true;
    }

    if((key == 8 || key == 46) && this.field.value) {
        this.text.value = '';
        this.field.value = '';
        this.on_change(evt);
    }

    //Tab
    if((key == 9) && this.text.value && !this.field.value) {
        this.get_matched();
    }

    // F1
    if(key == 112) {
        this.create(evt);
        evt.stop();
    }

    // F2
    if(key == 113 || (key == 13 && !this.text.value && !jQuery(this.text).hasClass('listfields'))) {
        this.select(evt);
        evt.stop();
    }

    return !this.specialKeyPressed;
};

ManyToOne.prototype.on_keypress = function(evt) {
    if(evt.event().keyCode == 9 || evt.modifier().ctrl) {
        return;
    }

    if((this.field.value && evt.key().string) || evt.event().keyCode == 13) {
        evt.stop();
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
    this.field.readOnly = readonly;
    this.field.disabled = readonly;
    this.text.readOnly = readonly;
    this.text.disabled = readonly;

    if(readonly) {
        jQuery(this.field).addClass('readonlyfield');
        jQuery(this.text).addClass('readonlyfield');
    } else {
        jQuery(this.field).removeClass('readonlyfield');
        jQuery(this.text).removeClass('readonlyfield');
    }
};

ManyToOne.prototype.clearResults = function() {
    // Hide all the results
    hideElement(openobject.dom.get("autoCompleteResults_" + this.name));
    // Clear out our result tracking
    this.selectedResultRow = 0;
    this.numResultRows = 0;
    this.lastSearch = null;
};

ManyToOne.prototype.doDelayedRequest = function () {
    this.delayedRequest = null;
    var s = this.text.value;
    var val = s.lastIndexOf(',') >= 0 ? s.substring(s.lastIndexOf(',') + 1).replace(/^\s+|\s+$/g, "") : s.replace(/^\s+|\s+$/g, "");

    // Check again if less than required chars, then we won't search.
    if(this.minChars && val.length < this.minChars) {
        this.clearResults();
        return false;
    }

    // Get what we are searching for
    this.processCount++;

    this.lastSearch = this.text.value;
    jQuery.getJSON('/openerp/search/get_matched', {
        text: val,
        model: this.relation
    }, jQuery.proxy(this, 'displayResults'));
    return true;
};

ManyToOne.prototype.displayResults = function(result) {
    try {
        if(!this.hasFocus) {
            this.updateSelectedResult();
            this.processCount--;
            return false;
        }

        var fancyTable = TABLE({"class": "autoTextTable","name": "autoCompleteTable" + this.name,
            "id": "autoCompleteTable" + this.name}, null);
        var fancyTableBody = TBODY(null, null);
        this.numResultRows = result.values.length;

        if(this.onlySuggest)
            this.selectedResultRow = null;
        else
            this.selectedResultRow = 0;

        this.isShowingResults = false;


        for(var i = 0; i <= (result.values.length - 1); i++) {
            var currentItem = result.values[i][1];

            var currentRow = TR({"class": "autoTextNormalRow", "name": "autoComplete" + this.name + "_" + i, "id": "autoComplete" + this.name + "_" + i},
                    TD({'id':result.values[i][0], 'class': 'm2o_coplition'},
                            createDOM("nobr", null, SPAN({'id':result.values[i][0], 'style':'text-transform:none;', 'title': currentItem}, currentItem))));

            connect(currentRow, 'onmouseover', this, this.getMouseover);
            connect(currentRow, 'onclick', this, this.getOnclick);
            appendChildNodes(fancyTableBody, currentRow);

            this.isShowingResults = true;
        }
        appendChildNodes(fancyTable, fancyTableBody);
        // Swap out the old results with the newly created table
        var resultsHolder = openobject.dom.get("autoCompleteResults_" + this.name);
        if(this.isShowingResults) {
            replaceChildNodes(resultsHolder, fancyTable);
            this.updateSelectedResult();
            showElement(resultsHolder);
        }
        else
            hideElement(resultsHolder);

        this.processCount--;
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
                var theCellHidden = $selectedRow.find('TD')[0];

                var autoCompleteText = jQuery($selectedRow.find('TD')[0]).find('span').text();
                var autoCompleteHidden = jQuery(theCellHidden).find('span').text();

                this.field.value = $selectedRow.find('TD')[0].id;
                this.text.value = autoCompleteText;
                this.lastTextResult = autoCompleteText;
                if(this.hiddenField)
                    this.hiddenField.value = autoCompleteHidden;
                this.lastHiddenResult = autoCompleteHidden;
            }
        }
        else
            $selectedRow.swapClass("autoTextSelectedRow", "autoTextNormalRow");
    }
};

ManyToOne.prototype.getMouseover = function(evt) {
    var target = evt.src().id;
    var id = target.split(this.name + "_")[1];
    this.selectedResult = false;
    this.suggestionBoxMouseOver = true;
    this.selectedResultRow = id;
    this.updateSelectedResult();
};

ManyToOne.prototype.getOnclick = function(evt) {
    evt.event().keyCode = 13;
    this.on_keydown(evt);
};
