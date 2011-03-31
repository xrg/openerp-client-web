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

if (typeof(openobject) == "undefined") {
    openobject = {};
}

if (typeof(openobject.process) == 'undefined') {
    openobject.process = {};
}

openobject.process.NAME = "openobject.process";
openobject.process.__repr__ = openobject.process.toString = function () {
    return "[" + this.NAME + "]";
};

/**
 * openobject.process.Workflow
 */
openobject.process.Workflow = function(canvas) {
    this.__init__(canvas);
};

openobject.process.Workflow.prototype = new draw2d.Workflow();
MochiKit.Base.update(openobject.process.Workflow.prototype, {

    __super__: draw2d.Workflow,

    __init__: function(canvas) {

        this.__super__.call(this, canvas);
        this.setBackgroundImage(null, false);

        this.nodes = {};
        this.transitions = {};
    },

    load: function(id, res_model, res_id, title) {

        this.process_id = id;
        this.res_model = res_model;
        this.res_id = res_id;
        this.title = title;

        var self = this;
        var req = openobject.http.postJSON('/view_diagram/process/get', {id: id, res_model: res_model, res_id: res_id, title: title});
        req.addCallback(function(obj){
            self._render(title, obj.perm, obj.notes, obj.nodes, obj.transitions, obj.related);
        });

    },

    reload: function() {
        this.load(this.process_id, this.res_model, this.res_id, this.title);
    },

    _render: function(title, perm, notes, nodes, transitions, related) {

        var h = 0;
        var w = 0;

        var subflows = {};
        var related = related || {};

    	for(var id in nodes){
    		var data = nodes[id];

            data['res_model'] = this.res_model;
            data['res_id'] = this.res_id;

    		var n = new openobject.process.Node(data);
	    	this.addFigure(n, data.x, data.y);

	    	this.nodes[id] = n; // keep reference

            h = Math.max(h, data.y);
            w = Math.max(w, data.x);

            if (data.subflow && data.subflow.length) {
                subflows[data.subflow[0]] = data.subflow[1];
            }

	    }

        h += 100 + 10; // add height of node + some margin
        w += 150 + 10; // add width of node + some margin

        MochiKit.DOM.setElementDimensions(this.html, {h: h, w: w});

	    for(var id in transitions){
    		var data = transitions[id];

    		var src = this.nodes[data.source];
    		var dst = this.nodes[data.target];

            // make active
            data.active = src.data.active && !dst.data.gray;

            var t = new openobject.process.Transition(data);

    		t.setSource(src.outPort);
    		t.setTarget(dst.inPort);

    		this.addFigure(t);

    		this.transitions[id] = t; // keep reference
    	}

        // create notes
        var note = this._create_note(notes, subflows, perm, related);
        var canvas = openobject.dom.get('process_canvas');
        canvas.parentNode.insertBefore(note, canvas);

        // check whether any node overlaps the notes
        var npos = getElementPosition(note, note.parentNode);
        var ndim = getElementDimensions(note);

        // set title
        openobject.dom.get('process_title').innerHTML = title;

        var elems = openobject.dom.select('*', this.html);
        elems = MochiKit.Base.filter(function(e){
            return MochiKit.DOM.getNodeAttribute(e, 'title');
        }, elems);

        if (elems.length) {
            new openerp.ui.Tips(elems);
        }
    },

    _create_note:  function(notes, subflows, perm, related) {

        var self = this;
        var elem = MochiKit.DOM.DIV({'class': 'process-notes'});
        var perm = perm || {};

        var sflows = "";
        var rflows = "";

        for(var k in subflows) {
            if (k != this.process_id)
                sflows += "<a href='" + openobject.http.getURL('/view_diagram/process', {id: k, res_model: self.res_model, res_id: self.res_id}) + "'>" + subflows[k] + "</a><br/>";
        }

        for(var k in related) {
            if (k != this.process_id)
                rflows += "<a href='" + openobject.http.getURL('/view_diagram/process', {id: k, res_model: self.res_model, res_id: self.res_id}) + "'>" + related[k] + "</a><br/>";
        }

        var text = (
                    "<dl>"+
                    "<dt>"+ _("Notes:") + "</dt>" +
                    "<dd>" +
                        notes +
                    "</dd>"+
                    "<dt>"+ perm.text + "</dt>"+
                    "<dd>"+ perm.value + "</dd>");

        if (sflows.length) {
            text += "<dt>" + _("Subflows:") + "</dt><dd>" + sflows + "</dd>";
        }

        if (rflows.length) {
            text += "<dt>" + _("Related:") + "</dt><dd>" + rflows + "</dd>";
        }

        text += "</dl>";

        elem.innerHTML = text;

        return elem;
    }

});

/**
 * openobject.process.Node
 */
openobject.process.Node = function(data) {
    this.__init__(data);
};

openobject.process.Node.prototype = new draw2d.Node();
MochiKit.Base.update(openobject.process.Node.prototype, {

    __super__: draw2d.Node,

    __init__: function(data) {
        this.data = data;

        this.__super__.call(this);

        this.setDimension(150, 100);
        this.setResizeable(false);
        this.setSelectable(false);
        this.setCanDrag(false);
        this.setColor(null);
    },

    createHTMLElement: function() {
        var elem = this.__super__.prototype.createHTMLElement.call(this);

        var bg = "node";
        bg = this.data.kind == "subflow" ? "node-subflow" : "node";
        bg = this.data.gray ? bg + "-gray" : bg;
        elem.style.background = 'url(/view_diagram/static/images/'+ bg + '.png) no-repeat';

        elem.innerHTML = (
        "<div class='node-title'></div>"+
        "<div class='node-text'></div>"+
        "<div class='node-bottom'>"+
        "   <table>"+
        "	    <tr>"+
        "		    <td class='node-buttons' nowrap='nowrap'></td>"+
        "		    <td class='node-menu' align='right'></td>"+
        "	    </tr>"+
        "   </table>"+
        "</div>");

        var title = openobject.dom.select('div.node-title', elem)[0];
        var text = openobject.dom.select('div.node-text', elem)[0];
        var bbar = openobject.dom.select('td.node-buttons', elem)[0];
        var menu = openobject.dom.select('td.node-menu', elem)[0];

        title.innerHTML = this.data.name || '';
        text.innerHTML = this.data.notes || '';

        if (this.data.subflow && this.data.subflow.length) {
            var href = openobject.http.getURL('/view_diagram/process', {id: this.data.subflow[0], res_model: this.data.res_model, res_id: this.data.res_id});
            title.innerHTML = "<a href='" + href + "'>" + this.data.name + "</a>";
        }

        if (this.data.res) {
            text.innerHTML= '<b>' + this.data.res.name + '</b><br>' + (this.data.notes || '');
            var perm = this.data.res.perm || {};
            text.title = perm.text + ": " + perm.value;
        }

        if (this.data.menu) {
            var menu_img = IMG({src: '/openerp/static/images/stock/gtk-jump-to.png'});
            menu_img.title = this.data.menu.name;
            menu_img.onclick = MochiKit.Base.bind(function(){
                openLink(openobject.http.getURL('/openerp/tree/open', {model: 'ir.ui.menu', id: this.data.menu.id}));
            }, this);
            MochiKit.DOM.appendChildNodes(menu, menu_img);
        }

        var buttons = [IMG({src: '/openerp/static/images/stock/gtk-info.png', title: _('Help')})];
        buttons[0].onclick = MochiKit.Base.bind(this.onHelp, this);

        if (this.data.active){
        	elem.style.background = 'url(/view_diagram/static/images/node-current.png) no-repeat';
        }

        MochiKit.DOM.appendChildNodes(bbar, buttons);

		elem.className = 'node';
        return elem;
    },

    setWorkflow: function(workflow) {
    	this.__super__.prototype.setWorkflow.call(this, workflow);

    	this.outPort = new draw2d.OutputPort();
        this.inPort = new draw2d.OutputPort();

        this.outPort.setWorkflow(workflow);
        this.inPort.setWorkflow(workflow);

        this.addPort(this.outPort, this.width, this.height/2);
        this.addPort(this.inPort, 0, this.height/2);

        this.inPort.getHTMLElement().style.display = 'none';
    	this.outPort.getHTMLElement().style.display = 'none';
    },

    onHelp: function() {
    	window.open(this.data.url || "http://doc.openerp.com/v6.0/index.php?model=" + this.data.model);
        //window.open(this.data.url || "http://openerp.com/scripts/context_index.php?model=" + this.data.model);
    }
});

/**
 * openobject.process.Transition
 */
openobject.process.Transition = function(data) {
    this.__init__(data);
};

openobject.process.Transition.prototype = new draw2d.Connection();
MochiKit.Base.update(openobject.process.Transition.prototype, {

    __super__: draw2d.Connection,

    __init__: function(data) {
        this.__super__.call(this);

        this.setSourceAnchor(new draw2d.ChopboxConnectionAnchor());
        this.setTargetAnchor(new draw2d.ChopboxConnectionAnchor());
        this.setRouter(new draw2d.NullConnectionRouter());
        //this.setRouter(new draw2d.ManhattanConnectionRouter());

        var color = new draw2d.Color(179, 179, 179);

        this.setTargetDecorator(new openobject.process.TargetDecorator(color));
        this.setColor(color);
        this.setLineWidth(3);
        this.setSelectable(false);

        this.data = data;

        var roles = data.roles || [];

        var elem = this.getHTMLElement();
        elem.style.cursor = 'help';

        MochiKit.Signal.connect(elem, 'onclick', this, this._makeTipText);

        if (roles.length) {
            var role_img = new draw2d.ImageFigure('/openerp/static/images/stock/stock_person.png');
            role_img.setDimension(32, 32);
            role_img.html.style.cursor = "pointer";
            this.addFigure(role_img, new draw2d.ManhattenMidpointLocator(this));
        }

    },

    _makeTipText: function() {

        var data = this.data;
        var title = data.name + '::' + (data.notes || '');

        var roles = data.roles || [];
        var buttons = data.buttons || [];

        var _mkList = function(values) {
            var r = '<ul style="margin-bottom: 0px; margin-top: 0px;">';
            MochiKit.Base.map(function(v) {
                r += '<li>' + v.name + '</li>';
            }, values);
            return r + '</ul>';
        };

        if (roles.length || buttons.length) {
            title += '<hr noshade="noshade"/>'
        }

        if (roles.length) {
            title += '<span>Roles:</span>' + _mkList(roles);
        }

        if (buttons.length) {
            title += '<span>Actions:</span>' + _mkList(buttons);
        }

        var params = {'title_tip': MochiKit.DOM.emitHTML(title)}

        openAction(openobject.http.getURL("/view_diagram/process/open_tip", params), 'new');
    }
});

/**
 * openobject.process.TargetDecorator
 */
openobject.process.TargetDecorator = function(color) {
    this.__init__(color);
};

openobject.process.TargetDecorator.prototype = new draw2d.ArrowConnectionDecorator();
MochiKit.Base.update(openobject.process.TargetDecorator.prototype, {

    __super__: draw2d.ArrowConnectionDecorator,

    __init__: function(color) {
        this.__super__.call(this);
	    this.setBackgroundColor(color);
        this.setColor(color);
    },

    paint: function(/*draw2d.Graphics*/ g) {

		if(this.backgroundColor!=null) {
     		g.setColor(this.backgroundColor);
     		g.fillPolygon([0, 6, 6, 0], [0, 6, -6, 0]);
  		}

		 // draw the border
		g.setColor(this.color);
		g.setStroke(1);
		g.drawPolygon([0, 6, 6, 0], [0, 6, -6, 0]);
	}
});

// vim: ts=4 sts=4 sw=4 si et


