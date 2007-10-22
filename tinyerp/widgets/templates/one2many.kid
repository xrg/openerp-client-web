<table border="0" cellpadding="0" cellspacing="0" class="one2many" width="100%" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td style="padding: 2px">
            <div class="toolbar">
                <table width="100%" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                        <td width="100%"><strong>${screen.string}</strong></td>
                        <td>
                            <button type="button" py:if="screen.editable"  title="${new_attrs['help']}" onclick="newO2M('${name}', '${screen.view_type}', ${(screen.view_type == 'tree' or 0) and len(screen.widget.editors)})" style="padding: 2px">
                                <img src="/static/images/stock/gtk-new.png" width="16" height="16"/>
                            </button>
                            <button type="button" py:if="screen.editable and screen.view_type == 'form' and screen.id" title="${_('Delete current record...')}" onclick="submit_form('delete', '${name}')" style="padding: 2px">
                                <img src="/static/images/stock/gtk-delete.png" width="16" height="16"/>                            
                            </button>                                
                            <button type="button" py:if="pager_info" title="${_('Previous record...')}" onclick="submit_form('previous', '${name}')" style="padding: 2px">
                                <img class="button" src="/static/images/stock/gtk-go-back.png" width="16" height="16"/>
                            </button>
                        </td>
                        <td py:if="pager_info" py:content="pager_info" style="padding: 0px 4px"/>
                        <td>
                            <button type="button" py:if="pager_info" title="${_('Next record...')}" onclick="submit_form('next', '${name}')" style="padding: 2px">
                                <img src="/static/images/stock/gtk-go-forward.png" width="16" height="16"/>
                            </button>
                            <button type="button" title="${_('Switch view...')}" onclick="switchView('${switch_to}', '${name}')" style="padding: 2px">
                                <img src="/static/images/stock/gtk-justify-fill.png" width="16" height="16"/>
                            </button>
                        </td>
                        <td>
                            <img class="button" title="${_('Translate me.')}" src="/static/images/translate.gif" width="16" height="16" py:if="not screen.editable and screen.view_type=='form'" onclick="openWindow('${tg.url('/translator', _terp_model=screen.model, _terp_id=screen.id)}')"/>
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
