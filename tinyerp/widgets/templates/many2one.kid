<table width="100%" cellpadding="0" cellspacing="0" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td width="100%">
            <input type="hidden" name='${field_id}' value="${field_value}"/>
            <input style="width: 100%" type="text" id ='${field_id}' value="${text}"/>
        </td>
        <td>
            <div class="spacer" />
        </td>
        <td>
            <button type="button" onclick="wopen('/find?model=${relation}', 'search', 800, 600)">Select</button>
        </td>
    </tr>
</table>
