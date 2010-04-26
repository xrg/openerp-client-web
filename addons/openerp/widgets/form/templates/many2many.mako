<table border="0" width="100%" class="many2many">
    % if editable:
    <tr>
        <td>
            <table width="100%" border="0" cellpadding="0" cellspacing="0">
                <tr>
                    <td>
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
                    <td width="4px"><div class="spacer"></div></td>
                    <td width="32" style="padding-left: 2px;">
                        <button type="button" id='_${name}_button1' ${py.attrs(attrs, domain=domain, context=ctx)} onclick="open_search_window('${relation}', getNodeAttribute(this, 'domain'), getNodeAttribute(this, 'context'), '${name}', 2, openobject.dom.get('${name}_set').value);">
                            <img width="16" height="16" src="/openerp/static/images/stock/gtk-add.png"/>
                        </button>
                    </td>
                    % if not inline:
                    <td width="4px"><div class="spacer"></div></td>
                    <td width="32" style="padding-left: 2px;">
                        <button type="button" id='_${name}_button2' ${py.attrs(attrs)} onclick="Many2Many('${name}').remove()">
                            <img src="/openerp/static/images/stock/gtk-remove.png" width="16" height="16"/>
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

