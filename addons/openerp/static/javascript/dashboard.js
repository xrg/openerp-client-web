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

function initialize_dashboard() {
    if (window.browser.isIE) {
        return;
    }
    jQuery('div.dashbar').each(function () {
        new Droppable(this, {
            'ondrop': onDrop,
            'hoverclass': 'dashbar-hover',
            'accept': ['dashlet']});

        jQuery(this).find('div.dashlet').each(function () {
            new Draggable(this, {
                'handle': 'dashlet-drag',
                'starteffect': null,
                'endeffect': null,
                'revert': true});
        })
    });
}

function onDrop(src, dst, evt) {
    var xy = MochiKit.DOM.elementPosition(src, dst);
    var ref = null;

    var divs = openobject.dom.select('div.dashlet', dst);

    for(var i=0; i < divs.length; i++) {

        var el = divs[i];
        var dim = MochiKit.DOM.elementDimensions(el);
        var pos = MochiKit.DOM.elementPosition(el);

        if ((pos.y > xy.y) && (xy.y < (pos.y + dim.h))) {
            ref = el;
            break;
        }
    }
    dst.insertBefore(src, ref);

    src.style.position = 'relative';
    src.style.top = 'auto';
    src.style.left = 'auto';
    src.style.width = '100%';

    if (src && ref != src) {

        var src_id = src.id.replace('dashlet_', '');
        var ref_id = ref ? ref.id.replace('dashlet_', '') : null;

        var args = {src: src_id, dst: dst.id, ref: ref_id};
        args['view_id'] = openobject.dom.get('_terp_view_id').value;

        var req = openobject.http.postJSON('/openerp/viewed/update_dashboard', args);
        req.addCallback(function(obj) {

            if (obj.error) {
                return error_display(obj.error);
            }

            if (obj.reload) {
                window.location.reload();
            }
        });
    }
}

jQuery(document).ready(initialize_dashboard);
