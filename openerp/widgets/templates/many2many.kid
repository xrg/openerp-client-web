<table xmlns:py="http://purl.org/kid/ns#" border="0" width="100%" class="many2many">
    <tr py:if="editable">
        <td>
            <table width="100%" border="0" cellpadding="0" cellspacing="0">
                <tr>
                    <td>
                        <input type="hidden" py:if="inline" class="${field_class}" kind="${kind}" id='${name}_id' value="${str(screen.ids)}" py:attrs='attrs' relation="${relation}"/>
                        <input type="hidden" py:if="inline" kind="${kind}" name="${name}" id="${name}" value="${str(screen.ids)}"/>
                        <input type="text" py:if="inline" class="${field_class}" value="(${len(screen.ids or [])})" readonly="0" id='${name}_set' kind="${kind}" py:attrs='attrs' style="width: 100%; text-align: center;"/>
                        <input type="text" py:if="not inline" class="${field_class}" id='${name}_set' kind="${kind}" py:attrs='attrs' style="width: 100%;"/>
                        <span class="fielderror" py:if="error" py:content="error"/>
                    </td>
                    <td width="4px"><div class="spacer"/></td>
                    <td width="32" style="padding-left: 2px;">
                        <button type="button" id='_${name}_button1' py:attrs='attrs' domain="${ustr(domain)}" context="${ustr(context)}" onclick="open_search_window('${relation}', getNodeAttribute(this, 'domain'), getNodeAttribute(this, 'context'), '${name}', 2, getElement('${name}_set').value);">
                            <img width="16" height="16" src="/static/images/stock/gtk-add.png"/>
                        </button>
                    </td>
                    <td py:if="not inline" width="4px"><div class="spacer"/></td>
                    <td py:if="not inline" width="32" style="padding-left: 2px;">
                        <button type="button" id='_${name}_button2' py:attrs='attrs' onclick="Many2Many('${name}').remove()">
                            <img src="/static/images/stock/gtk-remove.png" width="16" height="16"/>
                        </button>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    <tr py:if="not inline">
    	<td py:if="screen" id='${name}_container'>
            ${screen.display()}
            <!-- IMP: IE problem, $('some_name') returns field with name="some_id" instead of id="some_id" -->
            <input type="hidden" py:if="not inline" class="${field_class}" kind="${kind}" id='${name}_id' name="${name}" value="${str(screen.ids)}" py:attrs='attrs' relation="${relation}"/>
        </td>
    </tr>

    <script type="text/javascript" py:if="editable">
        new Many2Many('${name}');
    </script>
</table>
            
