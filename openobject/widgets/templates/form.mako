<form ${py.attrs(attrs)} class="${css_class}">
    % if hidden_fields:
    <div>
        % for child in hidden_fields:
        ${display_member(child)}
        % endfor
    </div>
    % endif
    <table class="form-container">
        % for child in fields:
        <%
            error = error_for(child)
            label = label_for(child)
            help = help_for(child)
        %>
        <tr>
            <td class="label">
                % if help:
                    <label id="${child.name}.label" for="${child.name}" class="fieldlabel help" title="${help}">${label}</label>
                    <span class="help" title="${help}">?</span>
                % else:
                    <label id="${child.name}.label" for="${child.name}" class="fieldlabel">${label}</label>
                % endif
            </td>
            <td class="fieldcol">
                ${display_member(child)}
                % if error:
                <span class="fielderror">${error}</span>
                % endif
            </td>
        </tr>
        % endfor
        <tr>
            <td>&nbsp;</td>
            <td align="right" style="padding: 0px 5px 5px 0px;"><button type="submit" class="static_boxes">${submit_text}</button></td>
        </tr>
    </table>
</form>
