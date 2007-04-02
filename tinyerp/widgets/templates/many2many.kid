<table xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td width="100%">
            <input type="text" style="width: 100%"/>
        </td>
        <td><div class="spacer"></div></td>
        <td><button type="button" onclick="wopen('/find?model=${relation}', 'search', 800, 600);">Add</button></td>
        <td><div class="spacer"></div></td>
        <td><button type="button">Remove</button></td>
    </tr>
    <tr><td height="3px"></td></tr>
    <tr>
        <td colspan="5">
            ${list_view.display()}
        </td>
    </tr>
</table>
