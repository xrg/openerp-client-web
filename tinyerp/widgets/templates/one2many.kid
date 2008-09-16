<table border="0" cellpadding="0" id="_o2m_$name" cellspacing="0" class="one2many" width="100%" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td style="padding: 2px">
            <div class="toolbar">
                <table width="100%" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                        <td width="100%"><strong>${screen.string}</strong></td>
                        <td>
                            <button type="button" py:if="screen.editable and not readonly"  title="${new_attrs['help']}" onclick="new One2Many('${name}', ${(screen.view_type == 'tree' or 0) and len(screen.widget.editors)}).create()" style="padding: 2px">
                                <img py:if="parent_id" src="/static/images/stock/gtk-new.png" width="16" height="16"/>
                                <img py:if="not parent_id" src="/static/images/stock/gtk-save.png" width="16" height="16"/>
                            </button>
                            <button type="button" py:if="screen.editable and screen.view_type == 'tree'" onclick="new ListView('${name}').remove()" style="padding: 2px">
                                <img src="/static/images/stock/gtk-delete.png" width="16" height="16"/>
                            </button>
                            <button type="button" py:if="screen.editable and screen.view_type == 'form' and screen.id and not readonly" title="${_('Delete current record...')}" onclick="submit_form('delete', '${name}')" style="padding: 2px">
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
                            <button type="button" title="${_('Switch view...')}" onclick="switch_O2M('${switch_to}', '${name}')" style="padding: 2px">
                                <img src="/static/images/stock/gtk-justify-fill.png" width="16" height="16"/>
                            </button>
                        </td>
                        <td>
                            <img class="button" title="${_('Translate me.')}" src="/static/images/translate.png" width="16" height="16" py:if="not screen.editable and screen.view_type=='form'" onclick="openWindow('${tg.url('/translator', _terp_model=screen.model, _terp_id=screen.id)}')"/>
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
            <input type="hidden" name="${name}/_terp_default_get_ctx" id="${name}/_terp_default_get_ctx" value="${ustr(default_get_ctx)}"/>
            ${screen.display()}
        </td>
    </tr>
    <tr>
        <td><div class="spacer"></div></td>
    </tr>
</table>
