<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <table py:if="editable" width="100%" cellpadding="0" cellspacing="0">
        <tr>
            <td>
                <input type="hidden" id='${name}' name='${name}' value="${value or None}" class="${field_class}" py:attrs='attrs' kind="${kind}" domain="${ustr(domain)}" context="${ustr(context)}" relation="${relation}" callback="${callback}"/>
                <input type="text" id='${name}_text' value="${text}" class="${field_class}"  py:attrs='attrs' kind="${kind}" relation="${relation}"/>
                <span class="fielderror" py:if="error" py:content="error"/>
            </td>
            <td width="16" style="padding-left: 2px">
                <img id='${name}_select' width="16" height="16" alt="${_('Search')}" title="${_('Search / Open a resource')}" src="/static/images/stock/gtk-find.png" style="cursor: pointer;"/>
            </td>
            <td width="16" style="padding-left: 2px" py:if="'_terp_listfields' not in name">
                <img id='${name}_menu' class="context_menu_button" width="16" height="16" alt="${_('Context Menu')}" title="${_('Context Menu')}" src="/static/images/stock/gtk-go-down.png" style="cursor: pointer;" onclick="m2oContextMenu(this)"/>
            </td>            
        </tr>
    </table>
    
    <script type="text/javascript" py:if="editable">
        new ManyToOne('${name}');
    </script>
    
    <span py:if="not editable">
        <a href="${tg.query('/form/view', model=relation, id=value)}" py:content="text"/>
    </span>
</span>