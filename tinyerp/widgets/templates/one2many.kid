<table border="0" cellpadding="0" cellspacing="0" style="margin: 5px 0; border-bottom: 1px solid #C3D9FF" width="100%" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td style="padding: 2px" align='right'>
            <div class="toolbar">
            <table width="100%" border="0" cellpadding="0" cellspacing="0">
                <tr>
                    <td width="100%"><strong>${string}</strong></td>
                    <td><button type="submit" title="Create new record...">New</button></td>
                    <td><button type="button" title="Delete current record...">Delete</button></td>
                    <td><button type="button" title="Previous record...">Prev</button></td>
                    <td><button type="button" title="Next record...">Next</button></td>
                    <td><button type="button" title="Switch view...">List</button></td>
                </tr>
            </table>
            </div>
        </td>
    </tr>
    <tr>
        <td py:if="form">
            <input type="hidden" name="${name}/__id" value="${id}" py:if="id"/>
            ${form.display()}
        </td>
    </tr>
</table>
