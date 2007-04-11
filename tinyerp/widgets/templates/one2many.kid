<table border="0" cellpadding="0" cellspacing="0" style="margin: 5px 0; border-bottom: 1px solid #C3D9FF" width="100%" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td style="padding: 2px" align='right'>
            <div class="toolbar">
            <table width="100%" border="0" cellpadding="0" cellspacing="0">
                <tr>
                    <td><strong>${screen.string}</strong></td>
                    <td align="right">
                        <button type="button" title="Create new record..." name="${button_name}" onclick="submit_form('save', this)">New</button>
                        <button type="button" title="Delete current record..." py:attrs="button_attrs" name="${button_name}" onclick="submit_form('delete', this)">Delete</button>
                        <button type="button" title="Previous record..." py:attrs="button_attrs" name="${button_name}" onclick="submit_form('prev', this)">Prev</button>
                        <button type="button" title="Next record..." py:attrs="button_attrs" name="${button_name}" onclick="submit_form('next', this)">Next</button>
                        <button type="button" title="Switch view..." name="${button_name}" onclick="submit_form('switch', this)">Switch</button>
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
            <input type="hidden" name="${name}/__id" value="${id}" py:if="id"/>
            ${screen.display()}
        </td>
    </tr>
    <tr>
        <td><div class="spacer"></div></td>
    </tr>
</table>
