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

        this.btnAdd = openobject.dom.get(name + '_button1');

        this.terp_ids = openobject.dom.get(name + '/_terp_ids');
        this.model = jQuery(this.id).attr('relation');

        this.hasList = !!openobject.dom.get(name + '_container');

        jQuery([this.id, this.text]).change(jQuery.proxy(this, 'onChange'));

        if (!this.hasList) {
            jQuery(this.text).keydown(jQuery.proxy(function(evt) {
                switch (evt.which) {
                    case 8:
                    case 46:
                        this.id.value = '';
                        this.onChange();
                        return false;
                    case 113:
                        this.onClick();
                        return false;
                }
            }, this));
        }

        // save the reference
        openobject.dom.get(name)._m2m = this;
    },

    onClick: function() {
        this.btnAdd.onclick();
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
    },

    setReadonly: function(readonly) {
        var $field = jQuery(idSelector(this.name));
        if(!$field.length) $field = jQuery(this.id);
        $field.add(this.text)
                .attr('readOnly', readonly)
                .toggleClass('readonlyfield', readonly);
    }
};
