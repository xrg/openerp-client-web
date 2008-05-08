<span xmlns:py="http://purl.org/kid/ns#" py:strip="">   
    <table py:if="editable" width="100%" cellpadding="0" cellspacing="0">
        <tr>
            <td width="25%">
                <input type="hidden" id='${name}' name='${name}' value="${value or None}" class="${field_class}" py:attrs='attrs' kind="${kind}" domain="${ustr(domain)}" context="${ustr(context)}" relation="${relation}" callback="${callback}"/>
                <select id="${name}_reference" name='${name}'>
                    <option value=""></option>
                    <option py:for="(k, v) in options" value="${k}" py:content="v" selected="1" py:if="relation == k">Selected</option>
                    <option py:for="(k, v) in options" value="${k}" py:content="v" py:if="relation != k">Not Selected</option>
                </select>
            </td>
            <td>
                <input type="text" id='${name}_text' value="${text}" class="${field_class}"  py:attrs='attrs' kind="${kind}" relation="${relation}"/>
                <span class="fielderror" py:if="error" py:content="error"/>
            </td>
            <td width="16" style="padding-left: 2px">
                <img id='${name}_select' width="16" height="16" alt="${_('Search')}" title="${_('Search / Open a resource')}" src="/static/images/stock/gtk-find.png" style="cursor: pointer;" class="imgSelect"/>
            </td>
        </tr>
    </table>

    <script type="text/javascript" py:if="editable">
        new ManyToOne('${name}');
    </script>    
    <span py:if="not editable" py:content="'(%s) %s'%(dict(options).get(ref), text)"/>
</span>
