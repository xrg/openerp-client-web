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

var TreeGrid = function(id, headers) {

    this.id = id;

    this.headers = eval(headers);
    this.tfield = this.headers[0][0];

    this.url = null;
    this.params = {};

    this.isloading = false;

    this.selectable = false;
    this.show_headers = true;

    this.onopen = function(id, args){};

    this.row_info = {0: {children: null, indent: 0}};
}

TreeGrid.prototype._onopen = function(id) {

    var func = function() {
        this.onopen(id, this.params);
    }

    return bind(func, this);
}

TreeGrid.prototype.toggle = function(row, forced) {

    if (this.isloading)
        return false;

    var table = $(this.id);
    var row = $(row);

    var children = this.row_info[row.id].children;

    if (!children)
        return false;

    var index = -1;
    var indent = this.row_info[row.id].indent; indent = parseInt(indent) + 1;

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

            var state = child ? (child.style.display == "none" ? 'expand' : 'collapse') : (forced ? 'expand' : 'collapse');
            this._row_state(row, state);

        } else if (!forced) {
            this._add_rows(index, children, indent);
            break;
        }
    }

    return true;
}

TreeGrid.prototype._make_head = function(){

    var thd = THEAD(null);
    var tr = TR(null);

    if (this.selectable){
        var cbx = INPUT({'type':'checkbox', 'onclick': this.id + '.selectAll(this.checked);' });
        appendChildNodes(tr, TH({'width':'20px'}, cbx));
    }

    for(var i in this.headers){
        var header = this.headers[i][1];
        var th = TH(null, header.string);

        setNodeAttribute(th, 'title', header.help ? header.help : '');
        setNodeAttribute(th, 'class', header.type);

        appendChildNodes(tr, th);
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
    var tr = TR({id: rid});

    // save children and indent info
    this.row_info[rid] = {children: record.children, indent: indent ? indent : 0};

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
            val = A({'href': '#'}, val);

            // connect onclick event
            connect(val, 'onclick', this._onopen(record.id));

            if (record.children && record.children.length > 0)
                appendChildNodes(td, SPAN({'class': 'expand', 'onclick': this.id + '.toggle("' + rid + '")' }));
            else
                appendChildNodes(td, SPAN({'class' : 'indent'}));
        }

        setNodeAttribute(td, 'class', header[1].type);

        appendChildNodes(td, val);
        appendChildNodes(tr, td);
    }

    return tr;
}

TreeGrid.prototype._row_state = function(row, state){
    var span = row.getElementsByTagName('span'); span = span[span.length-1];
    setNodeAttribute(span, 'class', state);
}

TreeGrid.prototype._add_rows = function(after, children, indent){

    var args = {ids: children}; update(args, this.params);
    var index = parseInt(after);

    this.isloading = true;

    var row = $(this.id).rows[index];
    this._row_state(row, 'loading');

    var req = doSimpleXMLHttpRequest(this.url, args);
    var grid = this;

    req.addCallback(function(xmlHttp){
        var res = evalJSONRequest(xmlHttp);

        var g = $(grid.id);

        for (var i in res.records){
            var tr = grid._make_row(res.records[i], indent);

            index = parseInt(index) + 1;
            var r = g.insertRow(index);

            swapDOM(r, tr);
        }

    });

    req.addBoth(function(xmlHttp){
        grid.isloading = false;
        grid._row_state(row, 'collapse');
    });
}

TreeGrid.prototype.load = function(url, id, params){

    this.url = url;
    this.params = params ? params : {};

    var args = {ids: id}; update(args, this.params);

    this.isloading = true;

    $(this.id).innerHTML = "Loading...";

    var req = doSimpleXMLHttpRequest(url, args);
    var grid = this;

    req.addCallback(function(xmlHttp){
        var res = evalJSONRequest(xmlHttp);

        var table = TABLE({id: grid.id, 'class': 'tree-grid'});

        var thd = grid._make_head();
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
