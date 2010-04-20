<div style="display: none;">
    % for w in hiddens:
        ${display_member(w)}
    % endfor
</div>
<table width="100%" border="0" class='fields'>
    % for row in table:
    <tr>
        % for attrs, widget  in row:
        <td ${py.attrs(attrs)}>
            % if isinstance(widget, basestring):
                % if attrs.get('title'):
                <sup style="color: darkgreen;">?</sup>
                % endif
                ${(widget or '') and widget + ':'}
            % endif
            % if not isinstance(widget, basestring) and widget.visible:
            ${display_member(widget)}
            % endif
        </td>
        % endfor
    </tr>
    % endfor
</table>

