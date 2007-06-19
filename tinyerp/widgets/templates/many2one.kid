<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <table py:if="editable" width="100%" cellpadding="0" cellspacing="0">
        <tr>
            <td>
                <input type="hidden" id='${name}' name='${name}' value="${value or None}" py:attrs='attrs' kind="${kind}" domain="${ustr(domain)}" context="${ustr(context)}" relation="${relation}" callback="${callback}"/>
                <input type="text" id='${name}_text' value="${text}" class="${field_class}"  py:attrs='attrs'/>
                <span class="fielderror" py:if="error" py:content="error"/>
            </td>
            <td width="1px"><div class="spacer"/></td>
            <td width="45px">
                <button type="button" id='${name}_create' title="Create a new resource" py:attrs="attrs">New</button>
            </td>
            <td width="1px"><div class="spacer"/></td>
    
            <td width="45px">
                <button type="button" id='${name}_select' title="Search / Open a resource" disabled="${tg.selector(attrs.get('disabled') and not value)}">Select</button>
            </td>
        </tr>
    </table>
    
    <script type="text/javascript">
        new ManyToOne('${name}');
    </script>
    
    <span py:if="not editable">
        <a href="${tg.query('/form/view', model=relation, id=value)}" py:content="text"/>
    </span>
</span>