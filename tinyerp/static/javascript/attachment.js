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

function do_select(id, src){
    var radio = $(src + '/' + id);
    radio.checked = true;

    do_save(document.forms[0]);
}

function save_file(form) {
	form.submit(form);
}

function do_select(id, src){
    var radio = $(src + '/' + id);
    radio.checked = true;

    do_save(document.forms[0]);
}

function do_edit(form, action) {
	var list = new ListView('_terp_list');
    var boxes = list.getSelectedItems();
	
	if (boxes.length == 0) {
		alert('Please select a resouce...');
		return;
	}
	
	if (boxes.length > 0){
    	var id = boxes[0].value;
    	
    	var p = boxes[0].parentNode.parentNode;
    	var a = getElementsByTagAndClassName('a', null, p)[0];

    	var fname = '/' + a.innerHTML;
    	
    	setNodeAttribute(form, 'action', getURL('/attachment/edit' + fname, {record: id}));
    }
	
    form.submit();
}

function do_add(form) {
	setNodeAttribute(form, 'action', '/attachment/edit');
	form.submit();
}

function do_delete(form) {
    var list = new ListView('_terp_list');
    var boxes = list.getSelectedItems();

    if (boxes.length == 0){
        alert('Please select a resouce...');
        return;
    }

    var id = boxes[0].value;
    setNodeAttribute(form, 'action', getURL('/attachment/delete', {record: id}));
    form.submit();
}

function do_save(form){

    var list = new ListView('_terp_list');
    var boxes = list.getSelectedItems();

    if (boxes.length == 0){
        alert('Please select a resouce...');
        return;
    }

    var id = boxes[0].value;

    var p = boxes[0].parentNode.parentNode;
    var a = getElementsByTagAndClassName('a', null, p)[0];

    var fname = '/' + a.innerHTML;

    setNodeAttribute(form, 'action', getURL('/attachment/save_as' + fname, {record: id}));
    form.submit();
}