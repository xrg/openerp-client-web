<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <table py:if="editable" width="100%" cellpadding="0" cellspacing="0">
        <tr>
            <td>
                <input type="hidden" kind="${kind}" id='${name}' name='${name}' value="${value or None}" py:attrs='attrs' callback="${callback}" onchange="${onchange}; getName(this, '${relation}')"/>
                <input type="text" id ='${name}_text' value="${text}" class="${field_class}"  py:attrs='attrs' onchange="if (!this.value){$('${name}').value=''; $('${name}').onchange();} else {getName('${name}', '${relation}');}"/>
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
                <button type="button" disabled="${tg.selector(attrs.get('disabled') and not value)}"
                    domain="${ustr(domain)}" context="${ustr(context)}"
                    onclick="if($('${name}').value) openm2o('edit', '${relation}', '${name}'); else open_search_window('${relation}', getNodeAttribute(this, 'domain'), getNodeAttribute(this, 'context'), '${name}', 1);">
                    Select
                </button>                
            </td>
        </tr>
    </table>
    <span py:if="not editable">
        <a href="${tg.query('/form/view', model=relation, id=value)}" py:content="text"/>
    </span>    
</span>