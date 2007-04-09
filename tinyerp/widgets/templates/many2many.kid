<table xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td width="100%">
            <input type="text" class="${field_class}" readonly="0" style="width: 100%"/>
            <br py:if="error"/><span class="fielderror" py:if="error" py:content="error"/>
        </td>
        <td><div class="spacer"></div></td>
        <td>
            <button type="button" onclick="alert('Not Implemented yet...');">Select</button>
        </td>
    </tr>
    <tr><td height="3px"></td></tr>
    <tr>
        <td colspan="3">
            ${list_view.display()}
        </td>
    </tr>
    <script language="javascript">
        new ListView('${list_view.name}').checkAll();
    </script>
</table>
