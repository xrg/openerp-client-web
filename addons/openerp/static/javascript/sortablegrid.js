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
// -   All names, links and logos of Tiny, Open ERP and Axelor must be 
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

// Based on MochiKit `sortable_table` demo

mouseOverFunc = function () {
    try{
        addElementClass(this, "over");
    } catch(e){}
};

mouseOutFunc = function () {
    try{
        removeElementClass(this, "over");
    } catch(e){}
};

ignoreEvent = function (ev) {
    if (ev && ev.preventDefault) {
        ev.preventDefault();
        ev.stopPropagation();
    } else if (typeof(event) != 'undefined') {
        event.cancelBubble = false;
        event.returnValue = false;
    }
};

SortableGrid = function (table, options) {
    this.__init__(table, options);
};

SortableGrid.prototype = {

    __init__ : function(table, options) {

        this.thead = null;
        this.tbody = null;
        this.columns = [];
        this.rows = [];
        this.sortState = {};
        this.sortkey = 0;

        table = openobject.dom.get(table);

        // Find the thead
        this.thead = table.getElementsByTagName('thead')[0];

        // get the kind key and contents for each column header
        var cols = this.thead.getElementsByTagName('th');
        for (var i = 0; i < cols.length; i++) {
            var node = cols[i];
            var attr = null;
            try {
                attr = node.getAttribute("kind");
            } catch (err) {
                // pass
            }

            if (attr) {
                addElementClass(node, 'sortable');
            }

            var o = node.childNodes;
            this.columns.push({
                "format": attr,
                "element": node,
                "proto": attr ? node.cloneNode(true) : node
            });
        }

        // scrape the tbody for data
        this.tbody = table.getElementsByTagName('tbody')[0];
        // every row
        var rows = openobject.dom.select('tr.grid-row', this.tbody);
        for (var i = 0; i < rows.length; i++) {

            // every cell
            var row = rows[i];
            var cols = openobject.dom.select('td.grid-cell', row);
            var rowData = [];
            for (var j = 0; j < cols.length; j++) {
                // scrape the text and build the appropriate object out of it
                var cell = cols[j];
                var obj = strip(scrapeText(cell));
                switch (this.columns[j].format) {
                    case 'date':
                    case 'datetime':
                        obj = MochiKit.DOM.getNodeAttribute(cell, 'sortable_value');
                        obj = isoTimestamp(obj) || obj;
                        break;
                    case 'float':
                        obj = MochiKit.DOM.getNodeAttribute(cell, 'sortable_value');
                        obj = parseFloat(obj) || 0;
                        break;
                    case 'integer':
                        obj = parseInt(obj) || 0;
                        break;
                    case 'many2many':
                    case 'one2many':
                        obj = obj.replace(/\((\d+)\)/g, '$1');
                        obj = parseInt(obj) || 0;
                        break;
                    default:
                        // default is case insensitive string comparison
                        obj = obj.toLowerCase();
                        break;
                }
                rowData.push(obj);
            }
            // stow away a reference to the TR and save it
            rowData.row = row.cloneNode(true);
            this.rows.push(rowData);

        }

        // do initial sort on first column
        //this.drawSortedRows(this.sortkey, true, false);
        this.drawColumnHeaders(-1, true, false);
    },

    onSortClick : function (name) {
        return method(this, function () {
            var order = this.sortState[name];
            if (order == null) {
                order = true;
            } else if (name == this.sortkey) {
                order = !order;
            }
            this.drawSortedRows(name, order, true);
            this.drawColumnHeaders(name, order, true);
        });
    },

    drawColumnHeaders : function (key, forward, clicked) {

        for (var i = 0; i < this.columns.length; i++) {
            var col = this.columns[i];
            var node = col.proto.cloneNode(true);

            if (col.format) {
                // remove the existing events to minimize IE leaks
                col.element.onclick = null;
                col.element.onmousedown = null;
                col.element.onmouseover = null;
                col.element.onmouseout = null;

                // set new events for the new node
                node.onclick = this.onSortClick(i);
                node.onmousedown = ignoreEvent;
                node.onmouseover = mouseOverFunc;
                node.onmouseout = mouseOutFunc;
            }

            // if this is the sorted column
            if (key == i && col.format) {

                var span = SPAN({'class': forward ? "sortup" : "sortdown"}, null);
                span.innerHTML = '&nbsp;&nbsp;&nbsp;';

                // add the character to the column header
                node.appendChild(span);

                if (clicked) {
                    node.onmouseover();
                }
            }

            // swap in the new th
            col.element = swapDOM(col.element, node);
        }
    },

    drawSortedRows : function (key, forward, clicked) {
        this.sortkey = key;
        // sort based on the state given (forward or reverse)
        var cmp = (forward ? keyComparator : reverseKeyComparator);
        this.rows.sort(cmp(key));
        // save it so we can flip next time
        this.sortState[key] = forward;
        // get every "row" element from this.rows and make a new tbody
        var newBody = TBODY(null, map(itemgetter("row"), this.rows));
        // swap in the new tbody
        this.tbody = swapDOM(this.tbody, newBody);
    }
};
