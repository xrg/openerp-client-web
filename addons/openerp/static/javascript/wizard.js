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

var WAIT_BOX = null;

jQuery(document).ready(function(){
    WAIT_BOX = new openerp.ui.WaitBox();
});

function wizardAction(state) {

    var form = document.forms['view_form'];
    var act = '/openerp/wizard/action';

    if (state == 'end'){
        act = '/openerp/wizard/end';
    }

    if (state == 'report'){
        act = '/openerp/wizard/report';
    }
    
    if (state != 'end' && !validate_required(form)) {
        return;
    }

    MochiKit.DOM.setNodeAttribute(form, 'action', openobject.http.getURL(act));
    form._terp_state.value = state;

    jQuery(form).submit();
}
