<table width="100%" cellpadding="0" cellspacing="0" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td width="100%">
            <input type="hidden" name='${name}' value="${value}"/>
            <input style="width: 100%" type="text" id ='${name}' value="${text}" class="${field_class}" onchange="if (this.value == '') document.getElementsByName('${name}')[0].value='';"/>
            <br py:if="error"/><span class="fielderror" py:if="error" py:content="error"/>
        </td>
        <td>
            <div class="spacer" />
        </td>
        <td>
            <button type="button" onclick="wopen(getURL('/many2one/new', {model: '${relation}', m2o: '${name}'}), 'search', 800, 600)">Select</button>
        </td>
    </tr>
</table>
