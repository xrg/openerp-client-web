<table width="100%" class="hpaned">
    <tr>
        % for child in children:
        <td style="padding: 0 3px 0 0;" valign="top">
            ${display_member(child)}
        </td>
        % endfor
    </tr>
</table>
