<%!
import itertools
import cherrypy
%>

<%def name="make_editors(data=None)">
    % if editable and editors:
        <tr class="grid-row editors">
            % if selector:
            	<td class="grid-cell selector">&nbsp;</td>
            % endif
            <td class="grid-cell selector" style="text-align: center; padding: 0;">
                <!-- begin hidden fields -->
                % for field, field_attrs in hiddens:
                	${editors[field].display()}
                % endfor
                <!-- end of hidden fields -->
                <img alt="save record" src="/openerp/static/images/listgrid/save_inline.gif"
                     class="listImage editors" border="0" title="${_('Update')}"
                     onclick="new ListView('${name}').save(${(data and data['id']) or 'null'})"/>
            </td>
            % for i, (field, field_attrs) in enumerate(headers):
                % if field == 'button':
                    <td class="grid-cell">
                    </td>
                % else:
                    <td class="grid-cell ${field_attrs.get('type', 'char')}">
                        ${editors[field].display()}
                    </td>
                % endif
            % endfor
            <td class="grid-cell selector" style="text-align: center; padding: 0;">
                <img alt="delete record" src="/openerp/static/images/iconset-b-remove.gif"
                     class="listImage editors" border="0" title="${_('Cancel')}"
                     onclick="new ListView('${name}').reload()"/>
            </td>
        </tr>
    % endif
</%def>

<%def name="make_row(data, row_num)">
	<%
		if row_num % 2:
			row_class = 'grid-row-even'
		else:
			row_class = 'grid-row-odd'
	%>
	% if editors:
    	<tr class="grid-row inline_editors ${row_class}" record="${data['id']}">
    % else:
    	<tr class="grid-row ${row_class}" record="${data['id']}">
    % endif
        % if selector:
            <td class="grid-cell selector">
                <input type="${selector}" class="${selector} grid-record-selector"
                       id="${name}/${data['id']}" name="${(checkbox_name or None) and name}"
                       value="${data['id']}"
                       onclick="new ListView('${name}').onBooleanClicked(!this.checked, '${data['id']}')"/>
            </td>
        % endif
        % if editable:
            <td class="grid-cell selector">
                % if not editors:
                    <img alt="edit record" src="/openerp/static/images/iconset-b-edit.gif"
                         class="listImage" border="0" title="${_('Edit')}"
                         onclick="editRecord(${data['id']}, '${source}')"/>
                % else:
                    <img alt="edit record" src="/openerp/static/images/iconset-b-edit.gif"
                         class="listImage" border="0" title="${_('Edit')}"
                         onclick="new ListView('${name}').edit(${data['id']})"/>
                % endif
            </td>
        % endif
        % for i, (field, field_attrs) in enumerate(headers):
            %if field == 'button':
                <td class="grid-cell">
                    <span>${buttons[field_attrs-1].display(parent_grid=name, **buttons[field_attrs-1].params_from(data))}</span>
                </td>
            % else:
                <td class="grid-cell ${field_attrs.get('type', 'char')}"
                    style="${(data[field].color or None) and 'color: ' + data[field].color};"
                    sortable_value="${data[field].get_sortable_text()}">
                    <span>${data[field].display()}</span>
                </td>
            % endif
        % endfor

        % if editable:
            <td class="grid-cell selector">
                <img src="/openerp/static/images/iconset-b-remove.gif" class="listImage"
                     border="0" title="${_('Delete')}"
                     onclick="new ListView('${name}').remove(${data['id']})"/>
            </td>
        % endif
    </tr>
</%def>

<div class="box-a list-a">
	<div class="inner">
	<table id="${name}" class="gridview" width="100%" cellspacing="0" cellpadding="0">
	    % if pageable:
	    <tr class="pagerbar">
	        <td colspan="2" class="pagerbar-cell" align="right">
	        	<table class="pager-table">
	        		<tr>
	        			<td class="pager-cell">
	        				<h2>${string} List</h2>
	        			</td>
	        			% if editable:
	        			    <td class="pager-cell-button">
	        			        % if m2m:
	        			            <a class="button-a" href="javascript: void(0)" title="${_('Add records...')}" id="${name}_button1">${_('add')}</a>
	        			            <script type="text/javascript">
	        			                jQuery('#${name}_button1').click(function() {
	        			                    open_search_window(jQuery('#_m2m_${name}').attr('relation'), jQuery('#_m2m_${name}').attr('domain'), jQuery('#_m2m_${name}').attr('context'),'${name}', 2, jQuery('#${name}_set').val())
	        			                });
	        			            </script>
	        			        % elif o2m:
	        			            <a class="button-a" href="javascript: void(0)" title="${_('Create new record.')}" id="${name}_btn_">${_('new')}</a>
	        			            <script type="text/javascript">
                                        jQuery('a.button-a[id*=${name}_btn]').click(function() {
                                            new One2Many('${name}', jQuery('table.one2many[id$=${name}]').attr('detail')).create();
                                        });
                                    </script>
	        			        % else:
	        			            <a id="${name}_new" class="button-a" href="javascript: void(0)" title="${_('Create new record.')}">${_('new')}<a/>
	        			            % if editors:
	        			                <script type="text/javascript">
	        			                    jQuery('#${name}_new').click(function() {
	        			                        new ListView('_terp_list').create();
	        			                    });

	        			                </script>
	        			            % else:
	        			                <script type="text/javascript">
	        			                    jQuery('#${name}_new').click(function() {
	        			                        editRecord(null);
	        			                    });
	        			                </script>
	        			            % endif
	        			        % endif
	        			    </td>
	        			% endif
	        			<td class="pager-cell-button" style="display: none;">
	        			    <a id="${name}_delete_record" class="button-a" href="javascript: void(0)" title="${_('Delete record(s).')}">${_('delete')}<a/>
	        			    <script type="text/javascript">
	        			        jQuery('#${name}_delete_record').click(function() {
-                                        new ListView('_terp_list').remove(null,this);
                                });
	        			    </script>
	        			</td>
	        			<td class="pager-cell-button" style="display: none;">
                            <a id="${name}_edit_record" class="button-a" href="javascript: void(0)" title="${_('Edit record(s).')}">${_('edit')}<a/>
                            <script type="text/javascript">
                                jQuery('#${name}_edit_record').click(function() {
-                                       editSelectedRecord();
                                });
                            </script>
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
	                        <th class="grid-cell selector"><div style="width: 0;"></div></th>
	                        % endif
	                        % for (field, field_attrs) in headers:
		                        % if field == 'button':
		                        	<th class="grid-cell"></th>
		                        %else:
		                        	<th id="grid-data-column/${(name != '_terp_list' or None) and (name + '/')}${field}" class="grid-cell ${field_attrs.get('type', 'char')}" kind="${field_attrs.get('type', 'char')}" style="cursor: pointer;" onclick="new ListView('${name}').sort_by_order('${field}')">${field_attrs['string']}</th>
		                    	% endif
	                        % endfor
	                        % if buttons:
	                        	<th class="grid-cell button"><div style="width: 0;"></div></th>
	                        % endif
	                        % if editable:
	                        	<th class="grid-cell selector"><div style="width: 0;"></div></th>
	                        % endif
	                    </tr>
	                </thead>

	                <tbody>
                        % if edit_inline == -1:
                            ${make_editors()}
                        % endif
                        % for i, d in enumerate(data):
                            % if d['id'] == edit_inline:
                                ${make_editors(d)}
                            % else:
                                ${make_row(d, i)}
                            % endif
                        % endfor
                        % if concurrency_info:
	                        <tr style="display: none">
	                            <td>${concurrency_info.display()}</td>
	                        </tr>
                        % endif
                        % for i in range(min_rows - len(data)):
	                        % if editors:
	                        	<tr class="grid-row inline_editors">
	                        % else:
	                        	<tr class="grid-row">
	                        % endif
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
                        <tr class="field_sum">
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
					// flag is used to check sorting is active or not //
                    var flag = "${'_terp_sort_key' in cherrypy.request.params.keys()}";

		            if(flag == 'False') {
                        jQuery('#${name} tr.grid-row').draggable({
                            revert: 'valid',
                            connectToSortable: 'tr.grid-row',
                            helper: function() {
                                var htmlStr = jQuery(this).html();
                                return jQuery('<table><tr id class="ui-widget-header">'+htmlStr+'</tr></table>');
                            },
                            axis: 'y'
                        });

                        jQuery('#${name} tr.grid-row').droppable({
                            accept: 'tr.grid-row',
                            hoverClass: 'grid-rowdrop',
                            drop: function(ev, ui) {
                                new ListView('${name}').dragRow(ui.draggable, jQuery(this), '${name}');
                            }
                        });

		            }
				</script>
			% endif

            % if editors:
                <script type="text/javascript">
                	/* In editable grid, clicking on empty row will create new and on existing row will edit. */

                    jQuery('table[id=${name}_grid] tr.grid-row').each(function(index, row) {
	                    jQuery(row).click(function(event) {
	                        if (!(event.target.tagName == 'INPUT' || event.target.tagName == 'IMG')) {
	                            record_id = jQuery(row).attr('record');
	                            if (record_id > 0) {
	                                new ListView('${name}').edit(record_id);
	                            }
	                            else {
	                                new One2Many('${name}', jQuery('table.one2many[id$=${name}]').attr('detail')).create();
	                            }
	                        }
	                    });
                    });
                </script>
            % else:
                <script type="text/javascript">
                    if('${name}' == '_terp_list') {
                        var view_type = jQuery('#_terp_view_type').val();
                        var editable = jQuery('#_terp_editable').val();
                    }
                    else {
                        var view_type = jQuery('[id=${name}/_terp_view_type]').val();
                        var editable = jQuery('[id=${name}/_terp_editable]').val();
                    }

                    jQuery('table#${name}_grid tr.grid-row').each(function(index, row) {
                        jQuery(row).click(function(event) {
                            if (!(event.target.nodeName == 'IMG' || event.target.nodeName == 'INPUT')) {
                                if (view_type == 'tree') {
                                    do_select(jQuery(row).attr('record'));
                                }
                            }
                        });
                    });

                    jQuery('table#${name}_grid tr.grid-row').each(function(index, row) {
                        jQuery(row).dblclick(function(event) {
                            if (!(event.target.className == 'checkbox grid-record-selector' || event.target.className == 'listImage')) {
                                if (view_type == 'tree') {
                                    if (editable != 'True') {
                                        do_select(jQuery(row).attr('record'));
                                    }
                                    else {
                                        editRecord(jQuery(row).attr('record'));
                                    }
                                }
                            }
                        });
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
