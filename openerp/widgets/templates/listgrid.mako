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
                        <th id="grid-data-column/${(name != '_terp_list' or None) and (name + '/')}${field}" class="grid-cell ${field_attrs.get('type', 'char')}" kind="${field_attrs.get('type', 'char')}">${field_attrs['string']}</th>
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
                            <img src="/static/images/listgrid/save_inline.gif" class="listImage editors" border="0" title="${_('Update')}" onclick="new ListView('${name}').save(${(data and data['id']) or 'null'})"/>
                        </td>
                        % for i, (field, field_attrs) in enumerate(headers):
                        <td class="grid-cell ${field_attrs.get('type', 'char')}">
                            ${editors[field].display()}
                        </td>
                        % endfor
                        <td class="grid-cell selector" style="text-align: center; padding: 0px;">
                            <img src="/static/images/listgrid/delete_inline.gif" class="listImage editors" border="0" title="${_('Cancel')}" onclick="new ListView('${name}').reload()"/>
                        </td>
                    </tr>
                    % endif
                    </%def>
            
                    <%def name="make_row(data)">
                    <tr class="grid-row" record="${data['id']}">
                        % if selector:
                        <td class="grid-cell selector">
                            <input type="${selector}" class="${selector} grid-record-selector" id="${name}/${data['id']}" name="${(checkbox_name or None) and name}" value="${data['id']}"/>
                        </td>
                        % endif
                        % if editable:
                        <td class="grid-cell selector">
                            % if not editors:
                            <img src="/static/images/listgrid/edit_inline.gif" class="listImage" border="0" title="${_('Edit')}" onclick="editRecord(${data['id']}, '${source}')"/>
                            % else:
                            <img src="/static/images/listgrid/edit_inline.gif" class="listImage" border="0" title="${_('Edit')}" onclick="new ListView('${name}').edit(${data['id']})"/>
                            % endif
                        </td>
                        % endif
                        % for i, (field, field_attrs) in enumerate(headers):
                        <td class="grid-cell ${field_attrs.get('type', 'char')}" style="${(data[field].color or None) and 'color: ' + data[field].color};" sortable_value="${data[field].get_sortable_text()}">
                            % if i==0:
                                % if link==1:
                                	%if data[field].link:
                                    	${data[field].display()}
                                	%else:
                                    	<span>
                                        	<a href="javascript: void(0)" onclick="do_select(${data['id']}, '${name}'); return false;">${data[field]}</a>
                                    	</span>
                                	% endif
                                % else:
                                <span>
                                	 ${data[field]}
                                </span>
                                % endif
                            % else:
                                % if show_links:
                                ${data[field].display()}
                                % else:
                                <span>${data[field]}</span>
                                % endif
                            %endif
                            
                            % if editable and field == 'sequence':
                            <span class="selector">
                                <img src="/static/images/listgrid/arrow_up.gif" class="listImage" border="0" title="${_('Move Up')}" onclick="new ListView('${name}').moveUp(${data['id']})"/>
                                <img src="/static/images/listgrid/arrow_down.gif" class="listImage" border="0" title="${_('Move Down')}" onclick="new ListView('${name}').moveDown(${data['id']})"/>
                            </span>
                            % endif
                        </td>
                        % endfor
                        % if buttons:
                        <td class="grid-cell button" nowrap="nowrap">
                            % for button in buttons:
                            ${button.display(parent_grid=name, **button.params_from(data))}
                            % endfor
                        </td>
                        % endif
                        % if editable:
                        <td class="grid-cell selector">
                            <img src="/static/images/listgrid/delete_inline.gif" class="listImage" border="0" title="${_('Delete')}" onclick="new ListView('${name}').remove(${data['id']})"/>
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
                        % if selector:
                        <td width="1%" class="grid-cell">&nbsp;</td>
                        % endif
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
            
            <script type="text/javascript">
                new SortableGrid('${name}_grid');
            </script>
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

