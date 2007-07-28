<table border="0" cellpadding="0" cellspacing="0" class="one2many" width="100%" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td style="padding: 2px">
            <div class="toolbar">
                <table width="100%" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                        <td width="100%"><strong>${screen.string}</strong></td>
                        <td>
                            <button type="button" title="${new_attrs['help']}" py:if="screen.editable" onclick="newO2M('${name}', '${screen.view_type}', ${(screen.view_type == 'tree' or 0) and len(screen.widget.editors)})" py:content="new_attrs['text']">New</button>
                            <button type="button" title="Delete current record..." py:if="screen.editable" disabled="${tg.checker(screen.view_type == 'tree' or not screen.id)}" onclick="submit_form('delete', '${name}')">Delete</button>
                            <button type="button" title="Switch view..." onclick="submit_form('switch', '${name}')">Switch</button>
                        </td>
                        <td py:if="pager_info">
                            <img class="button" title="Previous record..." src="/static/images/stock/gtk-go-back.png" width="16" height="16" onclick="submit_form('previous', '${name}')"/>
                        </td>
                        <td py:if="pager_info" py:content="pager_info" style="padding: 0px 4px"/>
                        <td py:if="pager_info">                            
                            <img class="button" title="Next record..." src="/static/images/stock/gtk-go-forward.png" width="16" height="16" onclick="submit_form('next', '${name}')"/>
                        </td>
                        <td>                            
                            <img class="button" title="Translate me." src="/static/images/translate.gif" width="16" height="16" py:if="not screen.editable and screen.view_type=='form'" onclick="openWindow('${tg.url('/translator', _terp_model=screen.model, _terp_id=screen.id)}')"/>
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
