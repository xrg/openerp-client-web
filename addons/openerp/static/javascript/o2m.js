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

var One2Many = function(name, inline) {

    this.name = name;
    this.inline = inline > 0;

    this.model = openobject.dom.get(name + '/_terp_model').value;
    this.mode = openobject.dom.get(name + '/_terp_view_type').value;

    if (openobject.dom.get(name + '/_terp_default_get_ctx'))
        this.default_get_ctx = openobject.dom.get(name + '/_terp_default_get_ctx').value;

    var parent_prefix = name.indexOf('/') > -1 ? name.slice(0, name.lastIndexOf('/') + 1) : '';

    this.parent_model = openobject.dom.get(parent_prefix + '_terp_model').value;
    this.parent_id = openobject.dom.get(parent_prefix + '_terp_id').value;
    this.parent_context = openobject.dom.get(parent_prefix + '_terp_context').value;
    this.parent_view_id = openobject.dom.get(parent_prefix + '_terp_view_id').value;

    // hide new button when editors are visible
    if (this.mode == 'tree' && this.inline) {
        var self = this;
        this.btn_new = openobject.dom.get(this.name + '_btn_');
        MochiKit.Signal.connect(ListView(this.name), 'onreload', function(evt) {
            self.btn_new.style.display = ListView(self.name).$getEditors().length > 0 ? 'none' : '';
        });
    }
};

One2Many.prototype = {

	remove: function(id) {

	if (!confirm(_('Do you really want to delete record ?'))) {
            return false;
    }

	var req = openobject.http.postJSON('/openerp/openo2m/delete', {'model': this.model, 'id': id});

	req.addCallback(function(obj) {
            if (obj.error) {
                jQuery.fancybox(obj.error, {scrolling: 'no'});
            }
            else {
                window.location.reload();
			}
    	});
	},

    create: function() {

        if (!this.parent_id || this.parent_id == 'False' || this.mode == 'form') {
            return submit_form('save', this.name);
        }

        if (this.mode == 'tree' && this.inline) {

            if (this.default_get_ctx) {
                var self = this;
                var req = eval_domain_context_request({source: this.name, context: this.default_get_ctx});
                req.addCallback(function(res) {
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
        if (id!='False' && id==0) {
        	return error_display(_('To edit Record, please first save it.'));
        }
        var parents = [];
        // get the required view params to get proper view
        var params = {
            '_terp_view_params/_terp_model': openobject.dom.get('_terp_model').value,
            '_terp_view_params/_terp_id': openobject.dom.get('_terp_id').value,
            '_terp_view_params/_terp_ids': openobject.dom.get('_terp_ids').value,
            '_terp_view_params/_terp_view_ids': openobject.dom.get('_terp_view_ids').value,
            '_terp_view_params/_terp_view_mode': openobject.dom.get('_terp_view_mode').value,
            '_terp_view_params/_terp_context': openobject.dom.get('_terp_context').value || {},
            '_terp_view_params/_terp_view_type': 'form'
        };

        while (names.length) {
            parents.push(names.shift());
            var prefix = parents.join('/');

            params['_terp_view_params/' + prefix + '/_terp_model'] = openobject.dom.get(prefix + '/_terp_model').value;
            params['_terp_view_params/' + prefix + '/_terp_id'] = openobject.dom.get(prefix + '/_terp_id').value;
            params['_terp_view_params/' + prefix + '/_terp_ids'] = openobject.dom.get(prefix + '/_terp_ids').value;
            params['_terp_view_params/' + prefix + '/_terp_view_ids'] = openobject.dom.get(prefix + '/_terp_view_ids').value;
            params['_terp_view_params/' + prefix + '/_terp_view_mode'] = openobject.dom.get(prefix + '/_terp_view_mode').value;
            params['_terp_view_params/' + prefix + '/_terp_context'] = openobject.dom.get(prefix + '/_terp_context').value || {};
            params['_terp_view_params/' + prefix + '/_terp_view_type'] = 'form';
        }

        jQuery.extend(params, {
            _terp_parent_model: this.parent_model,
            _terp_parent_id: this.parent_id,
            _terp_parent_view_id: this.parent_view_id,
            _terp_o2m: this.name,
            _terp_o2m_model: this.model,
            _terp_editable: readonly ? 0 : 1
        });

        if(id != null) {
            params['_terp_o2m_id'] = id;
        }
        if (id && id != 'False' && !this.default_get_ctx) {
            jQuery.o2m(params);
            return;
        }

        eval_domain_context_request({
            source: this.name,
            context : this.default_get_ctx
        }).addCallback(function(res) {
            jQuery.o2m(jQuery.extend(params, {
                _terp_o2m_context: res.context,
                _terp_parent_context: this.parent_context
            }));
        });
    },

    setReadonly: function(readonly) {
        var btn=MochiKit.DOM.getElement(this.name+'_btn_');
        var grid=MochiKit.DOM.getElement(this.name+'_grid');
        var edit=MochiKit.DOM.getElement(this.name + '/_terp_editable');
        var rows = jQuery('table[id='+this.name+'_grid] tr.grid-row');
        if (readonly) {
            jQuery('table.one2many[id$="'+this.name+'"]').addClass('m2o_readonly');
            if(btn){btn.style.display='none';}
            MochiKit.Base.map(function (el) {el.style.display='none'},MochiKit.Selector.findChildElements(grid,['.selector']));
            edit.value= 0;
            if (rows && rows.length) {
                rows.each(function(index, row) {
                    jQuery(row).unbind('click');});
            }
        }
        else{
            if(btn){btn.style.display='';}
            MochiKit.Base.map(function (el) {el.style.display=''},MochiKit.Selector.findChildElements(grid,['.selector']));
            edit.value = 1;
            if (rows && rows.length) {
                rows.each(function(index, row) {
                    jQuery(row).bind('click');});
            }
        }
    }
};

(function ($) {
    /**
     * Frame counter, used to uniquify (monotonously increasing) frame id in
     * order to ensure we avoid collisions between o2m frames (in case we
     * have nested o2ms somehow), as we need to get a frame we can target
     * with a form submission.
     */
    var frame_counter = 0;

    function frame_data($this, data) {
        return $($this.attr('frameElement')).data(data);
    }

    /**
     * Opens an o2m dialog linked to the provided <code>$this</code> window,
     * with the selected options.
     *
     * @param $this the parent window of the opened dialog, contains the
     * input to fill with the selected o2m value if any
     * @param options A map of options to provide to the newly opened iframe
     * call.
     */
    function open($this, options) {
        var frame_identifier = 'test-frame' + frame_counter++;
        var $frame = $('<iframe>', {
            src: 'about:blank',
            // never sure whether the iframe is targetted by name or by id,
            // so let's just set both
            id: frame_identifier,
            name: frame_identifier,
            frameborder: 0
        }).data('source-window', $this[0])
          .data('list', options['_terp_o2m'])
          .appendTo(document.documentElement)
          .dialog({
              modal: true,
              width: 640,
              height: 480,
              close: function () {
                  jQuery(this).dialog('destroy').remove();
              }
          });
        var $form = jQuery('<form>', {
            method: 'POST',
            action: '/openerp/openo2m/edit',
            target: frame_identifier
        });
        jQuery.each(options, function (key, value) {
            $form.append(jQuery('<input>', {
                type: 'hidden',
                name: key,
                value: value
            }));
        });
        $form.submit();
        return $frame;
    }


    var fetched_attrs = ['id', 'name', 'value', 'kind', 'class', 'domain',
                         'context', 'relation'];

    
    function initialize($frame_window) {
        // Within initialize, <code>jQ</code> is the "toplevel" jQuery whereas
        // <code>$</code> is the jQuery from within the iframe
        var jQ = jQuery;
        var $ = $frame_window[0].jQuery;

        var $form = $('#view_form');

        var list_id = frame_data($frame_window, 'list');
        jQ('#view_form :input[name]:not(:button)').each(function () {
            if (this.name.indexOf(list_id) == 0) {
                return;
            }
            var $this = $(this);
            var attrs = {};
            $.each(fetched_attrs, function (index, attribute) {
                var attr = $this.attr(attribute);
                if(!attr) { return; }
                attrs[attribute] = attr;
            });
            $form.append($('<input>', $.extend(attrs, {
                type: 'hidden',
                disabled: 'disabled',
                value: $this.val()
            })));
        });

        var lc = parseInt($('#_terp_load_counter').val(), 10) || 0;
        if(lc) {
            $.o2m('refresh');
        }
    }

    /**
     * Refreshes the backing ListView to make the newly added items appear.
     *
     * @param $this the window of the dialog to close
     */
    function refresh($this) {
        setTimeout(function () {
            frame_data($this, 'source-window')
                .ListView(frame_data($this, 'list'))
                    .reload(null, 1);
        })
    }

    /**
     * Closes the o2m dialog it was called from (represented by
     * <code>$this</code>.
     *
     * @param $this the window of the dialog to close
     */
    function close($this) {
        $($this.attr('frameElement')).dialog('close');
        return null;
    }

    /**
     * Manage o2m dialogs for this scope
     * <ul>
     *  <li><p>Called with only options, opens a new o2m dialog linking to the
     *         current scope.</p></li>
     *  <li><p>Called with the <code>"init"</code> command, performs the
     *         initial setup for the o2m dialog within the opened iframe
     *  </p></li>
     *  <li><p>Called with the <code>"close"</code> command, closes the o2m
     *         dialog it was invoked from and focuses its parent scope.
     *  </p></li>
     *  <li><p>Called with the <code>"refresh"</code> command, reloads
     *         the backing ListView to make the new items in it appear.
     *  </p></li>
     * </ul>
     *
     * @returns the o2m container (iframe) if one was created
     */
    $.o2m = function () {
        // $this should be the holder for the window from which $.o2m was
        // originally called, even if $.o2m() was bubbled to the top of
        // the window stack.
        var $this;
        if(this == $) $this = $(window);
        else $this = $(this);
        if(window != window.top) {
            return window.top.jQuery.o2m.apply($this[0], arguments);
        }
        // We're at the top-level window, $this is the window from which the
        // original $.o2m call was performed, window being the current window
        // level.
        switch(arguments[0]) {
            case 'close':
                return close($this);
            case 'refresh':
                return refresh($this);
            case 'init':
                return initialize($this);
            default:
                return open($this, arguments[0]);
        }
    };
})(jQuery);
