<%def name="sidebox_action_item(item, model, submenu)">
    % if submenu != 1:
	    <li onclick="do_action(${item['id']}, '_terp_id', '${model}', this);">
	    	<a href="javascript: void(0)" onclick="return false">${item['name']}</a>
	    </li>
	% else:
		<li data="${item}">
	   		% if item['name']:
				<a href="#" onclick="submenu_action('${item['action_id']}', '${model}');">
					${item['name']}
				</a>
			% endif
		</li>
	% endif
</%def>

<%def name="make_sidebox(title, model, items, submenu=0)">
<div class="sideheader-a"><h2>${title}</h2></div>
<ul class="clean-a">
	% for item in items:
        % if item:
        	${sidebox_action_item(item, model, submenu)}
        % endif
    % endfor
</ul>
</%def>

<div id="sidebar">
    % if reports:
        ${make_sidebox(_("REPORTS"), model, reports)}
    % endif

    % if actions:
        ${make_sidebox(_("ACTIONS"), model, actions)}
    % endif

    % if relates:
        ${make_sidebox(_("LINKS"), model, relates)}
    % endif

    % if sub_menu:
        ${make_sidebox(_("SUBMENU"), model, sub_menu, submenu=1)}
    % endif
    % if view_type == 'form':
    <div class="sideheader-a">
        <a href="#" id="add-attachment" class="button-a">Add</a>

        <h2>${_("Attachments")}</h2>
    </div>
    <ul id="attachments" class="attachments-a">
        % for attachment in attachments:
            <!-- don't forget to also change jquery template in form.js/createAttachment -->
            <li id="attachment_item_${attachment['id']}" data-id="${attachment['id']}">
                <a class="attachment-file" rel="external"
                   href="${attachment['url'] or py.url('/openerp/attachment/get', record=attachment['id'])}">
                    ${attachment['name']}
                </a>
                <span>|</span>
                <a href="#" class="close" title="${_('Delete')}">Close</a>
            </li>
        % endfor
    </ul>

    <form id="attachment-box" action="/openerp/attachment/save" method="post"
          enctype="multipart/form-data">
        <label for="datas">${_("File")}:</label>
        <input type="file" id="datas" class="binary"
               onchange="onChange(this);"
               name="datas" kind="binary" size="5"/>
    </form>
    % endif

    <div class="sideheader-a">
        <h2>${_("Customise")}</h2>
    </div>
    <ul class="clean-a">
        <li>
            <a class="customise_menu_options" title="${_('Manage views of the current object')}"
               onclick="openobject.tools.openWindow('/openerp/viewlist?model=${model}', {height: 400})"
               href="javascript: void(0)">${_("Manage Views")}</a>
        </li>
        <li>
            <a class="customise_menu_options" title="${_('Manage workflows of the current object')}"
               onclick="show_wkf(); return false;"
               href="javascript: void(0)">${_("Show Workflow")}</a>
        </li>
        <li>
            <a class="customise_menu_options" title="${_('Customise current object or create a new object')}"
               onclick="openobject.tools.openWindow('/openerp/viewed/new_model/edit?model=${model}')"
               href="javascript: void(0)">${_("Customise Object")}</a>
        </li>
    </ul>
    
    <div class="sideheader-a">
        <h2>${_("Other Options")}</h2>
    </div>
    <ul class="clean-a">
        <li>
            <a href="javascript: void(0)" onclick="new ListView('_terp_list').importData()">${_("Import")}</a>
        </li>
        <li>
            <a href="javascript: void(0)" onclick="new ListView('_terp_list').exportData()">${_("Export")}</a>
        </li>
        % if view_type == 'form':
        <li>
            <a href="${py.url('/openerp/translator', _terp_model=model, _terp_id=id, _terp_context=ctx)}"
               target="_blank">${_('Translate')}</a>
        </li>
        % endif
        % if id:
        <li>
            <a href="${py.url('/openerp/viewlog', _terp_id=id, _terp_model=model)}" target="_blank"
               onclick="openobject.tools.openWindow(this.href, {width: 550, height: 340}); return false;"
                    >${_('View Log')}</a>
        </li>
        % endif
    </ul>
</div>
<script type="text/javascript">
    jQuery(document).ready(setupAttachments);
</script>

