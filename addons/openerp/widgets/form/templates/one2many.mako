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
	                        	<font onclick="openobject.dom.get('_${name}_link_span').style.display='none'; openobject.dom.get('_${name}_limit_span').style.display=''" style="cursor: pointer;">${pager_info}</font>
	                        	<a class="next" title="${_('Next record...')}" href="javascript: void(0)" onclick="submit_form('next', '${name}')"></a>
							</p>
							<p>
								<div id="_${name}_limit_span" style="display: none" align="right">
						    		<a href="javascript: void(0)" onclick="openobject.dom.get('_${name}_limit_span').style.display='none'; openobject.dom.get('_${name}_link_span').style.display=''">${_("Change Limit:")}</a>&nbsp;
						    		<select id='_${name}_limit' style="width: 80px;" onchange="openobject.dom.get('${name and (name != '_terp_list' or None) and name + '/'}_terp_limit').value=openobject.dom.get('_${name}_limit').value; pager_action('filter', '${name}')">
						                    <option value="20" ${py.selector(limit==20)}>20</option>
						                    <option value="40" ${py.selector(limit==40)}>40</option>
						                    <option value="60" ${py.selector(limit==60)}>60</option>
						                    <option value="80" ${py.selector(limit==80)}>80</option>
						                    <option value="100" ${py.selector(limit==100)}>100</option>
						               </select>
						    	</div>
							</p>
						</div>
					</td>
                	% endif
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
    <tr>
        % if screen:
        <td>
            <input type="hidden" name="${name}/__id" id="${name}/__id" value="${id}" ${py.disabled(screen.view_mode!="form")}/>
            <input type="hidden" name="${name}/_terp_default_get_ctx" id="${name}/_terp_default_get_ctx" value="${default_get_ctx}"/>
            ${screen.display()}
        </td>
        % endif
    </tr>
</table>
