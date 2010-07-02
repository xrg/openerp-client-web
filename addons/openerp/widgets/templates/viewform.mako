<form method="post" id="${name}" name="${name}" action="${action}" enctype="multipart/form-data">

    <div>
        <input type="hidden" id="_terp_search_domain" name="_terp_search_domain" value="${search_domain}"/>
        <input type="hidden" id="_terp_filter_domain" name="_terp_filter_domain" value="${filter_domain}"/>
        <input type="hidden" id="_terp_search_data" name="_terp_search_data" value="${search_data}"/>

    % for field in hidden_fields:
        ${display_member(field)}
    % endfor
    </div>

% if screen:
	<table border="0" cellpadding="0" cellspacing="0" width="100%" style="border: none;">
        % if search:
        <tr>
            <td valign="top">${display_member(search)}</td>
        </tr>
        <tr>
            <td class="view_form_options" align="left">
            	<table style="border: none;">
            		<tr>
            			<td style="padding: 0;">
            				<div class="toolbar">
			                	<a class="button-a" title="${_('Filter records.')}" href="javascript: void(0)" onclick="search_filter()">${_("Filter")}</a>
                			</div>
            			</td>
            			<td style="padding: 0 2px 0 2px;">
           			         <a class="button-a" title="${_('Clear all .')}" href="javascript: void(0)">${_("Clear")}</a>
            			</td>
            			<td style="padding: 0 2px 0 2px;">
                             <a class="button-a" title="${_('Save as Filters.')}" href="javascript: void(0)" onclick="save_as_filter()">${_("Save as Filter")}</a>
                        </td>
                        <td style="padding: 0 2px 0 2px;">
                             <a class="button-a" title="${_('Manage Filters.')}" href="javascript: void(0)" onclick="manage_filters()">${_("Manage Filter")}</a>
                        </td>
                        <td class="custom-filter">
                             <ul>
                                <li style="padding-right: 3px;">
                                    <select name="filter_list" id="filter_list" onchange="search_filter();">
                                        % for f in search.filters_list:
                                        <option value="${f[0]}">${f[1]}</option>
                                        % endfor
                                    </select>
                                </li>
                                <li>
                                    <a class="button" href="javascript: void(0)" onclick="add_filter_row();">
                                        <span class="add">Add</span>
                                    </a>
                                </li>
                            </ul>
                        </td>
            		</tr>
            	</table>
                
            </td>
            
        </tr>
        % endif
        <tr>
            <td valign="top">${display_member(screen)}</td>
        </tr>
    </table>
% endif
</form>
