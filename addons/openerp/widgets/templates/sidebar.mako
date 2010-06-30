<%def name="sidebox_action_item(item, model, submenu)">
    % if submenu != 1:
	    <li onclick="do_action(${item['id']}, '_terp_id', '${model}', this);">
	    	<a href="javascript: void(0)" onclick="return false">${item['name']}</a>
	    </li>
	% else:
		<%
			from openobject import icons
		%>
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

<h4 class="a">${title}</h4>
<ul class="clean-a">
	% for item in items:
        % if item:
        	${sidebox_action_item(item, model, submenu)}
        % endif
    % endfor
</ul>
</%def>

<table id="sidebar_pane" border="0" cellpadding="0" cellspacing="0">
    <tr>
        <td id="sidebar" style="display: none">
			<div class="sideheader-a">
				<h2>Secondary Options</h2>
			</div>
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
        </td>

		<td id="sidebar_hide" valign="top">
			<p class="toggle-a"><a id="toggle-click" href="javascript: void(0)" onclick="toggle_sidebar();">Toggle</a></p>
        </td>
    </tr>
    <tr>
        <td colspan='2' id="customise_menu" style="display: none;">
            <div class="sideheader-a">
                <h2>${_("Customise")}</h2>
            </div>
            <ul id="customise_menu_" class="clean-a">
                <li>
                    <a class="customise_menu_options" title="${_('Manage views of the current object')}" 
                    onclick="openobject.tools.openWindow('/openerp/viewlist?model=${model}', {height: 400})" 
                    href="javascript: void(0)">${_("Manage Views")}</a>
                </li>
                <li>
                    <a class="customise_menu_options" title="${_('Manage workflows of the current object')}" 
                    onclick="javascript: show_wkf()" 
                    href="javascript: void(0)">${_("Show Workflow")}</a>
                </li>
                <li>
                    <a class="customise_menu_options" title="${_('Customise current object or create a new object')}" 
                    onclick="openobject.tools.openWindow('/openerp/viewed/new_model/edit?model=${model}')" 
                    href="javascript: void(0)">${_("Customise Object")}</a>
                </li>
            </ul>
        </td>
    </tr>
    % if view_type == 'form':
    <tr>
        <td id="add_attachment" colspan='2' style="display: none;">
            <div class="sideheader-a">
                <h2>${_("Add Attachments")}</h2>
            </div>
            <div>
            <form id="attachment-box" action="/openerp/form/save_attachment" method="post" enctype="multipart/form-data">
                <table class="attachment_bar">
                    <tr>
                        <td>
                            <div>
                                ${_("File Name")}:
                            </div>
                            <div>
                                <input id="file_name" type="text" maxlength="64" name="datas_fname" kind="char" class="char" size="10"/>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div>
                                ${_("File")}:
                            </div>
                            <div>
                                <input type="file" id="datas" class="binary" onchange="onChange(this); set_binary_filename(this, 'datas_fname');" name="datas" kind="binary" size="5"/>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td align="center">
                            <a id="FormSubmit" class="button-a" align="center" href="javascript: void(0)">${_("submit")}</a>
                        </td>
                    </tr>
                </table>
            </form>
            </div>
        </td>
    </tr>
    <tr>
        <td id="attach_sidebar" colspan='2' style="display: none;">
            <div class="poof"></div>
            <div class="sideheader-a" id="sideheader-a">
                
                <h2>${_("Attachments")}</h2>
            </div>
            <ul class="attachments-a">
                % for item in attachments:
                    <li id="attachment_item_${item[0]}">
                        <a target="_self" href="${py.url(['/openerp/attachment/save_as', item[1]], record=item[0])}">
                            ${item[1]}
                        </a>
                        <span>|</span>
                        <a href="javascript: void(0);" class="close" title="${_('Delete')}" onclick="removeAttachment(event, 'attachment_item_${item[0]}', ${item[0]});">Close</a>
                    </li>
                % endfor
            </ul>
        </td>
    </tr>
    % endif
</table>
<script type="text/javascript">
    jQuery('#datas').validate({
        expression: "if (VAL) return true; else return false;"
    });
   
    jQuery("#file_name").validate({
        expression: "if (VAL) return true; else return false;"
        });
        
   jQuery('#FormSubmit').click(function() {
       jQuery('#attachment-box').submit()
       window.location.reload()
   });
</script>

