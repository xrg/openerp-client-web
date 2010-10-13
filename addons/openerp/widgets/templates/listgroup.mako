<%!
import itertools
%>
<div class="box-a list-a">
<div class="inner">
<table id="${name}" groups="${group_by_ctx}" class="gridview" width="100%" cellspacing="0" cellpadding="0">
    % if pageable:
    <tr class="pagerbar">
        <td colspan="2" class="pagerbar-cell" align="right">
        	<table class="pager-table">
        		<tr>
        			<td class="pager-cell">
        				<h2>${string}</h2>
        			</td>
        			<td id="${name}" class="loading-list" style="display: none;">
        				<img src="/openerp/static/images/load.gif" width="16" height="16" title="loading..."/>
        			</td>
        			<td class="pager-cell" style="width: 90%">
    					${pager.display()}
    				</td>
        		</tr>
        	</table>
        </td>
    </tr>
    % endif
    
    <tr>
        <td colspan="2">
            <table id="${name}_grid" class="grid" width="100%" cellspacing="0" cellpadding="0">
                <thead>
                    <tr class="grid-header">
                        % if editable:
                            <th class="grid-cell selector"><div style="width: 0;"></div></th>
                        % endif
                        % for (field, field_attrs) in headers:
                            % if field == 'button':
                                <th class="grid-cell"><div style="width: 0;"></div></th>
                            % else:
                                <th id="grid-data-column/${(name != '_terp_list' or None) and (name + '/')}${field}" class="grid-cell ${field_attrs.get('type', 'char')}" kind="${field_attrs.get('type', 'char')}" style="cursor: pointer;" onclick="new ListView('${name}').sort_by_order('${field}', this)">${field_attrs['string']}</th>
                            % endif
                        % endfor
                        % if editable:
                            <th class="grid-cell selector"><div style="width: 0;"></div></th>
                        % endif
                    </tr>
                </thead>

                <tbody>
					% for j, grp_row in enumerate(grp_records):
					<tr class="grid-row-group" grp_by_id="${grp_row.get('group_by_id')}" records="${grp_row.get('group_id')}" style="cursor: pointer; " ch_records="${map(lambda x: x['id'], grp_row['child_rec'])}" grp_domain="${grp_row['__domain']}" grp_context="${grp_row['__context']['group_by']}">
                        % if editable:
                        
                            % if len(group_by_ctx) == 1 and group_by_no_leaf:
                                <td class="grid-cell"></td>
                            % elif len(group_by_ctx) > 0:
	                            <td class="grid-cell group-expand"
	                                onclick="new ListView('${name}').group_by('${grp_row.get('group_by_id')}', '${grp_row.get('group_id')}', '${group_by_no_leaf}', this);">
	                            </td>
                            % else:
                                <td class="grid-cell"></td>
                            % endif
                        % endif

                        % for i, (field, field_attrs) in enumerate(headers):
                            % if field != 'button':
                                <td class="grid-cell ${field_attrs.get('type', 'char')}" >
                                    % if field_attrs.get('type') == 'progressbar':
                                        ${grouped[j][field].display()}
                                    % else:
                                        % if grp_row.get(field):
                                            % if field_attrs.get('type') == 'many2one':
                                                ${grp_row.get(field)[-1]}
                                            % else:
                                                ${grp_row.get(field)}
                                            % endif
                                        % else:
                                            % if len(group_by_ctx):
                                                <span style="color: #888;">${(i == 0) and "undefined" or "&nbsp;"|n}</span>
                                            % else:
                                                <span style="color: #888;">&nbsp;</span>
                                            % endif
                                        % endif                                    
                                    % endif
                                </td>
                            % else:
                                <td class="grid-cell" nowrap="nowrap">
                                    <span></span>
                                </td>
                            % endif
                        % endfor
                        
                        % if editable:
                            <td class="grid-cell selector" >
                                <div style="width: 0;"></div>
                            </td>
                        % endif
                    </tr>

                    % for ch in grp_row.get('child_rec'):
                    <tr class="grid-row grid-row-group" id="${grp_row.get('group_id')}" parent_grp_id="${grp_row.get('group_by_id')}" 
                    	record="${ch.get('id')}" style="cursor: pointer; display: none;">
                        % if editable:
                            <td class="grid-cell">
                                <img src="/openerp/static/images/iconset-b-edit.gif" class="listImage" border="0"
                                     title="${_('Edit')}" onclick="editRecord(${ch.get('id')}, '${source}')"/>
                            </td>
                        % endif
                        % for i, (field, field_attrs) in enumerate(headers):
                            % if field != 'button':
                                <td class="grid-cell ${field_attrs.get('type', 'char')}"
                                    style="${(ch.get(field).color or None) and 'color: ' + ch.get(field).color};"
                                    sortable_value="${ch.get(field).get_sortable_text()}">
                                    <span>${ch[field].display()}</span>
                                </td>
                            % else:
                                <td class="grid-cell" nowrap="nowrap">
                                    ${buttons[field_attrs-1].display(parent_grid=name, **buttons[field_attrs-1].params_from(ch))}
                                </td>
                            % endif
                        % endfor

                        % if editable:
                            <td class="grid-cell selector">
                                <img src="/openerp/static/images/iconset-b-remove.gif" class="listImage" border="0"
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
                            % if editable:
                                <td width="1%" class="grid-cell">&nbsp;</td>
                            % endif
                            % for i, (field, field_attrs) in enumerate(headers):
                                % if field == 'button':
                                    <td class="grid-cell"><div style="width: 0;"></div></td>
                                % else:
                                    % if i == 0:
                                    <td class="grid-cell" id="total_sum_title" nowrap="nowrap">
                                        <strong id="total_sum_label"></strong>
                                    </td>
                                    % else:
                                        <td class="grid-cell" id="total_sum_value" nowrap="nowrap">
                                             % if 'sum' in field_attrs:
                                                 % for key, val in field_total.items():
                                                     % if field == key:
                                                        <span id="${field}" class="sum_value_field">${val[1]}</span>
                                                     % endif
                                                 % endfor
                                             % else:
                                                 &nbsp;
                                             % endif
                                         </td>
                                    % endif
                                % endif
                            % endfor
                            % if editable:
                                <td width="1%" class="grid-cell">&nbsp;</td>
                            % endif
                        </tr>
                    </tfoot>
                % endif
            </table>
            % if 'sequence' in map(lambda x: x[0], itertools.chain(headers,hiddens)):
                <script type="text/javascript">
                    jQuery('#${name} tr.grid-row-group').draggable({
                        revert: 'valid',
                        connectToSortable: 'tr.grid-row-group',
                        helper: function() {
                           var htmlStr = jQuery(this).html();
                           return jQuery('<table><tr class="ui-widget-header">'+htmlStr+'</tr></table>');
                        },
                        axis: 'y'
                    });
                    
                    jQuery('#${name} tr.grid-row-group').droppable({
                        accept : 'tr.grid-row-group',
                        hoverClass: 'grid-rowdrop',
                        drop: function(ev, ui) {
                                new ListView('${name}').groupbyDrag(ui.draggable, jQuery(this), '${name}');
                        }
                    });
                </script>
            % endif
        </td>
    </tr>

    % if pageable:
    <tr class="pagerbar">
        <td class="pagerbar-cell" align="right">${pager.display(pager_id=2)}</td>
    </tr>
    % endif
</table>
</div>
</div>

