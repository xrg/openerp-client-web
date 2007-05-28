<span xmlns:py="http://purl.org/kid/ns#">
    <table py:if="editable" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td>
                <input type="text" kind="${kind}" id="${field_id}" class="${field_class}" name="${name}" value="${strdate}" py:attrs='attrs' callback="${callback}" onchange="${onchange}"/>
                <span class="fielderror" py:if="error" py:content="error"/>
            </td>
            <td width="2">
                <div class="spacer"/>
            </td>
            <td width="75px">
                <button type="button" id="${field_id}_trigger" py:attrs='attrs'>
                    Select
                </button>
            </td>
            <script type="text/javascript">
                Calendar.setup(
                {
                    inputField : "${field_id}",
                    ifFormat : "${format}",
                    button : "${field_id}_trigger",
                    showsTime: ${str(picker_shows_time).lower()}
                });
               </script>
        </tr>
    </table>
    <span py:if="not editable" py:content="strdate"/>
</span>