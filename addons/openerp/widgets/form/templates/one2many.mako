<table border="0" id="_o2m_${name}" width="100%" class="one2many" detail="${(screen.view_type == 'tree' or 0) and len(screen.widget.editors)}">
    <tr>
        <td>
            <table width="100%" class="gridview" style="border-bottom: 1px solid #C0C0C0;"cellpadding="0" cellspacing="0">
                <tr class="pagebar">
                	<td class="pagerbar-cell" align="right" width="25%">
                		<div class="pagerbar-header">
                			<strong>${screen.string}</strong>
                		</div>
                	</td>
                	
                    % if pager_info:
                    <td width="75%" style="text-align: left" align="left">
                        <div class="pager">
                            <p id="_${name}_link_span" class="paging">
                                <a class="prev" title="${_('Previous record...')}" href="javascript: void(0)" onclick="submit_form('previous', '${name}')"></a>
                                <font>${pager_info}</font>
                                <a class="next" title="${_('Next record...')}" href="javascript: void(0)" onclick="submit_form('next', '${name}')"></a>
                            </p>                            
                        </div>
                    </td>
                    % endif
                    <td>
                        % if not screen.editable and screen.view_type=='form':
                        <img class="button" title="${_('Translate me.')}" alt="${_('Translate me.')}" 
                             src="/openerp/static/images/stock/stock_translate.png" width="16" height="16"
                             onclick="openobject.tools.openWindow('${py.url('/openerp/translator', _terp_model=screen.model, _terp_id=screen.id)}')"/>
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
