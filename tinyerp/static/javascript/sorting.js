
///////////////////////////////////////////////////////////////////////////////
//
// Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
//
// $Id$
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

function do_sort(table) {
	var table = $(table);
	var rows = getElementsByTagAndClassName("tr","grid-row", table);
	do_Sortable(rows, table);
}

var SORT_COLUMN_INDEX;

function do_Sortable(rows, tableId) {

    if (tableId && rows && rows.length > 0) {

        rows_header = getElementsByTagAndClassName("tr","grid-header", tableId);

		forEach(rows_header, function(e) {
		    header_cell = e.getElementsByTagName('td');

		    forEach(header_cell, function(ee) {
		        if(ee.attributes['id']) {

		            txt = get_innerText(ee);

		            var div = DIV({'class' : 'sortheader'});
		            div.style.cursor = 'pointer';

                    var span = SPAN({'class' : 'sortarrow'});

                    appendChildNodes(div, txt, span);

                    ee.innerHTML = '';
                    appendChildNodes(ee, div);

		            connect(div, 'onclick', do_resortTable);

		        }
		    });
	    });
    }
}

function get_innerText(el) {
	if (typeof el == "string" || typeof el == "undefined") return el;
	if (el.innerText) return el.innerText;	//Not needed but it is faster

	var str = "";

	var cs = el.childNodes;

	var l = cs.length;

	for (var i = 0; i < l; i++) {

		switch (cs[i].nodeType) {
			case 1: //ELEMENT_NODE
				str += get_innerText(cs[i]);
				break;

			case 3:	//TEXT_NODE
				str += cs[i].nodeValue;
    			break;
		}
	}
	return str;
}

function do_resortTable(lnk) {

    lnk = lnk.src();

    // get the span
    var span;

    forEach(lnk.childNodes, function(e) {
        if(e.tagName && e.tagName.toLowerCase() == 'span') {
            span = e;
        }
    });

    var spantext = get_innerText(span);
    var td = lnk.parentNode;
    log("td.."+td);
    if(td.attributes){
        if(td.attributes['kind']);
            click_kind = td.attributes['kind'].value;
    }

    var column = td.cellIndex;

    var table = getParent(td,'TABLE');

    rows = getElementsByTagAndClassName("tr","grid-row", table);

    var record_ids = new Array();

    forEach(rows, function(e) {
        if(e.attributes['record']) {
            record_ids.push(e.attributes['record'].value);
        }
    });

    record_ids = '[' + record_ids.join(',') + ']';

    if($(table.id + "/" + '_terp_model')) {
        $(table.id + "/" + '_terp_ids').value = record_ids;
    }
    else {
        $('_terp_ids').value = record_ids;
    }

    // Work out a type for the column
    if (rows.length <= 1) return;
    var itm = get_innerText(rows[1].cells[column]);

    var sortfn = sort_caseinsensitive;

    if(click_kind == 'float' || click_kind == 'integer') sortfn = sort_numeric;
    if(click_kind == 'char')  sortfn = sort_caseinsensitive;
    if(click_kind == 'date' || click_kind == 'datetime' || click_kind == 'time') sortfn = sort_date;

    SORT_COLUMN_INDEX = column;

    var firstRow = new Array();
    var newRows = new Array();

    for (i=0;i<rows_header.length;i++) {
        firstRow[i] = rows_header[i];
    }

    for (j=0;j<rows.length;j++) {
        newRows[j] = rows[j];
    }

    newRows.sort(sortfn);

    if (span.getAttribute("sortdir") == 'down') {
        //ARROW = '&nbsp;&nbsp;&uarr;';
        newRows.reverse();
        span.setAttribute('sortdir','up');
    } else {
        //ARROW = '&nbsp;&nbsp;&darr;';
        span.setAttribute('sortdir','down');
    }

    // We appendChild rows that already exist to the tbody, so it moves them rather than creating new ones
    // don't do sortbottom rows

    for (i=0;i<newRows.length;i++) {
        if (!newRows[i].className || (newRows[i].className && (newRows[i].className.indexOf('sortbottom') == -1)))
            table.tBodies[0].appendChild(newRows[i]);
    }

    // do sortbottom rows only
    for (i=0;i<newRows.length;i++) {
        if (newRows[i].className && (newRows[i].className.indexOf('sortbottom') != -1))
            table.tBodies[0].appendChild(newRows[i]);
    }

    // Delete any other arrows there may be showing
    var allspans = document.getElementsByTagName("span");
    for (var ci=0;ci<allspans.length;ci++) {
        if (allspans[ci].className == 'sortarrow') {
            if (getParent(allspans[ci],"table") == getParent(lnk,"table")) { // in the same table as us?
                allspans[ci].innerHTML = '&nbsp;&nbsp;&nbsp;';
            }
        }
    }

   // span.innerHTML = ARROW;
}

function getParent(el, pTagName) {
	if (el == null) return null;
	else if (el.nodeType == 1 && el.tagName.toLowerCase() == pTagName.toLowerCase())	// Gecko bug, supposed to be uppercase
		return el;
	else
		return getParent(el.parentNode, pTagName);
}
function sort_date(a,b) {
    // y2k notes: two digit years less than 50 are treated as 20XX, greater than 50 are treated as 19XX
    aa = get_innerText(a.cells[SORT_COLUMN_INDEX]);
    bb = get_innerText(b.cells[SORT_COLUMN_INDEX]);
    if (aa.length == 10) {
        dt1 = aa.substr(6,4)+aa.substr(3,2)+aa.substr(0,2);
    } else {
        yr = aa.substr(6,2);
        if (parseInt(yr) < 50) { yr = '20'+yr; } else { yr = '19'+yr; }
        dt1 = yr+aa.substr(3,2)+aa.substr(0,2);
    }
    if (bb.length == 10) {
        dt2 = bb.substr(6,4)+bb.substr(3,2)+bb.substr(0,2);
    } else {
        yr = bb.substr(6,2);
        if (parseInt(yr) < 50) { yr = '20'+yr; } else { yr = '19'+yr; }
        dt2 = yr+bb.substr(3,2)+bb.substr(0,2);
    }
    if (dt1==dt2) return 0;
    if (dt1<dt2) return -1;
    return 1;
}

function sort_currency(a,b) {
    aa = get_innerText(a.cells[SORT_COLUMN_INDEX]).replace(/[^0-9.]/g,'');
    bb = get_innerText(b.cells[SORT_COLUMN_INDEX]).replace(/[^0-9.]/g,'');
    return parseFloat(aa) - parseFloat(bb);
}

function sort_numeric(a,b) {
    aa = parseFloat(get_innerText(a.cells[SORT_COLUMN_INDEX]));
    if (isNaN(aa)) aa = 0;
    bb = parseFloat(get_innerText(b.cells[SORT_COLUMN_INDEX]));
    if (isNaN(bb)) bb = 0;
    return aa-bb;
}

function sort_caseinsensitive(a,b) {
    aa = get_innerText(a.cells[SORT_COLUMN_INDEX]).toLowerCase();
    bb = get_innerText(b.cells[SORT_COLUMN_INDEX]).toLowerCase();
    if (aa==bb) return 0;
    if (aa<bb) return -1;
    return 1;
}

function sort_default(a,b) {
    aa = get_innerText(a.cells[SORT_COLUMN_INDEX]);
    bb = get_innerText(b.cells[SORT_COLUMN_INDEX]);
    if (aa==bb) return 0;
    if (aa<bb) return -1;
    return 1;
}


function addEvent(elm, evType, fn, useCapture)
// addEvent and removeEvent
// cross-browser event handling for IE5+,  NS6 and Mozilla
// By Scott Andrew
{
    if(lm.addEventListener){
        elm.addEventListener(evType, fn, useCapture);
        return true;
    }
    else if (elm.attachEvent) {
        var r = elm.attachEvent("on"+evType, fn);
        return r;
    }
    else {
        alert("Handler could not be removed");
    }
}
