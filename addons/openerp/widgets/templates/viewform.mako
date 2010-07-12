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
	<table border="0" cellpadding="0" cellspacing="0" width="100%" style="border: none;">
        % if search:
        <%
             if not (search.listof_domain or search.custom_filter_domain or search.groupby):
                 css_clear = 'inactive_clear'
             else:
                 css_clear = ''
        %>

        <tr>
            <td valign="top">${display_member(search)}</td>
        </tr>
        <tr>
            <td class="view_form_options" align="left">
                <div>
                    <button onclick="add_filter_row(); return false;">
                        <img src="/openerp/static/images/button-b-icons-add.gif" alt="Add custom filtering">
                    </button>
                </div>
                <div>
                    <button title="${_('Filter records.')}" onclick="search_filter(); return false;"
                            >${_("Filter")}</button>
                    <button title="${_('Clear all .')}" id="clear_all_filters" class="${css_clear}"
                            onclick="new ListView('_terp_list').clear(); return false;"
                            >${_("Clear")}</button>
                    <button title="${_('Save as Filters.')}" onclick="save_as_filter(); return false;"
                            >${_("Save as Filter")}</button>
                    <button title="${_('Manage Filters.')}" onclick="manage_filters(); return false;"
                            >${_("Manage Filter")}</button>
                    <select class="custom-filter" name="filter_list" id="filter_list"
                            onchange="search_filter(); return false;">
                        % for f in search.filters_list:
                        <option value="${f[0]}">${f[1]}</option>
                        % endfor
                    </select>
                </div>
            </td>
        </tr>
        % endif
        <tr>
            <td valign="top">${display_member(screen)}</td>
        </tr>
    </table>
% endif
</form>
