<div xmlns:py="http://purl.org/kid/ns#" py:strip="">

    <table id="${name}" class="gridview" width="100%" cellspacing="0" cellpadding="0">
        <tr class="pagerbar" py:if="pageable">
            <td colspan="2" class="pagerbar-cell" align="right" py:content="pager.display()"></td>
        </tr>
        
        <tr>
            <td colspan="2">
                <table id="${name}_grid" class="grid" width="100%" cellspacing="0" cellpadding="0">
                    
                    <thead>
                        <tr class="grid-header">
                            <th width="1" py:if="selector" class="grid-cell selector">
                                <input type="checkbox" class="checkbox grid-record-selector" py:if="selector=='checkbox'" onclick="new ListView('${name}').checkAll(!this.checked)"/>
                                <span py:if="selector!='checkbox'">&nbsp;</span>
                            </th>
                            <th py:if="editable" class="grid-cell selector"><div style="width: 0px;"></div></th>
                            <th py:for="(field, field_attrs) in headers" id="grid-data-column/${(name != '_terp_list' or None) and (name + '/')}${field}" class="grid-cell ${field_attrs.get('type', 'char')}" kind="${field_attrs.get('type', 'char')}" py:content="field_attrs['string']"></th>
                            <th py:if="buttons" class="grid-cell button"><div style="width: 0px;"></div></th>
                            <th py:if="editable" class="grid-cell selector"><div style="width: 0px;"></div></th>
                        </tr>
                    </thead>
                    
                    <tbody>
                        <tr py:def="make_editors(data=None)" class="grid-row editors" py:if="editable and editors">
                            <td py:if="selector" class="grid-cell selector">&nbsp;</td>
                            <td class="grid-cell selector" style="text-align: center; padding: 0px;">
                                <!-- begin hidden fields -->
                                <span py:for="field, field_attrs in hiddens" py:replace="editors[field].display()"/>
                                <!-- end of hidden fields -->
                                <img src="/static/images/save_inline.gif" class="listImage editors" border="0" title="${_('Update')}" onclick="new ListView('${name}').save(${(data and data['id']) or 'null'})"/>
                            </td>
                            <td py:for="i, (field, field_attrs) in enumerate(headers)" class="grid-cell ${field_attrs.get('type', 'char')}">
                                ${editors[field].display()}
                            </td>
                            <td class="grid-cell selector" style="text-align: center; padding: 0px;">
                                <img src="/static/images/delete_inline.gif" class="listImage editors" border="0" title="${_('Cancel')}" onclick="new ListView('${name}').reload()"/>
                            </td>
                        </tr>
                
                        <tr py:def="make_row(data)" class="grid-row" record="${data['id']}">
                            <td py:if="selector" class="grid-cell selector">
                                <input type="${selector}" class="${selector} grid-record-selector" id="${name}/${data['id']}" name="${(checkbox_name or None) and name}" value="${data['id']}"/>
                            </td>
                            <td py:if="editable" class="grid-cell selector">
                                <img src="/static/images/edit_inline.gif" class="listImage" border="0" title="${_('Edit')}" py:if="not editors" onclick="editRecord(${data['id']}, '${source}')"/>
                                <img src="/static/images/edit_inline.gif" class="listImage" border="0" title="${_('Edit')}" py:if="editors" onclick="new ListView('${name}').edit(${data['id']})"/>
                            </td>
                            <td py:for="i, (field, field_attrs) in enumerate(headers)" class="grid-cell ${field_attrs.get('type', 'char')}" style="color: ${data[field].color};" sortable_value="${data[field].get_sortable_text()}">
                                <span py:if="i==0">
                                    <a href="${data[field].link}" onclick="${data[field].onclick}">${data[field]}</a>
                                </span>
                                <span py:if="i &gt; 0" py:replace="data[field].display()"/>
                                <span py:if="editable and field == 'sequence'" class="grid-cell selector">
                                    <img id="${data['id']}_moveup" src="/static/images/up.png" class="listImage" border="0" title="${_('Move Up')}" seq="${str(data['_seq'])}" onclick="new ListView('${name}').moveUp(${data['id']})"/>                                
                                </span>
                                <span py:if="editable and field == 'sequence'" class="grid-cell selector">
                                    <img id="${data['id']}_movedown" src="/static/images/down.png" class="listImage" border="0" title="${_('Move Down')}" seq="${str(data['_seq'])}" onclick="new ListView('${name}').moveDown(${data['id']})"/>
                                </span>
                            </td>
                            <td py:if="buttons" class="grid-cell button" nowrap="nowrap">
                                <span py:for="button in buttons" py:replace="button.display(parent=name, **button.params_from(data))"/>        
                            </td>
                            <td py:if="editable" class="grid-cell selector">
                                <img src="/static/images/delete_inline.gif" class="listImage" border="0" title="${_('Delete')}" onclick="new ListView('${name}').remove(${data['id']})"/>
                            </td>
                        </tr>
                        		
                        <span py:for="i, d in enumerate(data)" py:strip="">
                            <tr py:if="d['id'] == edit_inline" class="grid-row" py:replace="make_editors(d)"/>
                            <tr py:if="d['id'] != edit_inline" class="grid-row" py:replace="make_row(d)"/>
                        </span>

                        <tr py:for="i in range(0, 4 - len(data))" class="grid-row">
                            <td width="1%" py:if="selector" class="grid-cell selector">&nbsp;</td>
                            <td py:if="editable" style="text-align: center" class="grid-cell selector">&nbsp;</td>
                            <td py:for="i, (field, field_attrs) in enumerate(headers)" class="grid-cell">&nbsp;</td>
                            <td py:if="buttons" class="grid-cell button">&nbsp;</td>
                            <td py:if="editable" style="text-align: center" class="grid-cell selector">&nbsp;</td>
                        </tr>

                    </tbody>
                    
                    <tfoot py:if="field_total">                                    
                        <tr class="field_sum">
                            <td width="1%" py:if="selector" class="grid-cell">&nbsp;</td>
                            <td width="1%" py:if="editable" class="grid-cell">&nbsp;</td>
                            <td py:if="buttons" class="grid-cell button"><div style="width: 0px;"></div></td>
                            <td py:for="i, (field, field_attrs) in enumerate(headers)" class="grid-cell" style="text-align: right; padding: 2px;" nowrap="nowrap">
                                 <span py:if="'sum' in field_attrs" py:strip="">
                                     <span py:for="key, val in field_total.items()" py:strip="">
                                         <span py:if="field == key" style="border: 1px inset ; display: block; padding: 0px 1px;">${val[1]}</span>
                                     </span>
                                 </span>
                                 <span py:if="'sum' not in field_attrs" py:strip="">&nbsp;</span>
                            </td>
                            <td width="1%" py:if="editable" class="grid-cell">&nbsp;</td>
                        </tr>
                    </tfoot>
                    
                </table>
                
                <script type="text/javascript">
                    new SortableGrid('${name}_grid');
                </script>
            </td>
        </tr>
        
        <tr class="pagerbar" py:if="pageable">
            <td class="pagerbar-cell pagerbar-links" align="left">
                <a href="javascript: void(0)" onclick="new ListView('$name').importData()">Import</a> | <a href="javascript: void(0)" onclick="new ListView('$name').exportData()">Export</a>
            </td>
            <td class="pagerbar-cell" align="right" py:content="pager.display(pager_id=2)"></td>
        </tr>
    </table>
</div>
