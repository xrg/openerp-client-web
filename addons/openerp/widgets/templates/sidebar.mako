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
    % if view_type == 'form':
    <div class="sideheader-a">
        <h2>${_("Add Attachments")}</h2>
    </div>
    <div>
        <form id="attachment-box" action="/openerp/form/save_attachment" method="post"
              enctype="multipart/form-data">
            <div>
                <label for="file_name">${_("File Name")}:</label>
                <input id="file_name" type="text" maxlength="64" name="datas_fname" kind="char"
                       class="char" size="10"/>
            </div>
            <div>
                <label for="datas">${_("File")}:</label>
                <input type="file" id="datas" class="binary"
                       onchange="onChange(this); set_binary_filename(this, 'datas_fname');"
                       name="datas" kind="binary" size="5"/>
            </div>
            <button type="submit" id="FormSubmit" class="button-a" name="FormSubmit">${_('submit')}</button>
        </form>
    </div>
    <div class="sideheader-a">

        <h2>${_("Attachments")}</h2>
    </div>
    <ul id="attachments" class="attachments-a">
        % for item in attachments:
            <!-- don't forget to also change jquery template in form.js/createAttachment -->
            <li id="attachment_item_${item[0]}" data-id="${item[0]}">
                <a target="_self" href="${py.url('/openerp/attachment/save_as', record=item[0])}">
                    ${item[1]}
                </a>
                <span>|</span>
                <a href="#" class="close" title="${_('Delete')}">Close</a>
            </li>
        % endfor
    </ul>
    % endif
</div>

<div id="sidebar_hide">
    <a id="toggle-click" href="javascript: void(0)" onclick="toggle_sidebar();">Toggle</a>
</div>
<script type="text/javascript">
    jQuery(document).ready(function () {
        jQuery('#attachments li a.close').each(function () {
            jQuery(this).click(removeAttachment);
        });
        jQuery('#datas').validate({
            expression: "if (VAL) return true; else return false;"
        });
        jQuery('#attachment-box').submit(createAttachment);
    });
</script>

