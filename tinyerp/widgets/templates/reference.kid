<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <table py:if="editable" width="100%" cellpadding="0" cellspacing="0">
        <tr>
            <td width="25%">
                <!-- IMP: maintain order of hidden + select (IE7 issue) -->
                <input type="hidden" kind="${kind}" id='${name}' name='${name}' value="${value or None}" py:attrs='attrs' callback="${callback}" onchange="${onchange}; getName(this, $('${name}_select').value);"/>
                <select id="${name}_select" name='${name}' onchange="$('${name}_text').value='';$('${name}').value='';">
                    <option value=""></option>
                    <option py:for="(k, v) in options" value="${k}" py:content="v" selected="1" py:if="ref == k">Selected</option>
                    <option py:for="(k, v) in options" value="${k}" py:content="v" py:if="ref != k">Not Selected</option>
                </select>
            </td>
            <td width="2px"><div class="spacer"/></td>
               <td>
                <input type="text" value='${text}'  id ='${name}_text' class="${field_class}"  py:attrs='attrs' onchange="if (!this.value){$('${name}').value=''; $('${name}').onchange();} else {getName('${name}', $('${name}_select').value);}"/>
                <span class="fielderror" py:if="error" py:content="error"/>
            </td>
            <td width="16" style="padding-left: 2px;">
                <img width="16" height="16" src="/static/images/find.gif" style="cursor: pointer;"
                    domain="${ustr(domain)}" context="${ustr(context)}"
                    onclick="if($('${name}_select').value) open_search_window($('${name}_select').value, getNodeAttribute(this, 'domain'), getNodeAttribute(this, 'context'), '${name}', 1);"/>
            </td>
        </tr>
    </table>
    <span py:if="not editable" py:content="'(%s) %s'%(dict(options).get(ref), text)"/>
</span>
