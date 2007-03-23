///////////////////////////////////////////////////////////////////////////////
//
// Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
//
// $Id: list.py 5 2007-03-23 06:13:51Z ame $
//
// WARNING: This program as such is intended to be used by professional
// programmers who take the whole responsability of assessing all potential
// consequences resulting from its eventual inadequacies and bugs
// End users who are looking for a ready-to-use solution with commercial
// garantees and support are strongly adviced to contract a Free Software
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
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
//
///////////////////////////////////////////////////////////////////////////////

var AjaxList = function (id, checkable, editable) {

    makeHeader = function(headers){

        tr = TR(null);

        if (checkable) appendChildNodes(tr, TH({class: 'listButton'}, INPUT({type: 'checkbox'})));

        forEach(headers, function(header){
            td = TH(null, header[1]);
            appendChildNodes(tr, td);
        });

        if (editable) appendChildNodes(tr, TH({class: 'listButton'}));
        if (editable) appendChildNodes(tr, TH({class: 'listButton'}));

        return THEAD(null, tr);
    }

    makeBody = function(headers, data) {

        tbody = TBODY(null);

        i = 0;

        forEach(data, function(row){
            tr = TR({class: i%2 == 0 ? 'even' : 'odd'});

            if (checkable) appendChildNodes(tr, TD({class: 'listButton'}, INPUT({type: 'checkbox', value: row['id']})));

            forEach(headers, function(header){
                td = TD(null, row[header[0]]);
                appendChildNodes(tr, td);
            });

            if (editable) appendChildNodes(tr, TD({width: '25px', class: 'listButton'}, IMG({class: 'listImage', src: '/static/images/edit_inline.gif'})));
            if (editable) appendChildNodes(tr, TD({width: '25px', class: 'listButton'}, IMG({class: 'listImage', src: '/static/images/delete_inline.gif'})));

            appendChildNodes(tbody, tr);

            i++;
        });

        return tbody;
    }

    this.render = function (url, params) {

        res = doSimpleXMLHttpRequest(url, params);

        res.addCallback(function(xmlHttp) {

	        obj = evalJSONRequest(xmlHttp);

		    headers = obj['headers'];
    		data = obj['data'];

	    	table = TABLE({class: 'grid', cellpadding: 0, cellspacing: 1, border: 0}, makeHeader(headers), makeBody(headers, data));

		    swapDOM(id, table);
    	});

	    wait(res, 10);
    }
}
