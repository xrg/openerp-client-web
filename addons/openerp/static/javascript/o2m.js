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

var One2Many = function(name, inline) {
    
    this.name = name;
    this.inline = inline > 0;
    
    this.model = openobject.dom.get(name + '/_terp_model').value;
    this.mode = openobject.dom.get(name + '/_terp_view_type').value;
    
    if (openobject.dom.get(name + '/_terp_default_get_ctx'))
    	this.default_get_ctx = openobject.dom.get(name + '/_terp_default_get_ctx').value; 
    
    var parent_prefix = name.indexOf('/') > -1 ? name.slice(0, name.lastIndexOf('/')+1) : '';
    
    this.parent_model = openobject.dom.get(parent_prefix + '_terp_model').value;
    this.parent_id = openobject.dom.get(parent_prefix + '_terp_id').value;
    this.parent_context = openobject.dom.get(parent_prefix + '_terp_context').value;
    this.parent_view_id = openobject.dom.get(parent_prefix + '_terp_view_id').value;
    
    // hide new button when editors are visible
    if (this.mode == 'tree' && this.inline){ 
        var self = this;
        this.btn_new = openobject.dom.get(this.name + '_btn_');
        MochiKit.Signal.connect(ListView(this.name), 'onreload', function(evt) {
            self.btn_new.style.display = ListView(self.name).getEditors().length > 0 ? 'none': '';
        });
    }
}

One2Many.prototype = {

    create: function() {

        if (!this.parent_id || this.parent_id == 'False' || this.mode == 'form'){
            return submit_form('save', this.name);
        }
    
        if (this.mode == 'tree' && this.inline){
        
            if (this.default_get_ctx) {
                var self = this;
                var req = eval_domain_context_request({source: this.name, context: this.default_get_ctx});
                req.addCallback(function(res){
                    ListView(self.name).create(res.context);
                });
            } else {
                ListView(this.name).create();
            }
        } else {
            this.edit(null);
        }
    },

    edit: function(id, readonly) {

        var names = this.name.split('/');

        var parents = [];
        var params = {};

        // get the required view params to get proper view
        params['_terp_view_params/_terp_model'] = openobject.dom.get('_terp_model').value;
        params['_terp_view_params/_terp_view_ids'] = openobject.dom.get('_terp_view_ids').value;
        params['_terp_view_params/_terp_view_mode'] = openobject.dom.get('_terp_view_mode').value;
        params['_terp_view_params/_terp_view_type'] = 'form';

        while(names.length) {

            parents.push(names.shift());
            var prefix = parents.join('/');

            params['_terp_view_params/' + prefix + '/_terp_model'] = openobject.dom.get(prefix + '/_terp_model').value;
            params['_terp_view_params/' + prefix + '/_terp_view_ids'] = openobject.dom.get(prefix + '/_terp_view_ids').value;
            params['_terp_view_params/' + prefix + '/_terp_view_mode'] = openobject.dom.get(prefix + '/_terp_view_mode').value;
            params['_terp_view_params/' + prefix + '/_terp_view_type'] = 'form';
        }

        MochiKit.Base.update(params, {
                _terp_parent_model: this.parent_model,
        		_terp_parent_id: this.parent_id,
                _terp_parent_view_id: this.parent_view_id,
                _terp_o2m: this.name,
                _terp_o2m_model: this.model,
                _terp_o2m_id: id,
                _terp_editable: readonly ? 0 : 1});
                    
        if (id && id != 'False' && !this.default_get_ctx){
            return openobject.tools.openWindow(openobject.http.getURL('/openerp/openo2m/edit', params));
        }
        
        var req = eval_domain_context_request({source: this.name, context : this.default_get_ctx});
        
        req.addCallback(function(res){
        
            //XXX: IE hack, long context value generate long URI
            if (!window.browser.isIE) {
                params['_terp_o2m_context'] = res.context;
                params['_terp_parent_context'] = this.parent_context;
                return openobject.tools.openWindow(openobject.http.getURL('/openerp/openo2m/edit', params));
            }
            
            openobject.http.setCookie('_terp_o2m_context', res.context || '{}');
            openobject.http.setCookie('_terp_parent_context', this.parent_context || '{}');
            try {
                return openobject.tools.openWindow(openobject.http.getURL('/openerp/openo2m/edit', params));
            } finally {
                openobject.http.delCookie('_terp_o2m_context');
                openobject.http.delCookie('_terp_parent_context');
            }
        });
    }
}

// vim: ts=4 sts=4 sw=4 si et

