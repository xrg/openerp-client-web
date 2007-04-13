<table width="100%" cellpadding="0" cellspacing="0" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td width="100%">
            <input type="hidden" id='${name}_domain' value="${domain}"/>
            <input type="hidden" id='${name}_context' value="${context}"/>

            <input type="hidden" name='${name}' value="${value or None}" py:attrs='attrs'/>
            <input style="width: 100%" type="text" id ='${name}' value="${text}" class="${field_class}" onchange="if (this.value == '') document.getElementsByName('${name}')[0].value='';" py:attrs='attrs'/>
            <br py:if="error"/><span class="fielderror" py:if="error" py:content="error"/>
        </td>
        <td>
            <div class="spacer" />
        </td>
        <td>
            <button type="button" onclick="wopen(getURL('/many2one/new', {model: '${relation}', m2o: '${name}', domain: $('${name}_domain').value, context: $('${name}_context').value}), 'search', 800, 600)" py:attrs="attrs">Select</button>
        </td>
    </tr>
</table>
