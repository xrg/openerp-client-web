<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <table py:if="editable" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td>
                <input type="text" kind="${kind}" id="${field_id}" class="${field_class}" name="${name}" value="${strdate}" py:attrs='attrs' callback="${callback}" onchange="${onchange}"/>
                <span class="fielderror" py:if="error" py:content="error"/>
            </td>
            <td width="16">
                <img id="${field_id}_trigger" py:attrs='attrs' width="16" height="16" alt="Select" src="/static/images/calendar.gif" style="cursor: pointer;"/>                
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