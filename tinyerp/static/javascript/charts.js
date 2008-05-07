////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://tinyerp.com) All Rights Reserved.
//
// $Id$
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

// tango style
var ChartColors = ['#c4a000', '#ce5c00', '#8f5902', '#4e9a06', '#204a87', '#5c3566', '#a40000', '#babdb6', '#2e3436'];

var BarChart = function(elem, url, params) {
    this.__init__(elem, url, params);
}

BarChart.prototype = {
    
    __init__ : function(elem, url, params) {
        
        this.element = MochiKit.DOM.getElement(elem);
        
        var self = this;
        var req = Ajax.JSON.post(url, params);
        
        req.addCallback(function(obj) {
            self._render(obj.data);            
        });
    },
    
    _render : function(data) {
        
        var colors = ChartColors.slice(0, data.dataset.length);
        var dim = MochiKit.DOM.elementDimensions(this.element);

        var so = new SWFObject("/static/open-flash-chart.swf", 'swf_' + this.element.id, dim.w, dim.h, "9", "#FFFFFF");

        so.addVariable("variables","true");
        
        so.addVariable('title', data.title + ',{font-size: 20}');
        so.addVariable('y_legend', data.y_legend +',12,#000000');
        
        so.addVariable("y_label_size","15");
        
        //TODO: auto detact min/max and steps
        so.addVariable("y_max", data.y_max || 20);
        so.addVariable("y_min", data.y_min || 0);
        so.addVariable("y_ticks", '5,20,' + (data.y_steps||2));
        
        for(var i=0; i<data.dataset.length; i++) {
            
            var d = data.dataset[i];
            
            so.addVariable(i == 0 ? 'bar' : 'bar_' + (i+1), '80,' + colors[i] + ',' + d.legend + ',' + 12);
            so.addVariable(i == 0 ? 'values' : 'values_' + (i+1), d.values.join(','));
        }
        
        so.addVariable("x_labels", data.x_labels.join(','));
        so.addVariable("x_axis_steps", data.x_steps || 1);
        
        so.addParam("allowScriptAccess", "always" )
        
        so.write(this.element.id);
    }
}

var PieChart = function(elem, url, params) {
    this.__init__(elem, url, params);
}

PieChart.prototype = {
    
    __init__ : function(elem, url, params) {
        
        this.element = MochiKit.DOM.getElement(elem);
        
        var self = this;
        var req = Ajax.JSON.post(url, params);
        
        req.addCallback(function(obj) {
            self._render(obj.data);            
        });
    },
    
    _render : function(data) {
        
        if (!data) return;
        
        var colors = ChartColors.slice(0, data.dataset.length);
        var dim = MochiKit.DOM.elementDimensions(this.element);
        
        var so = new SWFObject("/static/open-flash-chart.swf", this.element.id + '_chart', dim.w, dim.h, "9", "#FFFFFF");
        
        so.addVariable("variables","true");
        so.addVariable('title', data.title + ',{font-size: 20}');

        var values = [];
        var labels = [];
        var links = [];
        
        for(var i=0; i<data.dataset.length; i++) {
            
            var d = data.dataset[i];
            labels = labels.concat(d.legend);
            values = values.concat(d.value);
            links = links.concat(d.link);
        }
        
        so.addVariable("pie", "80, #9933CC, {font-size: 12px; color: #000000;}");
        so.addVariable("pie_labels", labels.join(','));
        so.addVariable("values", values.join(','));
        so.addVariable("colours", colors.join(','));
        so.addVariable("links", links.join(','));
        
        so.addParam("allowScriptAccess", "always" )
        so.write(this.element.id);        
    }
}

