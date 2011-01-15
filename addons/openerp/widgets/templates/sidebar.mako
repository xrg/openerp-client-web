<%def name="sidebox_action_item(item, model, submenu, icon)">
    % if submenu != 1:
    	<li action_id="${item['id']}" relation="${model}" domain="${item.get('domain')}"
    	   context="${item.get('context')}" onclick="validate_action(this, do_action)">
            % if icon:
                <img src="${icon}" alt=""/>
            % endif
           <a href="javascript: void(0)" onclick="return false">${item['name']}</a>
        </li>
    % else:
        <li>
            % if icon:
                <img src="${icon}" alt=""/>
            % endif
            % if item['name']:
                <a href="#" onclick="submenu_action('${item['action_id']}', '${model}');">
                    ${item['name']}
                </a>
            % endif
        </li>
    % endif
</%def>

<%def name="make_sidebox(title, model, items, submenu=0, icon=None)">
<div class="sideheader-a"><h2>${title}</h2></div>
<ul class="clean-a">
	% for item in items:
        % if item:
        	${sidebox_action_item(item, model, submenu, icon)}
        % endif
    % endfor
</ul>
</%def>

<div id="sidebar">
    % if reports:
        ${make_sidebox(_("Reports"), model, reports, icon='/openerp/static/images/stock/gtk-print.png')}
    % endif

    % if actions:
        ${make_sidebox(_("Actions"), model, actions)}
    % endif

    % if relates:
        ${make_sidebox(_("Links"), model, relates)}
    % endif

    % if sub_menu:
        ${make_sidebox(_("Submenu"), model, sub_menu, submenu=1)}
    % endif
    % if view_type == 'form':
    <div class="attachments">
        <div class="sideheader-a">
            <h2>${_("Attachments")}</h2>
        </div>
        <a href="#" id="add-attachment" class="button-a attachment-button">${_("Add")}</a>
        <br style="clear: both"/>
        <ul id="attachments" class="attachments-a">
            % for attachment in attachments:
                <!-- don't forget to also change jquery template in form.js/createAttachment -->
                <li id="attachment_item_${attachment['id']}" data-id="${attachment['id']}">
                    <a class="attachment" target="_blank"
                       href="${attachment['url'] or py.url('/openerp/attachment/get', record=attachment['id'])}">
                        ${attachment['name']}
                    </a>
                    <span>|</span>
                    <a href="#" class="close" title="${_('Delete')}">${_("Close")}</a>
                </li>
            % endfor
        </ul>

        <form id="attachment-box" action="/openerp/attachment/save" method="post"
              enctype="multipart/form-data">
            <label for="sidebar_attachments_datas">${_("File")}:</label>
            <input type="file" id="sidebar_attachments_datas" class="binary"
                   name="datas" kind="binary" size="5"/>
        </form>
    </div>
    % endif
	
	% if rpc.session.uid == 1:
	    <div class="sideheader-a">
	        <h2>${_("Customize")}</h2>
	    </div>
	    <ul class="clean-a">
	        <li>
	            <a title="${_('Manage views of the current object')}"
	               onclick="openobject.tools.openWindow('/openerp/viewlist?model=${model}', {height: 400})"
	               href="javascript: void(0)">${_("Manage Views")}</a>
	        </li>
	        % if id:
	        <li>
	            <a title="${_('Edit workflow of the current object')}"
	               href="/view_diagram/workflow?model=${model}&amp;rec_id=${id}">${_("Edit Workflow")}</a>
	        </li>
	        % endif
	        <li>
	            <a title="${_('Customize current object or create a new object')}"
	               onclick="jQuery.frame_dialog({src:'/openerp/viewed/new_model/edit?model=${model}'}, null, { width: '80%', max_width: 1000, height: '90%' })"
	               href="javascript: void(0)">${_("Customize Object")}</a>
	        </li>
	    </ul>
	% endif

    <div class="sideheader-a">
        <h2>${_("Other Options")}</h2>
    </div>
    <ul class="clean-a">
        % if view_type == 'tree':
        <li>
            <a href="javascript: void(0)" onclick="new ListView('_terp_list').importData()">${_("Import")}</a>
        </li>
        <li>
            <a href="javascript: void(0)" onclick="new ListView('_terp_list').exportData()">${_("Export")}</a>
        </li>
        % elif view_type == 'form' and rpc.session.uid == 1:
        <li>
            <a xid="translate_fields" href="javascript: void(0)" data="${ctx}" relation="${model}" id="${id}" onclick="translate_fields(this)">${_('Translate')}</a>
        </li>
        % endif
        % if id:
        <li>
            <a href="${py.url('/openerp/viewlog', id=id, model=model)}" id="sidebar_view_log">${_('View Log')}</a>
        </li>
        % endif
    </ul>
</div>

<script type="text/javascript">
    jQuery(document).ready(function() {
    	setupAttachments();
    	jQuery('#sidebar_view_log').fancybox();
   	});
</script>
