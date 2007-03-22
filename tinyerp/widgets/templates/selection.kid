<table width="100%" cellpadding="0" cellspacing="0" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td width="100%">
            <select id="${field_id}" name="${field_id}" style = "width : 100%">
                <option py:for="(key, value) in options" value = "${key}" py:content="value" selected="1" py:if="field_value == key">Selected</option>
                <option py:for="(key, value) in options" value = "${key}" py:content="value" py:if="field_value != key">Not Selected</option>
            </select>
        </td>
    </tr>
</table>
