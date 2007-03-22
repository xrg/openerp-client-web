<table width="100%" cellpadding="0" cellspacing="0" border="0" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td width="100%">
            <input style="width: 100%" type="text" id="${field_id}" class="${field_class}" name="${name}" value="${field_value}"/>
        </td>
        <td>
            <div class="spacer"></div>
        </td>
        <td>
              <input type="button" id="${field_id}_trigger" class="date_field_button" value="Select" />
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
