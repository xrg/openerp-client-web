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

<%def name="sidebox_attach_item(item, model)">
    <li>
        <a href="${py.url(['/attachment/save_as', item[1]], record=item[0])}">${item[1]}</a>
    </li>
</%def>

<%def name="make_sidebox(title, model, items, item_cb=None, submenu=0)">

<h4 class="a">${title}</h4>
<ul class="clean-a">
	% for item in items:
        % if item:
            % if item_cb:
                ${item_cb(item, model)}
            % else:
                ${sidebox_action_item(item, model, submenu)}
            % endif
        % endif
    % endfor
</ul>
</%def>

% if reports or actions or relates or attachments:
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
            
            % if attachments:
                ${make_sidebox(_("ATTACHMENTS"), model, attachments, sidebox_attach_item)}
            % endif
            
            % if sub_menu:
                ${make_sidebox(_("SUBMENU"), model, sub_menu, submenu=1)}
            % endif
        </td>

		<td id="sidebar_hide" style="padding : 0 0 0 14px; border-color: #EAE7E7;" valign="top">
			<p class="toggle-a"><a id="toggle-click" href="javascript: void(0)" onclick="toggle_sidebar();">Toggle</a></p>
        </td>
    </tr>
</table>
% endif

