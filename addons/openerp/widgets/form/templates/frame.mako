<div style="display: none;">
    % for w in hiddens:
        ${display_member(w)}
    % endfor
</div>
<table border="0" class='fields'>
    % for row in table:
    <tr>
        % for attrs, widget  in row:
            <td title="${getattr(widget, 'help', '')}" valign="middle">
                % if widget.string and not widget.nolabel:
                    <label for="${widget.name}">
                        % if getattr(widget, 'help', None):
                            <sup style="color: #006400;">?</sup>
                        % endif
                        ${widget.string}
                    </label>
                % endif
                ${display_member(widget)}
            </td>
        % endfor
    </tr>
    % endfor
</table>

