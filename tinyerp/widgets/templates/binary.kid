<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
            <td  py:if="editable">
                <input type="file" class="${field_class}" py:attrs="attrs" id="${name}" name="${name}" py:if="editable"/>
            </td>
            <td py:if="text and editable">
                ( ${text} )
            </td>

            <td py:if="text is not None and editable" width="75px">
                <button type="button" onclick="save_binary_data('${name}')">Save As</button>
            </td>
            <td py:if="text is not None and editable" width="1px"><div class="spacer"/></td>
            <td py:if="text is not None and not readonly and editable" width="75px">
                <button type="button" onclick="submit_form('clear_binary_data?_terp_field=${name}')">Clear</button>
            </td>
            <span py:if="editable and error" class="fielderror" py:content="error"/>
            <td py:if="not editable">
                <span py:content="value or text"/>
                <td width="75px" py:if="value or text">
                    <button type="button" onclick="save_binary_data('${name}')">Save As</button>
                </td>
            </td>
         </tr>
     </table>
</span>
