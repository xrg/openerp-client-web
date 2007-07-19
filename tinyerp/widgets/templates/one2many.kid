<table border="0" cellpadding="0" cellspacing="0" class="one2many" width="100%" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td style="padding: 2px">
            <div class="toolbar">
                <table width="100%" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                        <td><strong>${screen.string}</strong></td>
                        <td align="right">
                            <button type="button" title="Create new record..." py:if="screen.editable and screen.view_mode[0]!='tree'" onclick="submit_form('save', '${button_name}')">New</button>
                            <button type="button" title="Create new record..." py:if="screen.editable and screen.view_mode[0]=='tree' and not screen.widget.editors" onclick="editO2M(null, '${name}')">New</button>
                            <button type="button" title="Create new record..." py:if="screen.editable and screen.view_mode[0]=='tree' and screen.widget.editors" onclick="new ListView('${name}').create()">New</button>                            
                            <button type="button" title="Delete current record..." py:if="screen.editable" disabled="${tg.checker(screen.view_mode[0] == 'tree' or not screen.id)}" onclick="submit_form('delete', '${button_name}')">Delete</button>
                            <button type="button" title="Previous record..." disabled="${tg.checker(screen.view_mode[0] == 'tree')}" onclick="submit_form('previous', '${button_name}')">Prev</button>
                            <button type="button" title="Next record..." disabled="${tg.checker(screen.view_mode[0] == 'tree')}" onclick="submit_form('next', '${button_name}')">Next</button>
                            <button type="button" title="Switch view..." onclick="submit_form('switch', '${button_name}')">Switch</button>
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
