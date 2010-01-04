<table border="0" id="_o2m_${name}" width="100%" class="one2many">
    <tr>
        <td class="toolbar">
            <table width="100%" border="0" cellpadding="0" cellspacing="0">
                <tr>
                    <td width="100%"><strong>${screen.string}</strong></td>
                    <td>
                        % if screen.editable and not readonly:
                        <button type="button" id="${name}_btn_" title="${new_attrs['help']}" onclick="new One2Many('${name}', ${(screen.view_type == 'tree' or 0) and len(screen.widget.editors)}).create()" style="padding: 2px">
                            % if parent_id:
                            <img src="${cp.static('base', 'images/stock/gtk-new.png')}" width="16" height="16"/>
                            % endif
                            % if not parent_id:
                            <img src="${cp.static('base', 'images/stock/gtk-save.png')}" width="16" height="16"/>
                            % endif
                        </button>
                        % endif
                        % if pager_info:
                        <button type="button" title="${_('Previous record...')}" onclick="submit_form('previous', '${name}')" style="padding: 2px">
                            <img class="button" src="${cp.static('base', 'images/stock/gtk-go-back.png')}" width="16" height="16"/>
                        </button>
                        % endif
                    </td>
                    % if pager_info:
                    <td style="padding: 0px 4px"/>${pager_info}</td>
                    % endif
                    <td>
                        % if pager_info:
                        <button type="button" title="${_('Next record...')}" onclick="submit_form('next', '${name}')" style="padding: 2px">
                            <img src="${cp.static('base', 'images/stock/gtk-go-forward.png')}" width="16" height="16"/>
                        </button>
                        % endif
                        <button type="button" title="${_('Switch view...')}" onclick="switch_O2M('${switch_to}', '${name}')" style="padding: 2px">
                            <img src="${cp.static('base', 'images/stock/gtk-justify-fill.png')}" width="16" height="16"/>
                        </button>
                    </td>
                    <td>
                        % if not screen.editable and screen.view_type=='form':
                        <img class="button" title="${_('Translate me.')}" src="${cp.static('base', 'images/stock/stock_translate.png')}" width="16" height="16" onclick="openobject.tools.openWindow('${py.url('/translator', _terp_model=screen.model, _terp_id=screen.id)}')"/>
                        % endif
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        % if screen:
        <td>
            <input type="hidden" name="${name}/__id" id="${name}/__id" value="${id}"/>
            <input type="hidden" name="${name}/_terp_default_get_ctx" id="${name}/_terp_default_get_ctx" value="${default_get_ctx}"/>
            ${screen.display()}
        </td>
        % endif
    </tr>
</table>

