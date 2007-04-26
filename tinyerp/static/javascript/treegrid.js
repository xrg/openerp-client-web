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

var TreeGrid = function(id) {

    this.tfield = null;
    this.id = id;

    this.url = null;
    this.params = {};

    this.isloading = false;

    this.selectable = false;
    this.show_headers = true;
}

TreeGrid.prototype.toggle = function(row, forced) {

    if (this.isloading)
        return false;

    var table = $(this.id);
    var row = $(row);

    var children = getNodeAttribute(row, 'children');
    children = children ? children.split(',') : null;

    if (!children)
        return false;

    var index = -1;
    var indent = getNodeAttribute(row, 'indent'); indent = parseInt(indent) + 1;

    for (var i in table.rows) {
        if (table.rows[i] == row) {
            index = i;
            break;
        }
    }

    for(var i in children) {

        var cid = children[i];
        var child = $(this.id + "_row_" + cid);

        if (child) {
            child.style.display = forced ? forced : (child.style.display == "none" ? "table-row" : "none");
            // force children of child row to be hidden
            this.toggle(child, "none");
        } else if (!forced) {
            index = parseInt(index);
            this._add_row(index+1, cid, indent);
        }
    }

    var plus = row.getElementsByTagName('span'); plus = plus[plus.length-1];
    var css = child ? (child.style.display == "none" ? 'plus' : 'minus') : (forced ? 'plus' : 'minus');

    setNodeAttribute(plus, 'class', css);

    return true;
}

TreeGrid.prototype._make_head = function(headers){

    this.headers = headers;

    var thd = THEAD(null);
    var tr = TR(null);

    if (this.selectable){
        var cbx = INPUT({'type':'checkbox', 'onclick': this.id + '.selectAll(this.checked);' });
        appendChildNodes(tr, TH({'width':'20px'}, cbx));
    }

    for(var i in headers){
        var header = headers[i];

        if (!this.tfield)
            this.tfield = header[0];

        appendChildNodes(tr, TH(null, header[1].title));
    }

    appendChildNodes(thd, tr);

    return this.show_headers ? thd : null;
}

TreeGrid.prototype._make_body = function(records){

    var tbd = TBODY(null);

    for(var i in records) {
        appendChildNodes(tbd, this._make_row(records[i]));
    }

    return tbd;
}

TreeGrid.prototype._make_row = function(record, indent){

    var rid = this.id + "_row_" + record.id;

    var tr = TR({id: rid, children: record.children, indent: indent ? indent : 0});

    if (this.selectable){
        var cbx = INPUT({'type':'checkbox', 'name':this.id, 'value':record.id});
        appendChildNodes(tr, TD(null, cbx));
    }

    for(var i in this.headers) {

        var header = this.headers[i];

        var td = TD(null);
        var key = header[0];

        if (indent && key === this.tfield){
            for(var i=0; i<indent; i++){
                appendChildNodes(td, SPAN({'class' : 'indent'}));
            }
        }

        var val = record.data[key];

        if (key === this.tfield){
            val = A({href: 'javascript: void(0)'}, val);

            if (record.children && record.children.length > 0)
                appendChildNodes(td, SPAN({'class': 'plus', onclick: this.id + '.toggle("' + rid + '")' }));
            else
                appendChildNodes(td, SPAN({'class' : 'indent'}));
        }

        appendChildNodes(td, val);
        appendChildNodes(tr, td);
    }

    return tr;
}

TreeGrid.prototype._add_row = function(after, cid, indent){

    var args = {id: cid}; update(args, this.params);

    this.isloading = true;

    var req = doSimpleXMLHttpRequest(this.url, args);
    var grid = this;

    req.addCallback(function(xmlHttp){
        var res = evalJSONRequest(xmlHttp);

        var tr = grid._make_row(res.records[0], indent);

        var g = $(grid.id);
        var r = g.insertRow(after);

        swapDOM(r, tr);
    });

    req.addBoth(function(xmlHttp){
        grid.isloading = false;
    });
}

TreeGrid.prototype.load = function(url, id, params){

    this.url = url;
    this.params = params ? params : {};

    var args = {id: id}; update(args, this.params);

    this.isloading = true;

    var req = doSimpleXMLHttpRequest(url, args);
    var grid = this;

    req.addCallback(function(xmlHttp){
        var res = evalJSONRequest(xmlHttp);

        var table = TABLE({id: grid.id, 'class': 'tree-grid'});

        var thd = grid._make_head(res.headers);
        var tbd = grid._make_body(res.records);

        appendChildNodes(table, thd, tbd);

        swapDOM(grid.id, table);
    });

    req.addBoth(function(xmlHttp){
        grid.isloading = false;
    });

}

TreeGrid.prototype.selectAll = function(clear) {
    clear = clear == null ? true: clear;

    boxes = $(this.id).getElementsByTagName('input');
    forEach(boxes, function(box){
        box.checked = clear;
    });

}

TreeGrid.prototype.getSelected = function() {
    var res = [];

    boxes = $(this.id).getElementsByTagName('input');
    forEach(boxes, function(box){
        if (box.checked && box.name) res.push(parseInt(box.value));
    });

    return res;
}
