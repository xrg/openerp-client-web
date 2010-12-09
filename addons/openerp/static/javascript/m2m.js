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
        this.model = getNodeAttribute(this.id, 'relation');

        this.hasList = openobject.dom.get(name + '_container') ? true : false;

        MochiKit.Signal.connect(this.id, 'onchange', this, this.onChange);
        MochiKit.Signal.connect(this.text, 'onchange', this, this.onChange);

        if (!this.hasList) {
            MochiKit.Signal.connect(this.text, 'onkeydown', bind(function(evt) {
                var key = evt.event().keyCode;

                if (key == 8 || key == 46) {
                    evt.stop();
                    this.id.value = '';
                    this.onChange();
                }

                if (key == 113) {
                    evt.stop();
                    this.onClick();
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

        if (this.hasList) {

            this.terp_ids.value = '[' + ids.join(',') + ']';
            this.id.value = '[' + ids.join(',') + ']';

            ListView(this.name).reload();

        } else {
            this.text.value = '(' + ids.length + ')';
            this.id.value = '[' + ids.join(',') + ']';
            openobject.dom.get(this.name).value = ids;
        }

        if (getNodeAttribute(this.id, 'callback')) {
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
        var boxes = ListView(this.name).getSelectedItems();

        if (boxes.length <= 0 && !remove_id)
            return;

        boxes = MochiKit.Base.map(function(box) {
            return parseInt(box.value);
        }, boxes);

        var removed_ids = remove_id ? [remove_id] : boxes;
        ids = MochiKit.Base.filter(function(id) {
            return MochiKit.Base.findIdentical(removed_ids, id) == -1;
        }, ids);

        this.id.value = this.terp_ids.value = '[' + ids.join(',') + ']';
        this.onChange();
    },

    setReadonly: function(readonly) {

        var field = jQuery('[id="'+this.name +'"]') || this.id;
        field.attr('readOnly', readonly);
        this.text.readOnly = readonly;

        if (readonly) {
            jQuery(field).addClass('readonlyfield');
            jQuery(this.text).addClass('readonlyfield');

        } else {
            jQuery(field).removeClass('readonlyfield');
            jQuery(this.text).removeClass('readonlyfield');
        }
    }
};
