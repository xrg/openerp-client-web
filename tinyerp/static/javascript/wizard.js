////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
//
// $Id$
//
// Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
//
// WARNING: This program as such is intended to be used by professional
// programmers who take the whole responsibility of assessing all potential
// consequences resulting from its eventual inadequacies and bugs
// End users who are looking for a ready-to-use solution with commercial
// guarantees and support are strongly advised to contract a Free Software
// Service Company
//
// This program is Free Software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the 
// Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
// Boston, MA  02111-1307, USA.
//
////////////////////////////////////////////////////////////////////////////////

var WAITBOX = null;
var WAITBOX_SHOW = false;

MochiKit.DOM.addLoadEvent(function(evt){
    WAITBOX = new WaitBox();
});

function showWaitBox() {

    if (WAITBOX_SHOW) {
        WAITBOX.show();
    }
}

function wizardAction(state) {

    var form = MochiKit.DOM.getElement('view_form');
    var act = '/wizard/action';

    if (state == 'end'){
        act = '/wizard/end';
    }

    if (state == 'report'){
        act = '/wizard/report';
    }
    
    if (state != 'end' && !validate_required(form)) {
        return false;
    }

    MochiKit.DOM.setNodeAttribute(form, 'action', act);
    form._terp_state.value = state;

    WAITBOX_SHOW = state != 'report';
    
    MochiKit.Async.callLater(2, showWaitBox);
    
    form.submit();
}
