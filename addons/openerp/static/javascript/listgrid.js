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
// -   All names, links and logos of Tiny, OpenERP and Axelor must be
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
    var elem = jQuery('[id="'+name+'"]').get(0);

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
        this.model = jQuery('[id*="'+prefix + '_terp_model'+'"]').get() ? jQuery('[id*="'+prefix + '_terp_model'+'"]').val() : null;
        this.current_record = null;

        this.ids = jQuery('[id*="'+prefix + '_terp_ids'+'"]').val();

        this.view_ids = jQuery('[id*="'+prefix + '_terp_view_ids'+'"]').get() ? jQuery('[id*="'+prefix + '_terp_view_ids'+'"]').val() : null;
        this.view_id = jQuery('[id="'+prefix + '_terp_view_id'+'"]').get() ? jQuery('[id="'+prefix + '_terp_view_id'+'"]').val() : null;
        this.view_mode = jQuery('[id*="'+prefix + '_terp_view_mode'+'"]').get() ? jQuery('[id*="'+prefix + '_terp_view_mode'+'"]').val() : null;
        this.view_type = jQuery('[id*="'+prefix + '_terp_view_type'+'"]').get() ? jQuery('[id*="'+prefix + '_terp_view_type'+'"]').val() : null;

        // if o2m

        this.m2m = jQuery('[id*="'+ name + '_set' + '"]');
        this.default_get_ctx = jQuery('[id*="' + prefix + '_terp_default_get_ctx' + '"]').get() ? jQuery('[id*="' + prefix + '_terp_default_get_ctx' + '"]').val() : null;
        // save the reference
        jQuery('[id="'+name+'"]').get(0).__listview = this;

        this.sort_order = null;
        this.sort_key = null;
    },

    checkAll: function(clear) {
        jQuery('[id="' + this.name + '"]:first :checkbox').each(function() {
            jQuery(this).attr('checked', !clear)
        });

        this.onBooleanClicked();
    },

    selectedRow_sum: function() {
        var selected_ids = this.getSelectedRecords();
        var $buttons = jQuery('[id="'+this.name+'_delete_record'+'"], [id="'+this.name+'_edit_record'+'"]');

        if(selected_ids.length) {
            $buttons.parent().show();
        }
        else {
            $buttons.parent().hide();
        }

        if(jQuery('table[id="'+this.name+'"] tr.field_sum td.grid-cell span').length>0) {
            var sum_fields = jQuery('tr.field_sum td.grid-cell span').map(function() {
                return jQuery(this).attr('id');
            }).get();

            var selected_fields = sum_fields.join(",");
            if(selected_ids.length) {
                selected_ids = '[' + selected_ids.join(',') + ']';
            } else if(this.ids) {
                selected_ids = this.ids;
            }
            jQuery.ajax({
                url: '/openerp/listgrid/count_sum',
                type: 'POST',
                data: {
                    'model':this.model,
                    'ids': selected_ids,
                    'sum_fields': selected_fields},
                dataType: 'json',
                success: function(obj) {
                    for(var i in obj.sum) {
                        jQuery('tr.field_sum td.grid-cell span[id="' + sum_fields[i] + '"]').html(obj.sum[i])
                    }
                }
            });
        }
    },

    getRecords: function() {
        return jQuery(openobject.dom.select('tr.grid-row', this.name)).map(function () {
            return parseInt(jQuery(this).attr('record')) || 0;
        }).filter(function () {
            return !!this;
        }).get();
    },

    getSelectedRecords: function() {
        return jQuery(this.getSelectedItems()).map(function() {
            if(this.value) {
                return this.value
            } else {
                var box_id = this.id.split('/');
                return box_id[box_id.length - 1]
            }
        }).get();
    },

    getSelectedItems: function() {
        return filter(function(box) {
            return box.id && box.checked;
        }, openobject.dom.select('input.grid-record-selector', this.name));
    },

    onBooleanClicked: function() {
        var $sidebar = jQuery('.toggle-sidebar');
        if ($sidebar.is('.closed')) {
            $sidebar.click()
        }
        if(!this.getSelectedRecords().length) {
            $sidebar.click();
        }

           this.selectedRow_sum();
    },

    getColumns: function(dom) {
        var header = openobject.dom.select('tr.grid-header', dom || this.name)[0];

        return jQuery(header).find('th.grid-cell').filter(function () {
            return !!this.id;
        }).get();
    },

    makeArgs: function() {
        var args = {};
        var names = ('/' + this.name).split('/');

        var prefix = '';
        var items = openobject.dom.select('input');

        while (names.length) {

            var name = names.shift();
            prefix += (name ? name + '/' : '');

            var pattern = prefix + '_terp_';

            forEach(items, function(item) {
                if (item.name.match("^" + pattern) == pattern && !item.name.match(/^_terp_listfields\//)) {
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
        return this.$getEditors(false, newlist).each(function(){
            var $this = jQuery(this);
            var $cell = $this.parent('.grid-cell');
            $this.attr('autocomplete', 'OFF').width($cell.width());
        }).get();
    },

    bindKeyEventsToEditors: function(editors) {
        var self = this;
        jQuery(editors).filter(function () {
            return this.type != 'hidden' && !this.disabled;
        }).each(function () {
            jQuery(this).addClass('listfields');
            connect(this, 'onkeydown', self, self.onKeyDown);
        });
    },

    $getEditors: function(named, dom) {
        return jQuery(openobject.dom.select("input, select, textarea", dom ? dom : this.name)).filter(function() {
            var name = named ? this.name : this.id;
            return name && name.indexOf('_terp_listfields') == 0;
        });
    }

});

// pagination & reordering
MochiKit.Base.update(ListView.prototype, {

    sort_by_order: function(column, field) {
        var $img = jQuery(field).find('img');
        if($img.length) {
            if ($img.attr('id') == 'asc') this.sort_order = 'desc';
            else this.sort_order = 'asc';
        }
        else this.sort_order = 'asc';

        this.sort_key = column;
        if(this.ids.length) {
            this.reload();
        }
    },

    group_by: function(id, record, no_leaf, group) {
        var $group_record = jQuery('[records="' + record + '"]');
        var group_by_context = $group_record.attr('grp_context');
        var domain = $group_record.attr('grp_domain');
        var total_groups = jQuery('#' + this.name).attr('groups');
        var $header = jQuery('table[id="'+this.name+'_grid'+'"] tr.grid-header');
        var check_order = eval(total_groups);
        var sort_order;
        var sort_key;
        for(var i in check_order) {
            var $img = $header.find('th[id="'+'grid-data-column/'+check_order[i]+'"] img');
            if($img.length) {
                sort_order = $img.attr('id');
                sort_key = check_order[i];
            }
        }
        if (group_by_context == '[]') {
            jQuery('#' + record + '[parent_grp_id="' + id + '"]').toggle();
        } else {
            if (jQuery(group).hasClass('group-expand')) {
                jQuery.ajax({
                    url: '/openerp/listgrid/multiple_groupby',
                    type: 'POST',
                    data: { 'model': this.model, 'name': this.name,
                            'grp_domain': domain, 'group_by': group_by_context,
                            'view_id': this.view_id,
                            'view_type': this.view_type,
                            'parent_group': record,
                            'group_level': jQuery(group).index() + 1,
                            'groups': total_groups,
                            'no_leaf': no_leaf,
                            'sort_order': sort_order,
                            'sort_key': sort_key},
                    dataType: 'html',
                    success: function(xmlHttp) {
                        $group_record.after(xmlHttp);
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

    groupbyDrag: function(drag, drop, view) {
        var _list_view = new ListView(view);
        var domain;
        var children;

        var drop_record = drop.attr('record');
        var drag_record = drag.attr('record');
        if(drop_record) {
            var dropGroup = drop.attr('id').split('grid-row ')[1];
            domain = jQuery('tr.grid-row-group[records="'+dropGroup+'"]').attr('grp_domain');
        }
        else {
            domain = drop.attr('grp_domain');
        }

        var ch_records = drag.attr('ch_records');
        if(ch_records) {
            children = ch_records;
        }
        else {
            if(drag.attr('id') == drop.attr('id')) {
                var dragGroup = drag.attr('id').split('grid-row ')[1];
                children = jQuery('tr.grid-row-group[records="'+dragGroup+'"]').attr('ch_records');
            }
            else {
                children = drag_record;
            }
        }

        if((drag_record && drop_record) && (drag.attr('id')) == drop.attr('id')) {
            _list_view.dragRow(drag, drop, view);
        }
        else {
            jQuery.ajax({
                url: '/openerp/listgrid/groupbyDrag',
                type: 'POST',
                data: {'model': _list_view.model, 'children': children, 'domain': domain},
                dataType: 'json',
                success: function () {
                    _list_view.reload();
                }
            });
        }
    },

    dragRow: function(drag, drop, view) {
        var _list_view = new ListView(view);
        jQuery.ajax({
            url: '/openerp/listgrid/dragRow',
            type: 'POST',
            data: {'_terp_model': _list_view.model,
                   '_terp_ids': _list_view.ids,
                   '_terp_id': jQuery(drag).attr('record'),
                   '_terp_swap_id': jQuery(drop).attr('record')
                  },
            dataType: 'json',
            success: function() {
                _list_view.reload();
            }
        });
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
    },

    clear: function() {
        group_by = new Array();
        filter_context = [];
        this.reload(-1, null, this.default_get_ctx, true)
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

        var editors = jQuery('#' + this.name + ' .listfields').get();

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
                ids: openobject.dom.get(prefix + '_terp_ids').value,
                model: openobject.dom.get(prefix + '_terp_model').value,
                view_ids: openobject.dom.get(prefix + '_terp_view_ids').value,
                domain: openobject.dom.get(prefix + '_terp_domain').value,
                context: openobject.dom.get(prefix + '_terp_context').value,
                limit: openobject.dom.get(prefix + '_terp_limit').value,
                offset: openobject.dom.get(prefix + '_terp_offset').value,
                count: openobject.dom.get(prefix + '_terp_count').value}));
        }

        name = name.split('.').pop();

        var params = {
            _terp_model : this.model,
            _terp_id : id,
            _terp_button_name : name,
            _terp_button_type : btype
        };

        var req = eval_domain_context_request({source: this.name, context : context || '{}',active_id: id, active_ids: openobject.dom.get(prefix + '_terp_ids').value});
        req.addCallback(function(res) {
            params['_terp_context'] = res.context;
            var req = openobject.http.postJSON('/openerp/listgrid/button_action', params);
            req.addCallback(function(obj) {
                if (obj.error) {
                    return error_display(obj.error);
                }

                if (obj.result && obj.result.url) {
                    window.open(obj.result.url);
                }

                if(obj.res) {
                    var popup_win = openobject.tools.openWindow("");
                    if(window.browser.isGecko) {
                        popup_win.document.write(obj.res);
                        popup_win.document.close();
                    }
                    else {
                        popup_win.document.close();
                        popup_win.document.write(obj.res);
                    }
                    return false;
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

    save: function(id, prev_id) {

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

        var $current_record = jQuery('table[id="'+this.name+'_grid'+'"]').find('tr.grid-row[record="'+id+'"]');
        req.addCallback(function(obj) {
            if (obj.error) {
                error_display(obj.error);

                var $focus_field;
                for (var k in data) {
                    var $req_field = $current_record.find('td [id="'+'_terp_listfields/'+k+'"].requiredfield');

                    if(!$req_field.length)
                        continue;
                    if($req_field.attr('kind') == 'many2one') {
                        $req_field = $current_record.find('td [id="'+'_terp_listfields/'+k+'_text'+'"]');
                    }

                    var req_value = $req_field.val();
                    if(req_value == '') {
                        $req_field.addClass('errorfield');
                        if(!$focus_field) {
                            $focus_field = $req_field;
                        }
                    } else if($req_field.hasClass('errorfield')) {
                        $req_field.removeClass('errorfield');
                    }
                }
                if($focus_field) {
                    $focus_field.focus();
                }
            } else {
                openobject.dom.get(prefix + '_terp_id').value = obj.id;
                openobject.dom.get(prefix + '_terp_ids').value = obj.ids;

                if(prev_id != undefined) {
                    self.reload(prev_id , prefix ? 1 : 0);
                } else {
                    self.reload(id > 0 ? null : -1, prefix ? 1 : 0);
                }
            }
        });
    },

    remove: function(ids) {

        var self = this;
        var args = getFormParams('_terp_concurrency_info');

        if (!ids) {
            ids = this.getSelectedRecords();
            if (ids.length > 0) {
                ids = '[' + ids.join(', ') + ']';
            }
        }

        if (ids.length == 0) {
            return error_display(_('You must select at least one record.'));
        }
        else if (!confirm(_('Do you really want to delete selected record(s) ?'))) {
            return false;
        }

        var $terp_ids;
        var $terp_count;

        if(this.name == '_terp_list') {
            $terp_ids = jQuery('#_terp_ids')
            $terp_count = jQuery('#_terp_count')
        }
        else {
            $terp_ids = jQuery('[id="'+this.name+'/_terp_ids'+'"]')
            $terp_count =  jQuery('[id="'+this.name+'/_terp_count'+'"]')
        }

        args['_terp_ids'] = $terp_ids.val()
        args['_terp_model'] = this.model;
        args['_terp_id'] = ids;
        var req = openobject.http.postJSON('/openerp/listgrid/remove', args);

        req.addCallback(function(obj) {
            if (obj.error) {
                error_display(obj.error);
            }
            else {
                if(obj.ids) {
                    $terp_ids.val(obj.ids)
                    $terp_count.val(obj.count)
                }
                self.reload();
                if(obj.res_ids) {
                    jQuery('div#corner ul.tools li a.messages small').text(obj.ids.length)
                }
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

    reload: function(edit_inline, concurrency_info, default_get_ctx, clear) {
        if (openobject.http.AJAX_COUNT > 0) {
            return callLater(1, bind(this.reload, this), edit_inline, concurrency_info);
        }

        var self = this;

        var current_id = edit_inline ? (parseInt(edit_inline) || 0) : edit_inline;

        var args = jQuery.extend(this.makeArgs(), {
            _terp_source: this.name,
            _terp_edit_inline: edit_inline,
            _terp_source_default_get: default_get_ctx,
            _terp_concurrency_info: concurrency_info,
            _terp_editable: openobject.dom.get('_terp_editable').value,
            _terp_group_by_ctx: openobject.dom.get('_terp_group_by_ctx').value
        });

        if (this.name == '_terp_list') {
            jQuery.extend(args, {
                _terp_search_domain: openobject.dom.get('_terp_search_domain').value,
                _terp_search_data: openobject.dom.get('_terp_search_data').value,
                _terp_filter_domain: openobject.dom.get('_terp_filter_domain').value
            });
        }

        if(this.sort_key) {
            jQuery.extend(args, {
                _terp_sort_key: this.sort_key,
                _terp_sort_order: this.sort_order
            });
        }

        if(clear) {
            args['_terp_clear'] = true;
        }

        jQuery('[id="'+self.name+'"] .loading-list').show();
        jQuery.ajax({
            url: '/openerp/listgrid/get',
            data: args,
            dataType: 'jsonp',
            type: 'POST',
            error: loadingError,
            success: function(obj) {
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

                self.current_record = edit_inline;
                if(obj.logs) {
                    jQuery('div#server_logs').replaceWith(obj.logs)
                }

                if(clear) {
                    jQuery('#view_form').replaceWith(obj.view);
                    initialize_search();
                }

                else {
                    var __listview = openobject.dom.get(self.name).__listview;
                    jQuery('[id="'+self.name+'"]').parent().replaceWith(obj.view);
                }

                var newlist = jQuery('[id="'+self.name+'"]');

                var editors = self.adjustEditors(newlist.get(0));
                if (editors.length > 0) {
                    self.bindKeyEventsToEditors(editors);
                }

                openobject.dom.get(self.name).__listview = __listview;

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
                var first = jQuery('input.listfields')[0] || null;
                if (first) {
                    first.focus();
                    first.select();
                }

                // call on_change for default values
                if (editors.length && edit_inline == -1) {
                    jQuery(editors).each(function () {
                        var $this = jQuery(this);
                        if ($this.val() && $this.attr('callback')) {
                            MochiKit.Signal.signal(this, 'onchange');
                        }
                    });
                }

                MochiKit.Signal.signal(__listview, 'onreload');

                if(self.sort_key != null) {
                    if(self.name != '_terp_list') {
                        var th = jQuery('th[id= grid-data-column/' + self.name + '/' + self.sort_key + ']').get();
                    }
                    else {
                        var th = jQuery('th[id= grid-data-column/' + self.sort_key + ']').get();
                    }

                    var detail = jQuery(th).html();
                    if(self.sort_order == 'asc') {
                        jQuery(th).html(detail + '&nbsp; <img src="/openerp/static/images/listgrid/arrow_down.gif" id="asc" style="vertical-align: middle;"/>');
                    } else {
                        jQuery(th).html(detail + '&nbsp; <img src="/openerp/static/images/listgrid/arrow_up.gif" id="desc" style="vertical-align: middle;"/>');
                    }
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

        openobject.tools.openWindow(openobject.http.getURL('/openerp/impex/exp', {
            _terp_model: this.model,
            _terp_source: this.name,
            _terp_context: $('_terp_context').value,
            _terp_search_domain: openobject.dom.get('_terp_search_domain').value,
            _terp_ids: ids,
            _terp_view_ids : this.view_ids,
            _terp_view_mode : this.view_mode}),{width: 700, height: 610});
    },

    importData: function() {
        openobject.tools.openWindow(openobject.http.getURL('/openerp/impex/imp', {
            _terp_model: this.model,
            _terp_context: $('_terp_context').value,
            _terp_source: this.name,
            _terp_view_ids : this.view_ids,
            _terp_view_mode : this.view_mode}),{width: 700, height: 500});
    }
});

function validateList(_list) {
    var $list = jQuery('[id="' + _list + '"]').removeAttr('current_id');
    var $check = jQuery('table.grid[id="'+_list+'_grid'+'"] tr.grid-row[record] td.grid-cell:not(.selector)').find('input, select');
    $check.change(function() {
        $list.attr(
            'current_id',
            parseInt(jQuery(this).closest('tr.grid-row').attr('record'), 10) || -1);
    });
}

function listgridValidation(_list, o2m, record_id) {
    o2m = parseInt(o2m, 0);
    var current_id = jQuery('[id="' + _list + '"]').attr('current_id');
    // not(null | undefined)
    if(current_id != null) {
        if(confirm('The record has been modified \n Do you want to save it ?')) {
            new ListView(_list).save(current_id, record_id);
        }
    } else{
        if(o2m) {
            var detail = jQuery('table.one2many[id$="' + _list + '"]').attr('detail');
            if(record_id == undefined || record_id == -1) {
                new One2Many(_list, detail).create();
            } else {
                new ListView(_list).edit(record_id);
            }
        } else if(record_id == -1) {
            new ListView(_list).create();
        } else {
            new ListView(_list).edit(record_id);
        }
    }
}
