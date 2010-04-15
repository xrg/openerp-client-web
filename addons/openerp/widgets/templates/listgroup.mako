<%!
import itertools
background = '#DEDEDE'
%>

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
                            % if field == 'button':
                                <th class="grid-cell button"><div style="width: 0px;"></div></th>
                            % else:
                                <th id="grid-data-column/${(name != '_terp_list' or None) and (name + '/')}${field}" class="grid-cell ${field_attrs.get('type', 'char')}" kind="${field_attrs.get('type', 'char')}" style="cursor: pointer;" onclick="new ListView('${name}').sort_by_order('${field}')">${field_attrs['string']}</th>
                            % endif
                        % endfor
                        % if editable:
                            <th class="grid-cell selector"><div style="width: 0px;"></div></th>
                        % endif
                    </tr>
                </thead>

                <tbody>
					% for j, grp_row in enumerate(grp_records):
					<tr class="grid-row-group" records="${grp_row.get('group_id')}" style="cursor: pointer;" ch_records="${map(lambda x: x['id'],grp_row['child_rec'])}" grp_domain="${grp_row['__domain']}">
                        % if editable:
                            <td class="grid-cell" style="background-color: ${background};">
                                <img id="img_${grp_row.get('group_id')}" class="group_expand"></img>
                                <script type="text/javascript">
					            	jQuery("[id=img_${grp_row.get('group_id')}]").click(function() {
					            		jQuery(this).toggleClass('group_collapse',100);
					            		jQuery("tr[id=grid-row ${grp_row.get('group_id')}]").toggle();
					            	});
					            	
					            </script>
                            </td>
                        % endif

                        % for i, (field, field_attrs) in enumerate(headers):
                            % if field != 'button':
                                <td class="grid-cell ${field_attrs.get('type', 'char')}"
                                    style="background-color: ${background};">
                                    % if field_attrs.get('type') == 'progressbar':
                                        <span>${grouped[j][field].display()}</span>
                                    % else:
                                        <span>${grp_row.get(field)}</span>
                                    % endif
                                </td>
                            % else:
                                <td class="grid-cell button" nowrap="nowrap" style="background-color: ${background};">
                                    <span></span>
                                </td>
                            % endif
                        % endfor
                        
                        % if editable:
                            <td class="grid-cell selector" style="background-color: ${background};">
                                <div style="width: 0px;"></div>
                            </td>
                        % endif
                    </tr>

                    % for ch in grp_row.get('child_rec'):
                    <tr class="grid-row-group" id="grid-row ${grp_row.get('group_id')}" record="${ch.get('id')}"
                        style="cursor: pointer; display: none;">
                        % if editable:
                            <td class="grid-cell">
                                <img src="/openerp/static/images/listgrid/edit_inline.gif" class="listImage" border="0"
                                     title="${_('Edit')}" onclick="editRecord(${ch.get('id')}, '${source}')"/>
                            </td>
                        % endif
                        % for i, (field, field_attrs) in enumerate(headers):
                            % if field != 'button':
                                <td class="grid-cell ${field_attrs.get('type', 'char')}"
                                    style="padding-left: 15px; ${(ch.get(field).color or None) and 'color: ' + ch.get(field).color};"
                                    sortable_value="${ch.get(field).get_sortable_text()}">
                                    <span>${ch[field].display()}</span>
                                </td>
                            % else:
                                <td class="grid-cell button" nowrap="nowrap">
                                    ${buttons[field_attrs-1].display(parent_grid=name, **buttons[field_attrs-1].params_from(ch))}
                                </td>
                            % endif
                        % endfor

                        % if editable:
                            <td class="grid-cell selector">
                                <img src="/openerp/static/images/listgrid/delete_inline.gif" class="listImage" border="0"
                                     title="${_('Delete')}" onclick="new ListView('${name}').remove(${ch.get('id')})"/>
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
                        % if editable:
                        <td style="text-align: center" class="grid-cell selector">&nbsp;</td>
                        % endif
                    </tr>
                    % endfor

                </tbody>

                % if field_total:
                <tfoot>
                    <tr class="field_sum">
                        <td colspan="${len(headers)}" style="border: none;">
                    		<table style="width: 40%; border: none;">
                    			<tr>
                    				% for i, (field, field_attrs) in enumerate(headers):
		                        		% if field != 'button':
		                        			% if 'sum' in field_attrs:
		                        				% for key, val in field_total.items():
				                                     % if field == key:
				                                     <td align="left" class="grid-cell" style="padding: 2px;" nowrap="nowrap">
				                                     	<strong style="color: black;">${val[0]}:</strong>
				                                     	${val[1]}
				                                     </td>
				                                     % endif
				                                 % endfor
		                        			% endif
		                        		% endif
		                        	% endfor
                    			</tr>
                    		</table>
                    	</td>
                    </tr>
                </tfoot>
                % endif
            </table>
            % if 'sequence' in map(lambda x: x[0], itertools.chain(headers,hiddens)):
                <script type="text/javascript">
                    jQuery('table[id=${name}_grid] tbody tr.grid-row-group').each(function(index, row) {
                   		jQuery(row).draggable({
                   				revert: 'valid',
                   				connectToSortable: 'tr.grid-row-group',
                   				helper: function() {
                   					var htmlStr = jQuery(this).html();
                   					return jQuery('<table><tr class="ui-widget-header">'+htmlStr+'</tr></table>');
                   				},
                   				axis: 'y'
                   		});
                   		
                   		jQuery(row).droppable({
                   			accept : 'tr.grid-row-group',
                   			hoverClass: 'grid-rowdrop',
                   			drop: function(ev, ui) {
                   				console.log('drag',ui.draggable);
                   				console.log('drop',jQuery(this));
                   			}
                   		});
					});
                </script>
            % endif
            
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

