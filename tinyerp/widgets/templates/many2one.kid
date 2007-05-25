<table width="100%" cellpadding="0" cellspacing="0" xmlns:py="http://purl.org/kid/ns#">
    <tr >
        <td>
            <input type="hidden" kind="${kind}" id='${name}' name='${name}' value="${value or None}" py:attrs='attrs' callback="${callback}" onchange="${onchange}; getName(this, '${relation}')"/>
            <input type="text" id ='${name}_text' value="${text}" class="${field_class}"  py:attrs='attrs' onchange="$('${name}').onchange();if (!this.value){$('${name}').value=''; } else {getName('${name}', '${relation}');}"/>
            <span class="fielderror" py:if="error" py:content="error"/>
        </td>
        <td width="1px"><div class="spacer"/></td>
        <td width="45px">
            <button type="button" py:attrs="attrs"
                domain="${ustr(domain)}" context="${ustr(context)}"
                onclick="openm2o('new', '${relation}', '${name}');">
                New
            </button>
        </td>
        <td width="1px"><div class="spacer"/></td>

        <td width="45px">
            <button type="button" py:attrs="attrs"
                domain="${ustr(domain)}" context="${ustr(context)}"
                onclick="if($('${name}').value) openm2o('edit', '${relation}', '${name}'); else wopen(getURL('/many2one/new', {model: '${relation}', m2o: '${name}', domain: getNodeAttribute(this, 'domain'), context: getNodeAttribute(this, 'context')}), 'search', 800, 600);">
                Select
            </button>
        </td>
    </tr>
</table>
