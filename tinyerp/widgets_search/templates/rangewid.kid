<table border="0" cellpadding="0" cellspacing="0" width="100%" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td width="50%">
            ${from_field.display(value_for(from_field), **params_for(from_field))}
        </td>
        <td align="center" width="10px"> - </td>        
        <td width="50%">
            ${to_field.display(value_for(to_field), **params_for(to_field))}
        </td>
    </tr>
</table>
