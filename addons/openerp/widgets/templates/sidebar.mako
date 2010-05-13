<%def name="sidebox_action_item(item, model, submenu)">
    % if submenu != 1:
	    <tr onclick="do_action(${item['id']}, '_terp_id', '${model}', this);">
	        <td>
	            <a href="javascript: void(0)" onclick="return false">${item['name']}</a>
	        </td>
	    </tr>
	% else:
		<%
			from openobject import icons
		%>
		<tr data="${item}">
	   		% if item['name']:
				<td>
					<a href="#" onclick="submenu_action('${item['action_id']}', '${model}');">
						${item['name']}
					</a>
				</td>
			% endif
		</tr>
	% endif
</%def>

<%def name="sidebox_attach_item(item, model)">
    <tr>
        <td>
            <a href="${py.url(['/openerp/attachment/save_as', item[1]], record=item[0])}">${item[1]}</a>
        </td>
    </tr>
</%def>

<%def name="make_sidebox(title, model, items, item_cb=None, submenu=0)">
<table border="0" cellpadding="0" cellspacing="0" width="100%" class="sidebox">
    <tr>
        <td class="sidebox-title">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td width="8" class="sidebox-title-l"></td>
                    <td class="sidebox-title-m">${title}</td>
                    <td width="35" valign="top" class="sidebox-title-r"></td>
                </tr>
            </table>
        </td>
    </tr>

    % for item in items:
        % if item:
            % if item_cb:
                ${item_cb(item, model)}
            % else:
                ${sidebox_action_item(item, model, submenu)}
            % endif
        % endif
    % endfor
</table>
</%def>

% if reports or actions or relates or attachments:
<table id="sidebar_pane" border="0" cellpadding="0" cellspacing="0">
    <tr>
        <td id="sidebar" style="display: none">
            % if reports:
                ${make_sidebox(_("REPORTS"), model, reports)}
            % endif
            
            % if actions:
                ${make_sidebox(_("ACTIONS"), model, actions)}
            % endif
            
            % if relates:
                ${make_sidebox(_("LINKS"), model, relates)}
            % endif
            
            % if attachments:
                ${make_sidebox(_("ATTACHMENTS"), model, attachments, sidebox_attach_item)}
            % endif
            
            % if sub_menu:
                ${make_sidebox(_("SUBMENU"), model, sub_menu, submenu=1)}
            % endif
        </td>

        <td id="sidebar_hide" valign="top">
           <img src="/openerp/static/images/sidebar_show.gif" alt="toggle sidebar"
           border="0" onclick="toggle_sidebar();" style="cursor: pointer;"/>
        </td>
    </tr>
</table>
% endif

