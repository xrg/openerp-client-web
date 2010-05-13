<%!
import itertools
%>
<div class="box-a list-a">
	<div class="inner">
	<table id="${name}" class="gridview" width="100%" cellspacing="0" cellpadding="0">
	    % if pageable:
	    <tr class="pagerbar">
	        <td colspan="2" class="pagerbar-cell" align="right">
	        	<table class="pager-table" width="0%">
	        		<tr>
	        			<td class="pager-cell">
	        				<h2>${string} List</h2>
	        			</td>
	        			<script type="text/javascript">
	        				if(jQuery('#${name}').length>0) {
	        					if(jQuery('#_m2m_${name}').length>0) {
	        						if('${editable}' != 'False') { 
		        						jQuery('#${name}').find('td.pager-cell:first').after('<td style="width: 10%;" class="pager-cell button"> <a title="${_('Add records...')}" class="button-a" href="javascript: void(0)" id="${name}_button1">add</a></td>')
		        						jQuery('#${name}_button1').click(function() {
		        							open_search_window(jQuery('#_m2m_${name}').attr('relation'), jQuery('#_m2m_${name}').attr('domain'), jQuery('#_m2m_${name}').attr('context'),'${name}', 2, jQuery('#${name}_set').val())
		        						});
	        						}
	        					}
	        					else if(jQuery('#_o2m_${name}').length>0) {
	        						jQuery('#${name}').find('td.pager-cell:first').after('<td style="width: 10%;" class="pager-cell"><a class="button-a" href="javascript: void(0)" id="${name}_btn_" title="${_('Create new record.')}">new<a/></td>');
	        						jQuery('#${name}_btn_').click(function() {
	        							new One2Many('${name}', jQuery('#_o2m_${name}').attr('detail')).create()
	        						});
	        					}
	        					else {
	        						jQuery('#${name}').find('td.pager-cell:first').after('<td style="width: 10%;" class="pager-cell-button"><a class="button-a" href="javascript: void(0)" title="${_('Create new record.')}">new<a/></td>');
	        						if("${editors}" == "{}") {
	        							jQuery('#${name}').find('td.pager-cell-button:first').find('a:first').click(function() {
	        								editRecord(null);
	        							});
	        						}
	        						else {
	        							jQuery('#${name}').find('td.pager-cell-button:first').find('a:first').click(function() {
	        								new ListView('_terp_list').create()
	        							});	
	        						}
	        					}
	        				}
	        			</script>
	        			
        				<td class="pager-cell" style="width: 90%">
        					${pager.display()}
        				</td>
	        		</tr>
	        	</table>
	        </td>
	    </tr>
	    % endif
	    <tr>
	        <td colspan="2" style="border: none;">
	            <table id="${name}_grid" class="grid" width="100%" cellspacing="0" cellpadding="0" style="background: none;">
	                <thead>
	                    <tr class="grid-header">
	                        % if selector:
	                        <th width="1" class="grid-cell selector">
	                            % if selector=='checkbox':
	                            <input type="checkbox" class="checkbox grid-record-selector" onclick="new ListView('${name}').checkAll(!this.checked)"/>
	                            % endif
	                            % if selector!='checkbox':
	                            <span>&nbsp;</span>
	                            % endif
	                        </th>
	                        % endif
	                        % if editable:
	                        <th class="grid-cell selector"><div style="width: 0px;"></div></th>
	                        % endif
	                        % for (field, field_attrs) in headers:
	                        % if field == 'button':
	                        	<th class="grid-cell"></th>
	                        %else: 
	                        	<th id="grid-data-column/${(name != '_terp_list' or None) and (name + '/')}${field}" class="grid-cell ${field_attrs.get('type', 'char')}" kind="${field_attrs.get('type', 'char')}" style="cursor: pointer;" onclick="new ListView('${name}').sort_by_order('${field}')">${field_attrs['string']}</th>
	                    	% endif
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
	                    <%def name="make_editors(data=None)">
	                    % if editable and editors:
	                    <tr class="grid-row editors">
	                        % if selector:
	                        <td class="grid-cell selector">&nbsp;</td>
	                        % endif
	                        <td class="grid-cell selector" style="text-align: center; padding: 0px;">
	                            <!-- begin hidden fields -->
	                            % for field, field_attrs in hiddens:
	                            ${editors[field].display()}
	                            % endfor
	                            <!-- end of hidden fields -->
	                            <img src="/openerp/static/images/listgrid/save_inline.gif" class="listImage editors" border="0" title="${_('Update')}" onclick="new ListView('${name}').save(${(data and data['id']) or 'null'})"/>
	                        </td>
	                        % for i, (field, field_attrs) in enumerate(headers):
	                        	% if field=='button':
		                        	<td class="grid-cell">
		                        	</td>
		                        % else:
		                        	<td class="grid-cell ${field_attrs.get('type', 'char')}">
		                            	${editors[field].display()}
		                        	</td>
	                        	% endif
	                        % endfor
	                        <td class="grid-cell selector" style="text-align: center; padding: 0px;">
	                            <img src="/openerp/static/images/iconset-b-remove.gif" class="listImage editors" border="0" title="${_('Cancel')}" onclick="new ListView('${name}').reload()"/>
	                        </td>
	                    </tr>
	                    % endif
	                    </%def>
	
	                    <%def name="make_row(data)">
	                    <tr class="grid-row" record="${data['id']}" style="cursor: pointer;">
	                        % if selector:
	                        <td class="grid-cell selector">
	                            <input type="${selector}" class="${selector} grid-record-selector" id="${name}/${data['id']}" name="${(checkbox_name or None) and name}" value="${data['id']}"/>
	                        </td>
	                        % endif
	                        % if editable:
	                        <td class="grid-cell selector">
	                            % if not editors:
	                            <img src="/openerp/static/images/iconset-b-edit.gif" class="listImage" border="0" title="${_('Edit')}" onclick="editRecord(${data['id']}, '${source}')"/>
	                            % elif not editors:
	                            <img src="/openerp/static/images/iconset-b-edit.gif" border="0" title="${_('Edit')}"/>
	                            % endif                            
	                            % if editors:
	                            <img src="/openerp/static/images/iconset-b-edit.gif" class="listImage" border="0" title="${_('Edit')}" onclick="new ListView('${name}').edit(${data['id']})"/>
	                            % endif
	                        </td>
	                        % endif
	                        % for i, (field, field_attrs) in enumerate(headers):
	                        %if field=='button':
	                        	<td class="grid-cell"><span>${buttons[field_attrs-1].display(parent_grid=name, **buttons[field_attrs-1].params_from(data))}</span></td>
	                        %else:
		                        <td class="grid-cell ${field_attrs.get('type', 'char')}" style="${(data[field].color or None) and 'color: ' + data[field].color};" sortable_value="${data[field].get_sortable_text()}">
									<span>${data[field].display()}</span>
		                        </td>
	                        % endif
	                        % endfor
	                        
	                        % if editable:
	                        <td class="grid-cell selector">
	                            <img src="/openerp/static/images/iconset-b-remove.gif" class="listImage" border="0" title="${_('Delete')}" onclick="new ListView('${name}').remove(${data['id']})"/>
	                        </td>
	                        % endif
	                    </tr>
	                    </%def>
	
	                    % if edit_inline == -1:
	                    ${make_editors()}
	                    % endif
	
	                    % for i, d in enumerate(data):
	                        % if d['id'] == edit_inline:
	                        ${make_editors(d)}
	                        % endif
	                        % if d['id'] != edit_inline:
	                        ${make_row(d)}
	                        % endif
	                    % endfor
	
	                    % if concurrency_info:
	                    <tr style="display: none">
	                        <td>${concurrency_info.display()}</td>
	                    </tr>
	                    % endif
	
	                    % for i in range(0, min_rows - len(data)):
	                    <tr class="grid-row">
	                        % if selector:
	                        <td width="1%" class="grid-cell selector">&nbsp;</td>
	                        % endif
	                        % if editable:
	                        <td style="text-align: center" class="grid-cell selector">&nbsp;</td>
	                        % endif
	                        % for i, (field, field_attrs) in enumerate(headers):
	                        % if field == 'button':
	                        	<td class="grid-cell button">&nbsp;</td>
	                    	% else:
	                        	<td class="grid-cell">&nbsp;</td>
	                    	% endif
	                        % endfor
	                        % if editable:
	                        <td style="text-align: center" class="grid-cell selector">&nbsp;</td>
	                        % endif
	                    </tr>
	                    % endfor
	
	                </tbody>
	
	               % if field_total:
                    <tfoot>
                        <tr class="field_sum" style="border: none; border-bottom: 1px solid #f4f2f2;">
                            % if selector:
                                <td width="1%" class="grid-cell">&nbsp;</td>
                            % endif
                            % if editable:
                                <td width="1%" class="grid-cell">&nbsp;</td>
                            % endif
                            % for i, (field, field_attrs) in enumerate(headers):
                                % if field == 'button':
                                    <td class="grid-cell button"><div style="width: 0;"></div></td>
                                % else:
                                    
                                    	% if i == 0:
                                    	<td class="grid-cell" style="text-align: left; padding: 2px;" nowrap="nowrap">
                                    		<strong style="color: black;">Total</strong>
                                   		</td>
                                    	% else:
                                    		<td class="grid-cell" style="text-align: right; padding: 2px;" nowrap="nowrap">
	                                         % if 'sum' in field_attrs:
	                                             % for key, val in field_total.items():
	                                                 % if field == key:
	                                                 <span id="${field}" style="border-top: 1px inset ; display: block; padding: 0 1px; color: black;">${val[1]}</span>
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
	
	            % if data and 'sequence' in map(lambda x: x[0], itertools.chain(headers,hiddens)):
				<script type="text/javascript">
					var drag = getElementsByTagAndClassName('tr','grid-row');
					jQuery('tr.grid-row').each(function() {
						jQuery(this).draggable({
							revert: 'valid',
							connectToSortable: 'tr.grid-row',
							helper: function() {
								var htmlStr = jQuery(this).html();
								return jQuery('<table><tr id class="ui-widget-header">'+htmlStr+'</tr></table>');
							},
							axis: 'y'
						});
											
						jQuery(this).droppable({ 
							accept: 'tr.grid-row',
							hoverClass: 'grid-rowdrop',
							drop: function(ev, ui) {
								new ListView('${name}').dragRow(ui.draggable.attr('record'), $(this).attr('record'));
							}
						});
						
					})
				</script>
				
				% endif 
	        </td>
	    </tr>
	
	    % if pageable:
	    <tr class="pagerbar">
	        <td class="pagerbar-cell footer" align="right">${pager.display(pager_id=2)}</td>
	    </tr>
	    % endif
	</table>
	</div>
</div>
