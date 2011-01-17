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

// requires: mootools & draw2d

if (typeof(openobject) == "undefined") {
    openobject = new Object;
}

if (typeof(openobject.workflow) == "undefined") {
    openobject.workflow = new Object;
}

var WORKFLOW;
function show_grid(el) {
    WORKFLOW.setBackgroundImage(
            el.checked ? '/view_diagram/static/images/grid_10.jpg' : null,
            el.checked);
    WORKFLOW.setGridWidth(10, 10);
    WORKFLOW.setSnapToGrid(el.checked);
}

function create_node() {
    var html = WORKFLOW.state.getHTMLElement();
    html.style.display = '';
    WORKFLOW.state.edit();
    html.style.display = 'none';
}

openobject.workflow.Workflow = new Class;
openobject.workflow.Workflow.prototype = $merge(openobject.workflow.Workflow.prototype, draw2d.Workflow.prototype);

openobject.workflow.Workflow.implement({

    initialize : function(canvas) {
        draw2d.Workflow.call(this, canvas);
        this.getCommandStack().setUndoLimit(0);

        // enable grid by default
        this.setBackgroundImage('/view_diagram/static/images/grid_10.jpg', true);
        this.setGridWidth(10, 10);
        this.setSnapToGrid(true);

        this.id = null;
        this.node_obj = openobject.dom.get('node').value;
        this.connector_obj = openobject.dom.get('connector').value;
        this.src_node_nm = openobject.dom.get('src_node').value;
        this.des_node_nm = openobject.dom.get('des_node').value;
        this.in_transition_field = this.out_transition_field = '';

        this.states = {};
        this.connectors = {};
        this.selected = null;

//		dummy state
        this.state = new openobject.workflow.StateOval({}, []);
        this.state.setDimension(100, 60);
        this.state.setBackgroundColor(new draw2d.Color(255, 255, 255));
        this.state.getHTMLElement().style.display = 'none';
        this.addFigure(this.state, 20, 20);
        this.state.initPort();
        this.state.initPort();

        this.node_flds_v = getElement('node_flds_visible').value;
        this.node_flds_h = getElement('node_flds_invisible').value;
        this.conn_flds = getElement('conn_flds').value;
        this.bgcolors = getElement('bgcolors').value;
        this.shapes = getElement('shapes').value;

        if (openobject.dom.get('wkf_id'))
            this.draw_graph(openobject.dom.get('wkf_id').value);
        else {
            openobject.dom.get('loading').style.display = 'none';
        }
    },

    draw_graph : function(wkf_id) {

        this.id = wkf_id;
        var self = this;

        openobject.http.postJSON('/view_diagram/workflow/get_info',{
            id:wkf_id, model:getElement('_terp_model').value,
            node_obj: self.node_obj, conn_obj:self.connector_obj,
            src_node: self.src_node_nm, des_node:self.des_node_nm,
            node_flds_v: this.node_flds_v, node_flds_h: this.node_flds_h, node_flds_string: jQuery('#node_flds_string').val(),
            conn_flds: this.conn_flds, conn_flds_string: jQuery('#conn_flds_string').val(),
            bgcolors: this.bgcolors, shapes: this.shapes
        }).addCallback(function(obj) {
            self.in_transition_field = obj['in_transition_field'];
            self.out_transition_field = obj['out_transition_field'];

            for(var i in obj.nodes) {
                var node = obj.nodes[i];

                var state;
                if(node['shape']=='ellipse')
                    state = new openobject.workflow.StateOval(node);
                else if(node['shape']=='rectangle')
                    state = new openobject.workflow.StateRectangle(node);

                self.addFigure(state, node['x'], node['y']);
                state.initPort();
                self.states[node['id']] = state;
            }

            //check for overlapping connections
            for(i in obj.conn) {
                var counter = 1;
                var check_for = obj.conn[i];
                check_for['isOverlaping'] = false;

                for(var k in obj.conn) {
                    if(i!=k) {
                        var check_to = obj.conn[k];

                        if(check_for['s_id']==check_to['s_id'] && check_for['d_id']==check_to['d_id']) {
                            check_for['isOverlaping'] = true;
                            counter++;
                        }
                        else if(check_for['d_id']==check_to['s_id'] && check_for['s_id']==check_to['d_id']) {
                            check_for['isOverlaping'] = true;
                            counter++;
                        }
                    }
                    else {
                        check_for['OverlapingSeq'] = counter;
                    }
                }
                check_for['totalOverlaped'] = counter;
            }

            for(i in obj.conn) {
                var conn = obj.conn[i];
                self.add_connection(conn['s_id'], conn['d_id'], conn);
            }

            openobject.dom.get('loading').style.display = 'none';
        });
    },

    get_overlaping_connection : function(s, e, flag) {

        var conn_overlapped = new Array();
        var counter = 1;

        var conn;
        for (var connector_id in this.connectors) {
            conn = this.connectors[connector_id];
            var start = conn.getSource().getParent().get_act_id();
            var end = conn.getTarget().getParent().get_act_id();

            if((start==s && end==e)) {
                conn.isOverlaping = true;
                conn.OverlapingSeq = counter ++;
                conn_overlapped.push(connector_id);
            }else if(end==s && start==e) {
                conn.isOverlaping = true;
                conn.OverlapingSeq = counter ++;
                conn_overlapped.push(connector_id);
            }
        }

        for(var i=0; i<conn_overlapped.length; i++) {
            conn = this.connectors[conn_overlapped[i]];

            if(flag) {
                conn.totalOverlaped = counter;
            } else {
                conn.totalOverlaped = counter - 1;
                if(counter-1==1)
                    conn.isOverlaping = false;
            }
        }

        return counter;
    },

    add_connection : function(start, end, params) {

        var source = this.states[start];
        var destination = this.states[end];

        var conn = new openobject.workflow.Connector(params.id, params.source, params.destination, params.options);

        //self connection
        if(start==end) {
            conn.setSourceAnchor(new draw2d.ConnectionAnchor);
            conn.setTargetAnchor(new draw2d.ConnectionAnchor);
            conn.setRouter(new draw2d.BezierConnectionRouter());
        }

        conn.isOverlaping = params.isOverlaping;
        conn.OverlapingSeq = params.OverlapingSeq;
        conn.totalOverlaped = params.totalOverlaped;

        var spos = source.getBounds();
        var dpos = destination.getBounds();

        //fix source and destination ports
        if(spos.x<dpos.x) {
            conn.setTarget(destination.portL);

            if((spos.y + spos.h - dpos.y)>50)
                conn.setSource(source.portD);
            else if((dpos.y + dpos.h - spos.y)>50)
                conn.setSource(source.portU);
            else
                conn.setSource(source.portR);
        }
        else {
            conn.setTarget(destination.portR);

            if((spos.y + spos.h - dpos.y)>50)
                conn.setSource(source.portD);
            else if((dpos.y + dpos.h - spos.y)>50)
                conn.setSource(source.portU);
            else
                conn.setSource(source.portL);
        }

        source.out_transition.push(params.id)
        destination.in_transition.push(params.id)

        this.addFigure(conn);
        this.connectors[params.id] = conn;
    },

    create_state : function(id) {

        if(id != 0) {
            var position = this.state.getPosition();
            this.state.setPosition(100, 20);
            var self = this;

            openobject.http.postJSON('/view_diagram/workflow/state/get_info',{
                node_obj: self.node_obj,
                id: id,
                in_transition_field: this.in_transition_field,
                out_transition_field: this.out_transition_field,
                node_flds_v: this.node_flds_v,
                node_flds_h: this.node_flds_h,
                node_flds_string: jQuery('#node_flds_string').val(),
                bgcolors: this.bgcolors,
                shapes: this.shapes
            }).addCallback(function(obj) {
                var flag = false;
                var data = obj.data;
                if (self.states[id])
                    flag = true;


                var state;
                if(!flag) {
                    if(!data['subflow_id'])
                         state = new openobject.workflow.StateOval(data);
                    else
                         state = new openobject.workflow.StateRectangle(data);

                    self.addFigure(state, position.x, position.y);
                    self.states[id] = state;
                    state.initPort();
                }else {
                    state = self.states[id];
                    var span = openobject.dom.get(state.name);
                    span.innerHTML = data['name'];
                    span.id = data['name'];

                    MochiKit.Base.update(state.options, data['options'])
                }

                var in_tr = data[self.in_transition_field];
                for(var i=0; i<in_tr.length; i++) {//create new transition
                    if (state.in_transition.indexOf(in_tr[i])==-1)
                        self.create_connection(false, false, in_tr[i]);
                }

                for(i=0; i<state.in_transition.length; i++) {//delete non-existent transition
                    var tr = state.in_transition[i];
                    if (in_tr.indexOf(tr)==-1)
                        self.remove_conn(self.connectors[tr]);
                }

                var out_tr = data[self.out_transition_field];
                for(i=0; i<out_tr.length; i++) {//create new transition
                    if (state.out_transition.indexOf(out_tr[i])==-1)
                        self.create_connection(false, false, out_tr[i]);
                }

                for(i=0; i<state.out_transition.length; i++) {//delete non-existent transition
                    var tr = state.out_transition[i];
                    if (out_tr.indexOf(tr)==-1)
                        self.remove_conn(self.connectors[tr]);
                }


            });
        } else {
            error_display(_('state could not be created'));
        }
    },


    create_connection : function(act_from, act_to, id) {

        var self = this;
        openobject.http.postJSON('/view_diagram/workflow/connector/auto_create', {
            conn_obj: self.connector_obj,
            src: self.src_node_nm,
            des: self.des_node_nm,
            act_from: act_from,
            act_to: act_to,
            id: id,
            conn_flds: this.conn_flds,
            conn_flds_string: jQuery('#conn_flds_string').val()
        }).addCallback(function(obj) {
            var data = obj.data;

            if(obj.flag) {
                if (!act_from)
                    act_from = data['s_id'];
                if (!act_to)
                    act_to = data['d_id'];

                var counter = self.get_overlaping_connection(data['s_id'], data['d_id'], 1);
                var params = MochiKit.Base.update({}, obj.data);

                if(counter>1) {
                    params['isOverlaping'] = true;
                    params['OverlapingSeq'] = counter;
                    params['totalOverlaped'] = counter;
                }

                self.add_connection(act_from, act_to, params);
            } else {
                error_display(_('Could not create transaction at server'));
            }
        });
    },

    update_connection : function(id) {

        var self = this;
        openobject.http.postJSON('/view_diagram/workflow/connector/get_info',{
            conn_obj: self.connector_obj,
            id: id
        }).addCallback(function(obj) {
            var conn = self.connectors[id];
            conn.signal = obj.data['signal'];
            conn.condition = obj.data['condition'];
        });
    },

    remove_elem : function(elem) {
        if(elem instanceof openobject.workflow.StateOval || elem instanceof openobject.workflow.StateRectangle)
            this.unlink_state(elem);
        else if(elem instanceof openobject.workflow.Connector)
            this.unlink_connector(elem);
    },

    unlink_state : function(state) {

        var self = this;
        openobject.http.postJSON('/view_diagram/workflow/state/delete', {
            node_obj: self.node_obj,
            'id': state.get_act_id()
        }).addCallback(function(obj) {
            if(!obj.error) {
                state.__delete__();
                self.remove_state(state);
            } else {
                error_display(obj.error);
            }
        });
    },

    remove_state : function(state) {

        var fig = this.getFigure(state.getId());
        var connections = null;

        if(fig.getPorts && connections==null) {
            connections = new draw2d.ArrayList();
            var ports = fig.getPorts();
            for(var i=0; i<ports.getSize(); i++) {
                if(ports.get(i).getConnections) {
                    connections.addAll(ports.get(i).getConnections());
            }
          }
        }

        if(connections == null)
            connections = new draw2d.ArrayList();

        for (var i = 0; i < connections.getSize(); ++i) {
            this.removeFigure(connections.get(i));
        }

        this.removeFigure(fig);
        this.setCurrentSelection(null);
        if(fig.parent!=null)
            fig.parent.removeChild(fig);
        delete this.states[state.get_act_id()];
    },

    unlink_connector : function(conn) {

        var self = this;
        openobject.http.postJSON('/view_diagram/workflow/connector/delete', {
            conn_obj: self.connector_obj,
            'id': conn.get_tr_id()
        }).addCallback(function(obj) {
            if(!obj.error) {
                conn.__delete__();
                self.remove_conn(conn);
            } else
                error_display(obj.error);
        });
    },

    remove_conn : function(conn) {
        var id = conn.get_tr_id();
        var start = conn.getSource().getParent().get_act_id();
        var end = conn.getTarget().getParent().get_act_id();

        this.states[end].in_transition.splice(this.states[end].in_transition.indexOf(id), 1);
        this.states[start].out_transition.splice(this.states[start].out_transition.indexOf(id), 1);
        delete this.connectors[id];
        if(conn.isOverlaping)
            this.get_overlaping_connection(start, end, 0);

        this.removeFigure(conn);
    },

    onMouseDown : function(x, y) {

        if (this.currentSelection instanceof draw2d.Connection)
            this.selected = this.currentSelection;
        else
            this.selected = null;

        draw2d.Workflow.prototype.onMouseDown.call(this, x, y);
    }
});
