<table xmlns:py="http://purl.org/kid/ns#" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr py:if="editable">
        <td>
            <table width="100%" border="0" cellpadding="0" cellspacing="0">
                <tr>
                    <td>
			            <input type="hidden" kind="${kind}" id='${list_view.name}_id' py:attrs='attrs' relation="${relation}" callback="${callback}"/>
			            <input type="hidden" py:if="inline" kind="${kind}" name="${list_view.name}" id="${list_view.name}" value="${str(list_view.ids)}"/>
			            <input type="text" py:if="inline" class="${field_class}" value="(${len(list_view.ids or [])})" readonly="0" id='${list_view.name}_set' py:attrs='attrs' style="width: 100%; text-align: center;"/>
			            <input type="text" py:if="not inline" class="${field_class}" readonly="0" id='${list_view.name}_set' py:attrs='attrs' style="width: 100%;"/>
			            <span class="fielderror" py:if="error" py:content="error"/>
                    </td>
			        <td width="2px"><div class="spacer"/></td>
			        <td width="24" style="padding-left: 2px;">
			            <button type="button" py:attrs='attrs' domain="${ustr(domain)}" context="${ustr(context)}" onclick="open_search_window('${relation}', getNodeAttribute(this, 'domain'), getNodeAttribute(this, 'context'), '${name}', 2);">
                            <img width="16" height="16" src="/static/images/find.gif"/>
			            </button>
			        </td>
                </tr>
            </table>
        </td>
    </tr>
    <tr py:if="editable and not inline"><td colspan="${(editable or None) and 3}" height="4px"></td></tr>
    <tr py:if="not inline">
        <td colspan="${(editable or None) and 3}" id="${list_view.name}_container">
            ${list_view.display()}
        </td>
    </tr>
    
    <script type="text/javascript">
        new Many2Many('${list_view.name}');
    </script>
</table>
