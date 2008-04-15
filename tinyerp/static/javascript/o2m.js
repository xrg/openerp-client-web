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

var One2Many = function(name, inline){
    
    this.name = name;
    this.inline = inline > 0;
    
    this.model = $(name + '/_terp_model').value;
    this.mode = $(name + '/_terp_view_type').value;
    
    this.default_get_ctx = $(name + '/_terp_default_get_ctx').value; 
    
    var parent_prefix = name.indexOf('/') > -1 ? name.slice(0, name.lastIndexOf('/')+1) : '';
    
    this.parent_model = $(parent_prefix + '_terp_model').value;
    this.parent_id = $(parent_prefix + '_terp_id').value;
    this.parent_view_id = $(parent_prefix + '_terp_view_id').value;
}

One2Many.prototype = {
    
    create : function(){

        if (!this.parent_id || this.parent_id == 'False' || this.mode == 'form'){
            return submit_form('save', this.name);
        }
    
        if (this.mode == 'tree' && this.inline){
            return new ListView(this.name).create();
        }
        
        this.edit(null);    
    },
    
    edit : function(id, readonly){

        var args = {_terp_parent_model: this.parent_model,
        			_terp_parent_id: this.parent_id,
                    _terp_parent_view_id: this.parent_view_id,
                    _terp_o2m: this.name,
                    _terp_o2m_model: this.model,
                    _terp_o2m_id: id,
                    _terp_editable: readonly ? 0 : 1};
                    
        if (id && id != 'False' && !this.default_get_ctx){
            return openWindow(getURL('/openo2m/edit', args));
        }
        
        var req = eval_domain_context_request({source: this.name, context : this.default_get_ctx});
        
        req.addCallback(function(res){
            args['_terp_o2m_context'] = res.context;
            return openWindow(getURL('/openo2m/edit', args));
        });
    
    }
}

// vim: sts=4 st=4 et
