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

var InfoBox = function(source) {
    this.__init__(source);
};

InfoBox.prototype = {

    __init__ : function(source) {

        this.source = source;
        this.layer = openobject.dom.get('calInfoLayer');
        this.box = openobject.dom.get('calInfoBox');

        var btnCancel = BUTTON({'class': 'button', 'type': 'button'}, 'Cancel');
        var btnEdit = BUTTON({'class': 'button', 'type': 'button'}, 'Edit');
        var btnDelete = BUTTON({'class': 'button', 'type': 'button'}, 'Delete');

        MochiKit.Signal.connect(btnCancel, 'onclick', this, 'hide');
        MochiKit.Signal.connect(btnEdit, 'onclick', this, 'onEdit');
        MochiKit.Signal.connect(btnDelete, 'onclick', this, 'onDelete');

        var title = 'Information Box';

        if (this.source instanceof openobject.workflow.StateOval || this.source instanceof openobject.workflow.StateRectangle) {
            var id = 'Id: ' + this.source.get_act_id();
        } else {
            var id = this.source.from + ' ---> ' + this.source.to;
        }

        var dtls = [];
        var options = this.source.options;
        for (f in options)
            dtls.push(DIV({'class': 'calInfoDesc'}, f + ': ' + options[f]))

        var info = DIV(null,
                DIV({'class': 'calInfoTitle'}, title),
                DIV({'id': 'info'},
                        DIV({'class': 'calInfoDesc'}, id),
                        map(function(x) {
                            return x
                        }, dtls)),
                TABLE({'class': 'calInfoButtons', 'cellpadding': 2},
                        TBODY(null,
                                TR(null,
                                        TD(null, btnEdit),
                                        TD(null, btnDelete),
                                        TD({'align': 'right', 'width': '100%'}, btnCancel)))));

        if (getElement('_terp_editable').value == 'False') {
            removeElement(btnEdit);
            removeElement(btnDelete)
        }

        if (!this.layer) {
            this.layer = DIV({id: 'calInfoLayer'});
            MochiKit.DOM.appendChildNodes(document.body, this.layer);
            setOpacity(this.layer, 0.3);
            connect(this.layer, 'onclick', this, 'hide');
        }

        if (!this.box) {
            this.box = DIV({id: 'calInfoBox'});
            MochiKit.DOM.appendChildNodes(document.body, this.box);
        }

        this.box.innerHTML = "";
        MochiKit.DOM.appendChildNodes(this.box, info);
    },

    show : function(evt) {

        MochiKit.DOM.setElementDimensions(this.layer, elementDimensions(document.body));
        //setElementDimensions(this.layer, getViewportDimensions());

        var w = 350;
        var h = elementDimensions('info').h > 0 ? elementDimensions('info').h + 53 : 125;

        MochiKit.DOM.setElementDimensions(this.box, {w: w, h: h});

        var x = evt.mouse().page.x;
        var y = evt.mouse().page.y;

        x -= w / 2;
        y -= h - h / 3;

        var vd = elementDimensions(document.body);
        var md = elementDimensions(this.box);

        if ((x + md.w) > vd.w) {
            x -= x + md.w - vd.w;
        }

        x = Math.max(0, x);
        y = Math.max(0, y);

        MochiKit.DOM.setElementPosition(this.box, {x: x, y: y});

        MochiKit.DOM.showElement(this.layer);
        MochiKit.DOM.showElement(this.box);
    },

    hide : function(evt) {
        MochiKit.DOM.hideElement(this.box);
        MochiKit.DOM.hideElement(this.layer);
    },

    onEdit : function() {
        this.hide();
        this.source.edit();
    },

    onDelete : function() {

        this.hide();
        if (!confirm(_('Do you really want to delete this record?'))) {
            return false;
        }
        WORKFLOW.remove_elem(this.source);
    }
};
