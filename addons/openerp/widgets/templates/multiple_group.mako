<%!
import itertools
background = '#DEDEDE'
%>
% for j, grp_row in enumerate(grp_records):
    <tr class="grid-row-group" parent="${parent_group}" grp_by_id="${grp_row['group_by_id']}"
        records="${grp_row['group_id']}" style="cursor: pointer;"
        ch_records="${map(lambda x: x['id'],grp_row['child_rec'])}" grp_domain="${grp_row['__domain']}"
        grp_context="${grp_row['__context']['group_by']}">
        % if editable:
            <td class="grid-cell" style="background-color: ${background};"></td>
        % endif
        % for i, (field, field_attrs) in enumerate(headers):
            % if field != 'button':
                <%
                if field_attrs.get('type') != 'progressbar' and i == group_level - 1:
                    if len(group_by_ctx) == 1 and group_by_no_leaf:
                        subgroup_expander = ''
                        subgroup_class = ''
                    else:
	                    subgroup_expander = "new ListView('%s').group_by('%s', '%s', '%s', this)" % (
	                        name, grp_row['group_by_id'], grp_row['group_id'], group_by_no_leaf)
	                    subgroup_class = 'group-expand'
                else:
                    subgroup_expander = ''
                    subgroup_class = ''
                %>
                <td class="grid-cell ${subgroup_class} ${field_attrs.get('type', 'char')}"
                    style="background-color: ${background};"
                    onclick="${subgroup_expander}">
                    <span>
                        % if field_attrs.get('type') == 'progressbar':
                            ${grouped[j][field].display()}
                        % elif i != group_level - 1:
                            % if grp_row.get(field):
                                % if field_attrs.get('type') == 'many2one':
                                    ${grp_row.get(field)[-1]}
                                % else:
                                    ${grp_row.get(field)}
                                % endif
                            % else:
                                &nbsp;
                            % endif
                        % endif
                    </span>
                </td>
            % else:
                <td class="grid-cell button" nowrap="nowrap" style="background-color: ${background};">
                    <span></span>
                </td>
            % endif
        % endfor
        % if editable:
            <td class="grid-cell selector" style="background-color: ${background};">
                <div style="width: 0px;"></div>
            </td>
        % endif
    </tr>
    % for ch in grp_row.get('child_rec'):
        <tr class="grid-row-group" id="grid-row ${grp_row.get('group_id')}" parent="${parent_group}"
            parent_grp_id="${grp_row.get('group_by_id')}" record="${ch.get('id')}"
            style="cursor: pointer; display:none;">
            % if editable:
                <td class="grid-cell">
                    <img src="/openerp/static/images/listgrid/edit_inline.gif" class="listImage" border="0"
                         title="${_('Edit')}" onclick="editRecord(${ch.get('id')}, '${source}')"/>
                </td>
            % endif
            % for i, (field, field_attrs) in enumerate(headers):
                % if field != 'button':
                    <td class="grid-cell ${field_attrs.get('type', 'char')}"
                        style="${(ch.get(field).color or None) and 'color: ' + ch.get(field).color};"
                        sortable_value="${ch.get(field).get_sortable_text()}">
                        <span>${ch[field].display()}</span>
                    </td>
                % else:
                    <td class="grid-cell button" nowrap="nowrap">
                        ${buttons[field_attrs-1].display(parent_grid=name, **buttons[field_attrs-1].params_from(ch))}
                    </td>
                % endif
            % endfor
            % if editable:
                <td class="grid-cell selector">
                    <img src="/openerp/static/images/listgrid/delete_inline.gif" class="listImage" border="0"
                         title="${_('Delete')}" onclick="new ListView('${name}').remove(${ch.get('id')})"/>
                </td>
            % endif
        </tr>
    % endfor
% endfor
