<table border="0" cellpadding="0" cellspacing="0" class="one2many" width="100%" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td style="padding: 2px">
            <div class="toolbar">
                <table width="100%" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                        <td><strong>${screen.string}</strong></td>
                        <td align="right">
                            <button type="button" title="${new_attrs['help']}" py:if="screen.editable" onclick="newO2M('${name}', '${screen.view_mode[0]}', ${(screen.view_mode[0] == 'tree' or 0) and len(screen.widget.editors)})" py:content="new_attrs['text']">New</button>
                            <button type="button" title="Delete current record..." py:if="screen.editable" disabled="${tg.checker(screen.view_mode[0] == 'tree' or not screen.id)}" onclick="submit_form('delete', '${name}')">Delete</button>
                            <button type="button" title="Previous record..." disabled="${tg.checker(screen.view_mode[0] == 'tree')}" onclick="submit_form('previous', '${name}')">Prev</button>
                            <button type="button" title="Next record..." disabled="${tg.checker(screen.view_mode[0] == 'tree')}" onclick="submit_form('next', '${name}')">Next</button>
                            <button type="button" title="Switch view..." onclick="submit_form('switch', '${name}')">Switch</button>
                            <button type="button" title="Translate me." py:if="not screen.editable and screen.view_mode[0]=='form'" onclick="openWindow('${tg.url('/translator', _terp_model=screen.model, _terp_id=screen.id)}')">i18n</button>
                        </td>
                    </tr>
                </table>
            </div>
        </td>
    </tr>
    <tr>
        <td><div class="spacer"></div></td>
    </tr>
    <tr>
        <td py:if="screen">
            <input type="hidden" name="${name}/__id" value="${id}"/>
            ${screen.display()}
        </td>
    </tr>
    <tr>
        <td><div class="spacer"></div></td>
    </tr>
</table>
