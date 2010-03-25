<table id="${name}" class="gridview" width="100%" cellspacing="0" cellpadding="0">
    % if pageable:
    <tr class="pagerbar">
        <td colspan="2" class="pagerbar-cell" align="right">${pager.display()}</td>
    </tr>
    % endif
    
    <tr>
        <td colspan="2">
            <table id="${name}_grid" class="grid" width="100%" cellspacing="0" cellpadding="0">
                <thead>
                    <tr class="grid-header">
                        % if editable:
                        <th class="grid-cell selector"><div style="width: 0px;"></div></th>
                        % endif
                        % for (field, field_attrs) in headers:
                        <th id="grid-data-column/${(name != '_terp_list' or None) and (name + '/')}${field}" class="grid-cell ${field_attrs.get('type', 'char')}" kind="${field_attrs.get('type', 'char')}" style="cursor: pointer;" onclick="new ListView('${name}').sort_by_order('${field}')">${field_attrs['string']}</th>
                        % endfor
                        % if buttons:
                        <th class="grid-cell button"><div style="width: 0px;"></div></th>
                        % endif
                        % if editable:
                        <th class="grid-cell selector"><div style="width: 0px;"></div></th>
                        % endif
                    </tr>
                </thead>

                <tbody>
					% for grp_row in grp_records:
					<tr class="grid-row-group" style="cursor: pointer;" grp_domain="${grp_row['__domain']}">
                        % if editable:
                        <td class="grid-cell" style="background-color: #CCCCCC;">
                            <img id="img_${grp_row.get('group_id')}" src="/openerp/static/images/treegrid/expand.gif" onclick="toggle_group_data('${grp_row.get('group_id')}');"></img>
                        </td>
                        % endif
                        
                        % for i, (field, field_attrs) in enumerate(headers):
                        <td class="grid-cell ${field_attrs.get('type', 'char')}" style="background-color: #CCCCCC;">
                        	% if map(lambda x: x[0],hiddens).__contains__('sequence') or  field == 'sequence':
								<span class="draggable">${grp_row.get(field)}</span>
								<script type="text/javascript">
									function make_draggale(){
										var drag = getElementsByTagAndClassName('span','draggable');
										for(var j=0;j< drag.length;j++) {
											new Draggable(drag[j].parentNode.parentNode,{revert:true,ghosting:true});
											new Droppable(drag[j].parentNode.parentNode,{accept: [drag[j].parentNode.parentNode.className], ondrop: new ListView('${name}').sort_by_drag});
										}		
									}
							</script>
							% else:	
								<span>${grp_row.get(field)}</span>
							% endif
                        </td>
                        % endfor
                        
                        % if buttons:
                        <td class="grid-cell button" nowrap="nowrap" style="background-color: #CCCCCC;">
                        	<div style="width: 0px;"></div>
                        </td>
                        % endif
                        
                        % if editable:
                        <td class="grid-cell selector" style="background-color: #CCCCCC;">
                            <div style="width: 0px;"></div>
                        </td>
                        % endif
                    </tr>
                        
                    % for ch in grp_row.get('child_rec'):
	                    <tr class="grid-row ${grp_row.get('group_id')}" record="${ch.get('id')}" style="cursor: pointer; display: none;">
	                        % if editable:
	                        <td class="grid-cell">
	                            <img src="/openerp/static/images/listgrid/edit_inline.gif" class="listImage" border="0" title="${_('Edit')}" onclick="editRecord(${ch.get('id')}, '${source}')"/>
	                        </td>
	                        % endif
	                        % for i, (field, field_attrs) in enumerate(headers):
	                        <td class="grid-cell ${field_attrs.get('type', 'char')}" style="padding-left: 15px; ${(ch.get(field).color or None) and 'color: ' + ch.get(field).color};" sortable_value="${ch.get(field).get_sortable_text()}">
	                        	% if map(lambda x: x[0], hiddens).__contains__('sequence') or field == 'sequence':
									<span class="draggable">${ch.get(field).display()}</span>
									<script type="text/javascript">
										function make_draggale(){
											var drag = getElementsByTagAndClassName('span','draggable');
											for(var j=0;j< drag.length;j++) {
												new Draggable(drag[j].parentNode.parentNode,{revert:true,ghosting:true});
												new Droppable(drag[j].parentNode.parentNode,{accept: [drag[j].parentNode.parentNode.className], ondrop: new ListView('${name}').sort_by_drag});
											}		
										}
								</script>
								% else:	
									<span>${ch[field].display()}</span>
								% endif
	                        </td>
	                        % endfor
	                        % if buttons:
	                        <td class="grid-cell button" nowrap="nowrap">
	                            % for button in buttons:
	                            ${button.display(parent_grid=name, **button.params_from(ch))}
	                            % endfor
	                        </td>
	                        % endif
	                        % if editable:
	                        <td class="grid-cell selector">
	                            <img src="/openerp/static/images/listgrid/delete_inline.gif" class="listImage" border="0" title="${_('Delete')}" onclick="new ListView('${name}').remove(${ch.get('id')})"/>
	                        </td>
	                        % endif
	                    </tr>
	              	% endfor
                	% endfor

                    % for i in range(0, min_rows - len(grp_records)):
                    <tr class="grid-row-group">
                        % if editable:
                        <td style="text-align: center" class="grid-cell selector">&nbsp;</td>
                        % endif
                        % for i, (field, field_attrs) in enumerate(headers):
                        <td class="grid-cell">&nbsp;</td>
                        % endfor
                        % if buttons:
                        <td class="grid-cell button">&nbsp;</td>
                        % endif
                        % if editable:
                        <td style="text-align: center" class="grid-cell selector">&nbsp;</td>
                        % endif
                    </tr>
                    % endfor

                </tbody>

                % if field_total:
                <tfoot>
                    <tr class="field_sum">
                        % if editable:
                        <td width="1%" class="grid-cell">&nbsp;</td>
                        % endif
                        % for i, (field, field_attrs) in enumerate(headers):
                        <td class="grid-cell" style="text-align: right; padding: 2px;" nowrap="nowrap">
                             % if 'sum' in field_attrs:
                                 % for key, val in field_total.items():
                                     % if field == key:
                                     <span style="border-top: 1px inset ; display: block; padding: 0px 1px;">${val[1]}</span>
                                     % endif
                                 % endfor
                             % endif
                             % if 'sum' not in field_attrs:
                             &nbsp;
                             % endif
                        </td>
                        % endfor
                        % if buttons:
                        <td class="grid-cell button"><div style="width: 0px;"></div></td>
                        % endif
                        % if editable:
                        <td width="1%" class="grid-cell">&nbsp;</td>
                        % endif
                    </tr>
                </tfoot>
                % endif

            </table>
        </td>
    </tr>

    % if pageable:
    <tr class="pagerbar">
        <td class="pagerbar-cell pagerbar-links" align="left">
            <a href="javascript: void(0)" onclick="new ListView('${name}').importData()">${_("Import")}</a> | <a href="javascript: void(0)" onclick="new ListView('${name}').exportData()">${_("Export")}</a>
        </td>
        <td class="pagerbar-cell" align="right">${pager.display(pager_id=2)}</td>
    </tr>
    % endif
</table>

