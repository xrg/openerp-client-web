<table xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td width="100%">
            <input type="hidden" id='${name}_domain' value="${domain}"/>
            <input type="hidden" id='${name}_context' value="${context}"/>
            
            <input type="hidden" name='${name}'/>
            <input type="text" class="${field_class}" readonly="0" style="width: 100%" id='${list_view.name}_set' onchange="new ListView('${list_view.name}').checkAll();" py:attrs='attrs' />
            <br py:if="error"/><span class="fielderror" py:if="error" py:content="error"/>
        </td>
        <td><div class="spacer"></div></td>
        <td>
            <button type="button" py:attrs='attrs' onclick="wopen(getURL('/many2many/new', {model: '${relation}', m2m: '${name}', domain: $('${name}_domain').value, context: $('${name}_context').value}), 'search', 800, 600);">Select</button>
        </td>
    </tr>
    <tr><td height="3px"></td></tr>
    <tr>
        <td colspan="3" id="${list_view.name}_container">
            ${list_view.display()}
        </td>
    </tr>
    <script language="javascript">
        new ListView('${list_view.name}').checkAll();
    </script>
</table>
