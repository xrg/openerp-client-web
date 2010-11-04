<%
    if view_type == 'form':
        pager_width = '35%'
        o2m_css_class = ''
    else:
        pager_width = '100%'
        o2m_css_class = 'o2m_box'
%>
<table border="0" id="_o2m_${name}" width="100%" class="one2many ${o2m_css_class}" detail="${(screen.view_type == 'tree' or 0) and len(screen.widget.editors)}">
    % if screen.editable and not readonly and view_type == 'form':
    <tr>
        <td class="o2m_cell">
            <table width="100%" class="gridview" style="border-bottom: 1px solid black;"cellpadding="0" cellspacing="0">
                <tr class="pagerbar">
	               	<td class="pagerbar-cell" align="left" width="${pager_width}">
	               		<div class="pagerbar-header">
	               			<strong>${screen.string}</strong><nobr>
	               			<a class="button-a" href="javascript: void(0)" title="${_('Create new record...')}" onclick="new One2Many('${name}', ${(screen.view_type == 'tree' or 0) and len(screen.widget.editors)}).create(); return false;">${_('New')}</a>
	               			%if id:
	               				<a class="button-a" href="javascript: void(0);" title="${_('Delete record...')}" onclick="new One2Many('${name}', ${(screen.view_type == 'tree' or 0) and len(screen.widget.editors)}).remove(${id}); return false;">${_("Delete")}</a>
	               			%endif
	               		</div>
	               	</td>
                    <td>
                        % if not screen.editable and screen.view_type=='form':
                        <img class="button" title="${_('Translate me.')}" alt="${_('Translate me.')}"
                             src="/openerp/static/images/stock/stock_translate.png" width="16" height="16"
                             onclick="openobject.tools.openWindow(openobject.http.getURL('/openerp/translator', {_terp_model: '${screen.model}', _terp_id: ${screen.id}, _terp_context: $('_terp_context').value}));"/>
                        % endif
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    % endif
    % if pager_info:
             <td width="65%" style="text-align: left" align="left">
                 <div class="pager">
                     <p id="_${name}_link_span" class="paging">
                         <a class="prev nav" title="${_('Previous record...')}" href="javascript: void(0)" onclick="submit_form('previous', '${name}');"></a>
                         <span>${pager_info}</span>
                         <a class="next nav" title="${_('Next record...')}" href="javascript: void(0)" onclick="submit_form('next', '${name}');"></a>
                     </p>
                 </div>
             </td>
	% endif
    <tr>
        % if screen:
        <td class="o2m_cell">
            <input type="hidden" name="${name}/__id" id="${name}/__id" value="${id}" ${py.disabled(screen.view_type!="form")}/>
            <input type="hidden" name="${name}/_terp_default_get_ctx" id="${name}/_terp_default_get_ctx" value="${default_get_ctx}"/>
            % if default_value:
            	<input type="hidden" name="_terp_default_o2m/${name}" id="_terp_default_o2m/${name}" value="${default_value}"/>
            %endif
            ${screen.display()}
        </td>
        % endif
    </tr>
    % if screen.editable and not readonly and view_type == 'tree':
        % if name == source:
            <script type="text/javascript">
                jQuery(document).ready(function() {
                    new One2Many('${name}', jQuery('table.one2many[id=_o2m_${name}]').attr('detail')).create();
                })
            </script>
        % endif
    % endif
</table>
