<table width="100%" cellpadding="0" cellspacing="0" xmlns:py="http://purl.org/kid/ns#">
    <tr>
    	<td width="30%">
		    <select id="${name}_select" name='${name}' style="width : 100%" onchange="$('${name}_text').value='';$('${name}').value='';">
        		<option value=""></option>
		        <option py:for="(k, v) in options" value="${k}" py:content="v" selected="1" py:if="ref == k">Selected</option>
        		<option py:for="(k, v) in options" value="${k}" py:content="v" py:if="ref != k">Not Selected</option>
		    </select>
		</td>
		<td>
            <div class="spacer" />
        </td>
   		<td width="70%">
            <input type="hidden" kind="${kind}" id='${name}' name='${name}' value="${value or None}" py:attrs='attrs' callback="${callback}" onchange="${onchange}; getName(this, $('${name}_select').value);"/>
            <input type="text" style="width: 100%" value='${text}'  id ='${name}_text' class="${field_class}"  py:attrs='attrs' onchange="if (!this.value){$('${name}').value=''; $('${name}').onchange();} else {getName('${name}', $('${name}_select').value);}"/>
            <span class="fielderror" py:if="error" py:content="error"/>
        </td>
        <td>
            <div class="spacer" />
        </td>
        <td>
            <button type="button" py:attrs="attrs"
                domain="${ustr(domain)}" context="${ustr(context)}"
                onclick="if($('${name}_select').value) wopen(getURL('/many2one/new', {model: $('${name}_select').value, m2o: '${name}', domain: getNodeAttribute(this, 'domain'), context: getNodeAttribute(this, 'context')}), 'search', 800, 600);">Select</button>
        </td>
    </tr>
</table>
