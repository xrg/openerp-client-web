<table width="100%" cellpadding="0" cellspacing="0" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td width="100%">
            <input type="hidden" name="${field_id}" id="${field_id}" value="${field_value}"/>
            <input type="checkbox" py:attrs="checked" onclick="$('${field_id}').value = this.checked ? 1 : '';"/>
        </td>
    </tr>
</table>
