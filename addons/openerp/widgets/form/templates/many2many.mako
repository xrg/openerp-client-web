<table border="0" width="100%" class="many2many">
    % if editable:
    <tr>
        <td>
            <table width="100%" border="0" cellpadding="0" cellspacing="0">
                <tr>
                    <td width="80%">
                        % if inline:
                        <input type="hidden" class="${css_class}" kind="${kind}" id='${name}_id' value="${screen.ids}" ${py.attrs(attrs)} relation="${relation}"/>
                        <input type="hidden" kind="${kind}" name="${name}" id="${name}" value="${screen.ids}" relation="${relation}"/>
                        <input type="text" class="${css_class}" value="(${len(screen.ids or [])})" readonly="0" id='${name}_set' kind="${kind}" ${py.attrs(attrs)} style="width: 100%; text-align: center;"/>
                        % else:
                        <input type="text" class="${css_class}" id='${name}_set' kind="${kind}" ${py.attrs(attrs)} style="width: 100%;"/>
                        % endif
                        % if error:
                        <span class="fielderror">${error}</span>
                        % endif
                    </td>
                    <td>
                        <button type="button" title="${_('Add records...')}" id='_${name}_button1' ${py.attrs(attrs, domain=domain, context=ctx)} onclick="open_search_window('${relation}', getNodeAttribute(this, 'domain'), getNodeAttribute(this, 'context'), '${name}', 2, openobject.dom.get('${name}_set').value);">
                            add
                        </button>
                    </td>
                    % if not inline:
                    <td style="padding-left: 0px">
                        <button type="button" title="${_('Delete records...')}" id='_${name}_button2' ${py.attrs(attrs)} onclick="Many2Many('${name}').remove()" style="width: 60px;">
                            remove
                        </button>
                    </td>
                    % endif
                </tr>
            </table>
        </td>
    </tr>
    % endif
    % if not inline:
    <tr>
        % if screen:
    	<td id='${name}_container'>
            ${screen.display()}
            <!-- IMP: IE problem, openobject.dom.get('some_name') returns field with name="some_id" instead of id="some_id" -->
            <input type="hidden" class="${css_class}" kind="${kind}" id='${name}_id' name="${name}" value="${screen.ids}" ${py.attrs(attrs)} relation="${relation}"/>
        </td>
        % endif
    </tr>
    % endif

    % if editable:
    <script type="text/javascript">
        new Many2Many('${name}');
    </script>
    % endif
</table>

