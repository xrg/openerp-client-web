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

var ListView = function(name) {

//    var elem = openobject.dom.get(name);
    var elem = jQuery('[id="'+name+'"]').get()
    
    if (elem.__listview) {
        return elem.__listview;
    }
    var cls = arguments.callee;
    if (!(this instanceof cls)) {
        return new cls(name);
    }

    this.__init__(name);
};

ListView.prototype = {

    __init__: function(name) {

        var prefix = name == '_terp_list' ? '' : name + '/';
		
        this.name = name;
        this.model = $('[id*="'+prefix + '_terp_model'+'"]').get() ? $('[id*="'+prefix + '_terp_model'+'"]').val() : null;
        
        this.current_record = null;

        this.ids = $('[id*="'+prefix + '_terp_ids'+'"]').val();

        this.view_ids = $('[id*="'+prefix + '_terp_view_ids'+'"]').get() ? $('[id*="'+prefix + '_terp_view_ids'+'"]').val() : null;
        this.view_mode = $('[id*="'+prefix + '_terp_view_mode'+'"]').get() ? $('[id*="'+prefix + '_terp_view_mode'+'"]').val() : null;

        // if o2m
		
        this.m2m = $('[id*="'+ name + '_set' + '"]');
		this.default_get_ctx = $('[id*="' + prefix + '_terp_default_get_ctx' + '"]').get() ? $('[id*="' + prefix + '_terp_default_get_ctx' + '"]').val() : null;
		this.sort_key = null;
		this.sort_key_order = null;
		this.sort_domain = "[]";
		
        // save the reference
        $('[id*="'+name+'"]:first').__listview = this;
    },

    checkAll: function(clear) {

        clear = clear ? false : true;
        
        $('[id*="'+this.name+'"]:first').find(':checkbox').each(function(i) {
			$(this).attr('checked', clear)
		});
        
        var sb = openobject.dom.get('sidebar');
        if (sb) toggle_sidebar();
        
        this.selectedRow_sum();
    },
	
	selectedRow_sum: function() {
		if(jQuery('tr.field_sum').find('td.grid-cell').find('span').length>0) {
        	var selected_ids = this.getSelectedRecords();
	    	var sum_fields = [];
	    	 
	    	jQuery('tr.field_sum').find('td.grid-cell').find('span').each(function() {
	    		sum_fields.push(jQuery(this).attr('id'))
	    	});
	    	
	    	var selected_fields = sum_fields.join(",");
	    	var selected_ids = '[' + selected_ids.join(',') + ']';
	    	
	    	if(selected_ids == '[]') {
	    			selected_ids =this.ids;
	    	}
	    	
	    	jQuery.ajax({
	    		url: '/listgrid/count_sum',
	    		type: 'POST',
	    		data: {'model':this.model, 'ids': selected_ids, 'sum_fields': selected_fields},
	    		dataType: 'json',
	    		success: function(obj) {
	    			for(i in obj.sum) {
						jQuery('tr.field_sum').find('td.grid-cell').find('span[id="'+sum_fields[i]+'"]').html(obj.sum[i])
					}
	    		}
	    	});
        }	
	},
	
    getRecords: function() {
        var records = map(function(row) {
            return parseInt(getNodeAttribute(row, 'record')) || 0;
        }, openobject.dom.select('tr.grid-row', this.name));

        return filter(function(rec) {
            return rec;
        }, records);
    },

    getSelectedRecords: function() {
        return map(function(box) {
            return box.value;
        }, this.getSelectedItems());
    },

    getSelectedItems: function() {
        return filter(function(box) {
            return box.id && box.checked;
//            $('input.grid-record-selector')
        }, openobject.dom.select('input.grid-record-selector', this.name));
    },

    onBooleanClicked: function(clear, value) {
        var selected_ids = this.getSelectedRecords()
        var sb = openobject.dom.get('sidebar');

        if (selected_ids.length <= 1) {
            if (sb){
                if(sb.style.display != '') {toggle_sidebar() };
            }
        }
        if (selected_ids.length == 0) {
            if (sb) toggle_sidebar();
        }
        
       	this.selectedRow_sum();
    },

    getColumns: function(dom) {
        dom = dom || this.name;
        var header = openobject.dom.select('tr.grid-header', dom)[0];

        return filter(function(c) {
            return c.id ? true : false;
        }, openobject.dom.select('th.grid-cell', header));
    },

    makeArgs: function() {
        var args = {};
        var names = ('/' + this.name).split('/');

        var prefix = '';
        var items = openobject.dom.select('input');

        while (names.length) {

            var name = names.shift();
            prefix = prefix + (name ? name + '/' : '');

            var pattern = prefix + '_terp_';

            forEach(items, function(item) {
                if (item.name.match("^" + pattern) == pattern && !item.name.match('^_terp_listfields/')) {
                    args[item.name] = item.value;
                }
            });
        }

        return args;
    }
};

// inline editor related functions
MochiKit.Base.update(ListView.prototype, {

    adjustEditors: function(newlist) {

        var editors = this.getEditors(false, newlist);
        forEach(editors, function(e) {
            // disable autocomplete (Firefox < 2.0 focus bug)
            setNodeAttribute(e, 'autocomplete', 'OFF');
        });

        if (/MSIE/.test(navigator.userAgent)) {
            return editors;
        }

        var columnWidths = {};
        // set the column widths of the newlist
        forEach(this.getColumns(), function(c) {
            columnWidths[c.id] = parseInt(c.offsetWidth) - 8;
        });

        forEach(this.getColumns(newlist), function(c) {
            c.style.width = columnWidths[c.id] + 'px';
        });

        var editorWidths = {};
        forEach(this.getEditors(), function(e) {
            editorWidths[e.id] = parseInt(e.offsetWidth);
        });

        return editors;
    },

    bindKeyEventsToEditors: function(editors) {
        var self = this;
        var enabledEditors = filter(function(e) {
            return e.type != 'hidden' && !e.disabled
        }, editors);

        forEach(enabledEditors, function(e) {
            connect(e, 'onkeydown', self, self.onKeyDown);
            addElementClass(e, 'listfields');
        });
    },

    getEditors: function(named, dom) {
        var dom = dom ? dom : this.name;

        var editors = openobject.dom.select("input, select, textarea", dom);

        return filter(function(e) {
            name = named ? e.name : e.id;
            return name && name.indexOf('_terp_listfields') == 0;
        }, editors);
    }

});

// pagination & reordering
MochiKit.Base.update(ListView.prototype, {
	
    sort_by_order: function(column) {
        var self = this;
        
        if(this.sort_key == column) {
        	if(this.sort_key_order == 'asc') {
        		order = 'desc';
        	}
        	else {
        		order = 'asc';
        	}
        }	
    	else {
    		this.sort_key_order = null;
    		if(this.sort_key_order == 'asc') {
        		order = 'desc';
        	}
        	else {
        		order = 'asc';
        	}
    	}
        
        if(jQuery('input[id$="' + this.name + '/_terp_ids'+'"]').get().length > 0) {
        	ids = jQuery('input[id$="' + this.name + '/_terp_ids' + '"]').val();
        	this.sort_domain = domain = "[('id','in'," + ids + ")]";
        	filter_domain = search_domain = "[]";
        }
        else {
        	ids = this.ids;
        	domain = "[]";
        	search_domain = "[]";
        	filter_domain = jQuery('input[id=_terp_filter_domain]').val() || "[]";
        	if(jQuery('input[id=_terp_search_domain]').val() != '' && jQuery('input[id=_terp_search_domain]').val() != 'None') {
        		search_domain = jQuery('input[id=_terp_search_domain]').val();
        	}
        }
        
        if(eval(ids).length > 0) {
        	jQuery.post(
    			'/openerp/listgrid/sort_by_order',
    			{'model': this.model, 'column': column, 'domain': domain, 'search_domain': search_domain, 'filter_domain': filter_domain, 'order': order},
    			function(obj) {
    				if(obj.error) {
    					alert('error' + obj.error)
    				}
    				else {
    					var _terp_id = openobject.dom.get(self.name + '/_terp_id') || openobject.dom.get('_terp_id');
            			var _terp_ids = openobject.dom.get(self.name + '/_terp_ids') || openobject.dom.get('_terp_ids');
            			_terp_ids.value = '[' + obj.ids.join(',') + ']';
            			_terp_id.value = obj.ids.length ? obj.ids[0] : 'False';
    					self.reload();
    				}
    			},
    			"json"
        	);
        	this.sort_key = column;
        	this.sort_key_order = order;
        }
    },
    
    group_by: function(id, record, no_leaf, group) {
        var group_record = jQuery('[records="' + record + '"]');
        var group_by_context = jQuery(group_record).attr('grp_context');
        var domain = jQuery(group_record).attr('grp_domain');
        var total_groups = jQuery('#' + this.name).attr('groups');
        
        if (group_by_context == '[]') {
            jQuery('[parent_grp_id="' + id + '"][id$="' + record + '"]').toggle();
        } else {
            if (jQuery(group).hasClass('group-expand')) {
                jQuery.ajax({
                    url: '/listgrid/multiple_groupby',
                    type: 'POST',
                    data: { 'model': this.model, 'name': this.name,
                            'grp_domain': domain, 'group_by': group_by_context,
                            'view_id': jQuery('#_terp_view_id').val(),
                            'view_type': jQuery('#_terp_view_type').val(),
                            'parent_group': record,
                            'group_level': jQuery(group).index() + 1,
                            'groups': total_groups,
                            'no_leaf': no_leaf},
                    dataType: 'html',
                    success: function(xmlHttp) {
                        jQuery(group_record).after(xmlHttp);
                    }
                });
            } else {
                jQuery('[parent="' + record + '"]').each(function() {
                    var parent_id = jQuery('[parent="' + record + '"]').attr('records');
                    if (jQuery('[parent="' + parent_id + '"]').length > 0) {
                        jQuery('[parent="' + parent_id + '"]').remove();
                    }
                    jQuery(this).remove();
                })
            }
        }
        
        jQuery(group).toggleClass('group-collapse group-expand');
    },

    groupbyDrag: function(drag, drop) {
        var view = jQuery('table.grid[id$=grid]').attr('id').split("_grid")[0];
        var _list_view = new ListView(view);
        var domain;
        var children;
        if(jQuery(drop).attr('record')) {
            var dropGroup = jQuery(drop).attr('id').split('grid-row ')[1];
            domain = jQuery('tr.grid-row-group[records="'+dropGroup+'"]').attr('grp_domain');
        } else {
            domain = jQuery(drop).attr('grp_domain');
        }

        if(jQuery(drag).attr('ch_records')) {
            children = jQuery(drag).attr('ch_records')
        } else {
            if(drag.id == drop.id) {
                var dragGroup = jQuery(drag).attr('id').split('grid-row ')[1];
                children = jQuery('tr.grid-row-group[records="'+dragGroup+'"]').attr('ch_records')
            } else {
                children = jQuery(drag).attr('record')
            }
        }

        if((jQuery(drag).attr('record') && jQuery(drop).attr('record')) && (jQuery(drag).attr('id')) == jQuery(drop).attr('id')) {
            _list_view.dragRow(drag, drop);
        } else {
            jQuery.post(
                '/openerp/listgrid/groupbyDrag',
                {'model': _list_view.model, 'children': children, 'domain': domain},
                function () { _list_view.reload(); },
                "json");
        }

        MochiKit.Async.wait(2).addCallback(function() {
            var id = jQuery('tr.grid-row-group[grp_domain="'+domain+'"]').attr('records');
            toggle_group_data(id)
        });
    },

    dragRow: function(drag, drop, event) {
        var view = jQuery(drag).parent().parent().attr('id').split("_grid")[0];
        var _list_view = new ListView(view);
            jQuery.post('/openerp/listgrid/dragRow',
	            {'_terp_model': _list_view.model,
	             '_terp_ids': _list_view.ids,
	             '_terp_id': jQuery(drag).attr('record'),
	             '_terp_swap_id': jQuery(drop).attr('record')},
	            function () { _list_view.reload(); },
            "json");
    },

    moveUp: function(id) {

        var self = this;
        var args = {};

        args['_terp_model'] = this.model;
        args['_terp_ids'] = this.ids;
        args['_terp_id'] = id;

        var req = openobject.http.postJSON('/openerp/listgrid/moveUp', args);
        req.addCallback(function() {
            self.reload();
        });
    },

    moveDown: function(id) {

        var self = this;
        var args = {
            '_terp_model': this.model,
            '_terp_ids': this.ids,
            '_terp_id': id
        };

        var req = openobject.http.postJSON('/openerp/listgrid/moveDown', args);
        req.addCallback(function() {
            self.reload();
        });
    }
});

// event handlers
MochiKit.Base.update(ListView.prototype, {

    onKeyDown: function(evt) {
        var key = evt.key();
        var src = evt.src();

        if (!(key.string == "KEY_TAB" || key.string == "KEY_ENTER" || key.string == "KEY_ESCAPE")) {
            return;
        }

        if (key.string == "KEY_ESCAPE") {
            evt.stop();
            return this.reload();
        }

        if (key.string == "KEY_ENTER") {

            if (hasElementClass(src, "m2o")) {

                var k = src.id;
                k = k.slice(0, k.length - 5);

                if (src.value && !openobject.dom.get(k).value) {
                    return;
                }
            }

            if (src.onchange) {
                src.onchange();
            }

            evt.stop();
            return this.save(this.current_record);
        }

        var editors = openobject.dom.select('listfields', this.name);

        var first = editors.shift();
        var last = editors.pop();

        if (src == last) {
            evt.stop();
            first.focus();
            first.select();
        }
    },

    onButtonClick: function(name, btype, id, sure, context) {

        if (sure && !confirm(sure)) {
            return;
        }

        var self = this;
        var prefix = this.name == '_terp_list' ? '' : this.name + '/';

        if (btype == "open") {
            return window.open(get_form_action('/openerp/form/edit', {
                id: id,
//                ids: $('[id*="'+prefix + '_terp_ids'+'"]').val(),
                ids: openobject.dom.get(prefix + '_terp_ids').value,
                model: openobject.dom.get(prefix + '_terp_model').value,
//                model: $('[id*="'+prefix + '_terp_model'+'"]').val(),
                view_ids: openobject.dom.get(prefix + '_terp_view_ids').value,
//                view_ids: $('[id*="'+prefix + '_terp_view_ids'+'"]').val(),
                domain: openobject.dom.get(prefix + '_terp_domain').value,
//                domain: $('[id*="'+prefix + '_terp_domain'+'"]').val(),
                context: openobject.dom.get(prefix + '_terp_context').value,
//                context: $('[id*="'+prefix + '_terp_context'+'"]').val(),
                limit: openobject.dom.get(prefix + '_terp_limit').value,
//                limit: $('[id*="'+prefix + '_terp_limit'+'"]').val(),
                offset: openobject.dom.get(prefix + '_terp_offset').value,
//                offset: $('[id*="'+prefix + '_terp_offset'+'"]').val(),
                count: openobject.dom.get(prefix + '_terp_count').value}));
        }

        name = name.split('.').pop();

        var params = {
            _terp_model : this.model,
            _terp_id : id,
            _terp_button_name : name,
            _terp_button_type : btype
        };

        var req = eval_domain_context_request({source: this.name, context : context || '{}'});
        req.addCallback(function(res) {
            params['_terp_context'] = res.context;
            var req = openobject.http.postJSON('/openerp/listgrid/button_action', params);
            req.addCallback(function(obj) {
                if (obj.error) {
                    return alert(obj.error);
                }

                if (obj.result && obj.result.url) {
                    window.open(obj.result.url);
                }
                
                if(obj.wiz_result){
                	var act = get_form_action('action');
                	MochiKit.Base.update(params, {
                		'_terp_action': obj.wiz_result.action_id,
                		'_terp_id': obj.wiz_result.id,
                		'_terp_model': obj.wiz_result.model});
                	window.open(openobject.http.getURL(act, params))
                }

                if (obj.reload) {
                    window.location.reload();
                } else {
                    self.reload();
                }
            });
        });
    }
});

// standard actions
MochiKit.Base.update(ListView.prototype, {

    create: function(default_get_ctx) {
        this.edit(-1, default_get_ctx);
    },

    edit: function(edit_inline, default_get_ctx) {
        this.reload(edit_inline, null, default_get_ctx);
    },

    save: function(id) {

        if (openobject.http.AJAX_COUNT > 0) {
            return callLater(1, bind(this.save, this), id);
        }

        var parent_field = this.name.split('/');
        var data = getFormData(2);
        var args = getFormParams('_terp_concurrency_info');

        for (var k in data) {
            if (k.indexOf(this.name + '/') == 0 || this.name == '_terp_list') {
                args[k] = data[k];
            }
        }

        var prefix = this.name == '_terp_list' ? '' : this.name + '/';

        args['_terp_id'] = id ? id : -1;
        args['_terp_ids'] = openobject.dom.get(prefix + '_terp_ids').value;
        args['_terp_model'] = this.model;

        if (parent_field.length > 0) {
            parent_field.pop();
        }

        parent_field = parent_field.join('/');
        parent_field = parent_field ? parent_field + '/' : '';

        args['_terp_parent/id'] = openobject.dom.get(parent_field + '_terp_id').value;
        args['_terp_parent/model'] = openobject.dom.get(parent_field + '_terp_model').value;
        args['_terp_parent/context'] = openobject.dom.get(parent_field + '_terp_context').value;
        args['_terp_source'] = this.name;

        var self = this;
        var req = openobject.http.postJSON('/openerp/listgrid/save', args);

        req.addCallback(function(obj) {
            if (obj.error) {
                alert(obj.error);

                if (obj.error_field) {
                    var fld = openobject.dom.get('_terp_listfields/' + obj.error_field);

                    if (fld && getNodeAttribute(fld, 'kind') == 'many2one') {
                        fld = openobject.dom.get(fld.id + '_text');
                    }

                    if (fld) {
                        fld.focus();
                        fld.select();
                    }
                }
            } else {

                openobject.dom.get(prefix + '_terp_id').value = obj.id;
                openobject.dom.get(prefix + '_terp_ids').value = obj.ids;

                self.reload(id > 0 ? null : -1, prefix ? 1 : 0);
            }
        });
    },

    remove: function(ids) {

        var self = this;
        var args = getFormParams('_terp_concurrency_info');


        if (!ids) {
            var ids = this.getSelectedRecords();
            if (ids.length > 0) {
                ids = '[' + ids.join(', ') + ']';
            }
        }

        if (ids.length == 0) {
        	jQuery('div.message-box').show().html(_('You must select at least one record.')); // show and set the message
        	return setTimeout(function(){ jQuery('div.message-box').fadeOut("slow").html('')}, 3000);
        } 
        else if (!confirm(_('Do you really want to delete selected record(s) ?'))) {
            return false;
        }

        args['_terp_model'] = this.model;
        args['_terp_ids'] = ids;

        var req = openobject.http.postJSON('/openerp/listgrid/remove', args);

        req.addCallback(function(obj) {
            if (obj.error) {
                alert(obj.error);
            } else {
                self.reload();
            }
        });
    },

    go: function(action) {

        if (openobject.http.AJAX_COUNT > 0) {
            return;
        }

        var prefix = this.name == '_terp_list' ? '' : this.name + '/';

        var o = openobject.dom.get(prefix + '_terp_offset');
        var l = openobject.dom.get(prefix + '_terp_limit');
        var c = openobject.dom.get(prefix + '_terp_count');

        var ov = o.value ? parseInt(o.value) : 0;
        var lv = l.value ? parseInt(l.value) : 0;
        var cv = c.value ? parseInt(c.value) : 0;

        switch (action) {
            case 'next':
                o.value = ov + lv;
                break;
            case 'previous':
                o.value = lv > ov ? 0 : ov - lv;
                break;
            case 'first':
                o.value = 0;
                break;
            case 'last':
                o.value = cv - (cv % lv);
                break;
        }

        this.reload();
    },

    reload: function(edit_inline, concurrency_info, default_get_ctx) {

        if (openobject.http.AJAX_COUNT > 0) {
            return callLater(1, bind(this.reload, this), edit_inline, concurrency_info);
        }

        var self = this;
        var args = this.makeArgs();
        
        var current_id = edit_inline ? (parseInt(edit_inline) || 0) : edit_inline;
        
        // add args
        args['_terp_source'] = this.name;
        args['_terp_edit_inline'] = edit_inline;
        args['_terp_source_default_get'] = default_get_ctx;
        args['_terp_concurrency_info'] = concurrency_info;
        args['_terp_group_by_ctx'] = openobject.dom.get('_terp_group_by_ctx').value;
        
        if (this.name == '_terp_list') {
            args['_terp_search_domain'] = openobject.dom.get('_terp_search_domain').value;
            args['_terp_search_data'] = openobject.dom.get('_terp_search_data').value;
            args['_terp_filter_domain'] = openobject.dom.get('_terp_filter_domain').value;
        }
        
        if(this.sort_key) {
        	args['_terp_sort_key'] = this.sort_key;
        	args['_terp_sort_order'] = this.sort_key_order;
        	args['_terp_sort_model'] = self.model
        	args['_terp_sort_domain'] = this.sort_domain;
        	if(self.name !='_terp_list') {
        		args['_terp_o2m'] = self.name;
        	}
        }
        
        var req = openobject.http.postJSON('/openerp/listgrid/get', args);
        req.addCallback(function(obj) {
            var _terp_id = openobject.dom.get(self.name + '/_terp_id') || openobject.dom.get('_terp_id');
            var _terp_ids = openobject.dom.get(self.name + '/_terp_ids') || openobject.dom.get('_terp_ids');
            var _terp_count = openobject.dom.get(self.name + '/_terp_count') || openobject.dom.get('_terp_count');
            _terp_id.value = current_id > 0 ? current_id : 'False';
            
            if (obj.ids) {
                if (typeof(current_id) == "undefined" && obj.ids.length) {
                    current_id = obj.ids[0];
                }
                _terp_id.value = current_id > 0 ? current_id : 'False';
                _terp_ids.value = '[' + obj.ids.join(',') + ']';
                _terp_count.value = obj.count;
            }

            var d = DIV();
            d.innerHTML = obj.view;

            var newlist = d.getElementsByTagName('table')[0];
            var editors = self.adjustEditors(newlist);

            if (editors.length > 0) {
                self.bindKeyEventsToEditors(editors);
            }

            self.current_record = edit_inline;
			
            var __listview = openobject.dom.get(self.name).__listview;
            swapDOM(self.name, newlist);
            openobject.dom.get(self.name).__listview = __listview;
			
            var ua = navigator.userAgent.toLowerCase();

            if ((navigator.appName != 'Netscape') || (ua.indexOf('safari') != -1)) {
                // execute JavaScript
                var scripts = openobject.dom.select('script', newlist);
                forEach(scripts, function(s) {
                    eval(s.innerHTML);
                });
            }

            // update concurrency info
            for (var key in obj.info) {
                try {
                    var items = openobject.dom.select("[name=_terp_concurrency_info][value*=" + key + "]");
                    var value = "('" + key + "', '" + obj.info[key] + "')";
                    for (var i = 0; i < items.length; i++) {
                        items[i].value = value;
                    }
                } catch(e) {
                }
            }

            // set focus on the first field
            var first = openobject.dom.select('listfields', self.name)[0] || null;
            if (first) {
                first.focus();
                first.select();
            }

            // call on_change for default values
            if (editors.length && edit_inline == -1) {
                forEach(editors, function(e) {
                    if (e.value && getNodeAttribute(e, 'callback')) {
                        MochiKit.Signal.signal(e, 'onchange');
                    }
                });
            }

            MochiKit.Signal.signal(__listview, 'onreload');
            
            if(self.sort_key != null) {
            	if(self.name !='_terp_list') {
            		var th = jQuery('th[id= grid-data-column/' + self.name + '/' + self.sort_key + ']').get();
            	}	
            	else {
            		var th = jQuery('th[id= grid-data-column/' + self.sort_key + ']').get();
            	}	
            		
            	var detail = jQuery(th).html();
            	
				if(self.sort_key_order == 'asc') {
					jQuery(th).html(detail + '&nbsp; <img src="/openerp/static/images/listgrid/arrow_down.gif" style="vertical-align: middle;"/>');
				}
				else { 
					jQuery(th).html(detail + '&nbsp; <img src="/openerp/static/images/listgrid/arrow_up.gif" style="vertical-align: middle;"/>');
				}		
			}
        });
    }
});

// export/import functions
MochiKit.Base.update(ListView.prototype, {

    exportData: function() {

        var ids = this.getSelectedRecords();

        if (ids.length == 0) {
            ids = this.getRecords();
        }

        ids = '[' + ids.join(',') + ']';

        openobject.tools.openWindow(openobject.http.getURL('/openerp/impex/exp', {_terp_model: this.model,
            _terp_source: this.name,
            _terp_context: $('_terp_context').value,
            _terp_search_domain: openobject.dom.get('_terp_search_domain').value,
            _terp_ids: ids,
            _terp_view_ids : this.view_ids,
            _terp_view_mode : this.view_mode}));
    },

    importData: function() {
        openobject.tools.openWindow(openobject.http.getURL('/openerp/impex/imp', {_terp_model: this.model,
            _terp_context: $('_terp_context').value,
            _terp_source: this.name,
            _terp_view_ids : this.view_ids,
            _terp_view_mode : this.view_mode}));
    }
});
