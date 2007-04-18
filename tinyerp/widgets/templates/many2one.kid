<table width="100%" cellpadding="0" cellspacing="0" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td width="100%"> 
            <input type="hidden" id='${name}_domain' value="${str(domain)}"/>
            <input type="hidden" id='${name}_context' value="${str(context)}"/>
            <input type="hidden" id='${name}_onchange' value="${onchange}"/>
                       
            <input type="hidden" kind="${kind}" id='${name}' name='${name}' value="${value or None}" py:attrs='attrs' 
                onchange="on_change('${name}', $('${name}_onchange').value, '${model}', '${name}_text'); get_name('${name}', '${relation}')"/>
                
            <input style="width: 100%" type="text" id ='${name}_text' value="${text}" class="${field_class}"  py:attrs='attrs'
                onchange="if (!this.value){$('${name}').value=''; $('${name}').onchange();} else {get_name('${name}', '${relation}');}"/>
            <br py:if="error"/><span class="fielderror" py:if="error" py:content="error"/>
        </td>
        <td>
            <div class="spacer" />
        </td>
        <td>
            <button type="button" py:attrs="attrs" 
                onclick="wopen(getURL('/many2one/new', {model: '${relation}', m2o: '${name}', domain: $('${name}_domain').value, context: $('${name}_context').value}), 'search', 800, 600)">Select</button>
        </td>
    </tr>
</table>
