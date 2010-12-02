<table width="100%" class="vpaned">
    % for child in children:
    <tr>
        <td style="padding: 0 3px 0 0;" valign="top">
            ${display_member(child)}
        </td>
    </tr>
    % endfor
</table>
