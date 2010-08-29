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
