<form method="post" id="${name}" name="${name}" action="${action}" enctype="multipart/form-data">
    <div>
        <input type="hidden" id="_terp_search_domain" name="_terp_search_domain" value="${search_domain}"/>
        <input type="hidden" id="_terp_filter_domain" name="_terp_filter_domain" value="${filter_domain}"/>
        <input type="hidden" id="_terp_search_data" name="_terp_search_data" value="${search_data}"/>
        <input type="hidden" id="_terp_notebook_tab" name="_terp_notebook_tab" value="${notebook_tab}"/>

    % for field in hidden_fields:
        ${display_member(field)}
    % endfor
    </div>

% if screen:
    <div id="server_logs"></div>
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
        % if search:
        <tr>
            <td valign="top">${display_member(search)}</td>
        </tr>
         % if screen.view_type == 'tree' and screen.widget:
            <tr>
                <td id="custom_columns">
                    <div id="customcolumns" class="group-expand" onclick="collapse_expand(this, '#custcols');">
                        <h2>${_("Hide Columns")}</h2>
                    </div>
                    % if getattr(screen.widget,'headers', []):
                        <table id="custcols" style="display:none;">
                            <tr>
                                % for i, (field, field_attrs) in enumerate(screen.widget.headers):
                                % if field != 'button':
                                    <td class="label">
                                        <input type="checkbox" checked id="display_column_${field}" onchange="search_filter();">
                                        <label for="display_column_${field}">
                                            ${field_attrs['string']}
                                        </label>
                                    </td>
                                % endif
                                % endfor
                            </tr>
                        </table>
                    % endif
                </td>
            </tr>
        % endif
        <tr>
            <td class="view_form_options" width="100%">
                <table width="100%">
                    <tr>
                        <td align="left">
                             <button title="${_('Filter records.')}" onclick="search_filter(); return false;">
                             ${_("Search")}</button>
                             <button title="${_('Clear all.')}" id="clear_all_filters"
                             onclick="new ListView('_terp_list').clear(); return false;"
                             >${_("Clear")}</button>
                             % if context_menu:
                                <button title="${_('Close')}" onclick="window.close()" href="javascript: void(0)">${_("Close")}</button>
                             % endif
                        </td>
                        <td align="right">
                            <button title="${_('Save Filter.')}"
                                onclick="save_filter(); return false;"
                                >${_("Save Filter")}</button>
                            <button title="${_('Manage Filter.')}"
                                onclick="manage_filters(); return false;"
                                >${_("Manage Filters")}</button>
                            <select name="filter_list" id="filter_list"
                                onchange="search_filter(); return false;">
                                % for f in search.filters_list:
                                    <option id="${f[3]}" value="${f[0]}" group_by="${f[2]}">${f[1]}</option>
                                % endfor
                            </select>
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
    % if screen.view_type == 'tree':
	    <script type="text/javascript">

	        jQuery(document).ready(function() {
	           var filter_box_index = jQuery('#${name} div.filter-a').closest('td.item:first').index();
	           var input_index = jQuery('#${name} input[type!="hidden"][type="text"]:first').closest('td.label').index();

	           if(filter_box_index >= 0 && (filter_box_index <  input_index)) {
                    jQuery('#${name} div.filter-a:first button').focus();
	           }
	            else {
                    jQuery('#${name} input[type!="hidden"][type="text"]:first').focus();
	            }
	        });
	    </script>
    % endif
% endif
</form>
