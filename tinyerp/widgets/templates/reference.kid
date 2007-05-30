<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <table py:if="editable" width="100%" cellpadding="0" cellspacing="0">
        <tr>
        	<td width="25%">
    		    <select id="${name}_select" name='${name}' onchange="$('${name}_text').value='';$('${name}').value='';">
            		<option value=""></option>
    		        <option py:for="(k, v) in options" value="${k}" py:content="v" selected="1" py:if="ref == k">Selected</option>
            		<option py:for="(k, v) in options" value="${k}" py:content="v" py:if="ref != k">Not Selected</option>
    		    </select>
    		</td>
    		<td width="2px"><div class="spacer"/></td>
       		<td width="65%">
                <input type="hidden" kind="${kind}" id='${name}' name='${name}' value="${value or None}" py:attrs='attrs' callback="${callback}" onchange="${onchange}; getName(this, $('${name}_select').value);"/>
                <input type="text" value='${text}'  id ='${name}_text' class="${field_class}"  py:attrs='attrs' onchange="if (!this.value){$('${name}').value=''; $('${name}').onchange();} else {getName('${name}', $('${name}_select').value);}"/>
                <span class="fielderror" py:if="error" py:content="error"/>
            </td>
            <td width="2px"><div class="spacer"/></td>
            <td width="75px">
                <button type="button" py:attrs="attrs"
                    domain="${ustr(domain)}" context="${ustr(context)}"
                    onclick="if($('${name}_select').value) open_search_window($('${name}_select').value, getNodeAttribute(this, 'domain'), getNodeAttribute(this, 'context'), '${name}', 1);">Select</button>

            </td>
        </tr>
    </table>
    <span py:if="not editable" py:content="'(%s) %s'%(dict(options).get(ref), text)"/>
</span>
