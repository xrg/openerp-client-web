<div xmlns:py="http://purl.org/kid/ns#">

    <table id="${name}" class="grid" width="100%" cellspacing="0" cellpadding="0">
        <tbody>
            <tr class="pagerbar" py:if="pageable">
                <td colspan="${columns}" class="pagerbar-cell">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td align="right" py:content="pager.display()"></td>
                        </tr>
                    </table>
                </td>
            </tr>

            <tr class="grid-header">
                <td width="1%" py:if="selector" class="grid-cell">
                    <input type="checkbox" class="checkbox grid-record-selector" py:if="selector=='checkbox'" onclick="new ListView('${name}').checkAll(this.checked)"/>
                    <span py:if="selector!='checkbox'">&nbsp;</span>
                </td>
                <td py:for="(field, field_attrs) in headers" id="grid-data-column/${(name != '_terp_list' or None) and (name + '/')}${field}" class="grid-cell ${field_attrs.get('type', 'char')}" kind="${field_attrs.get('type', 'char')}" py:content="field_attrs['string']">Title</td>
                <td width="1%" py:if="editable" class="grid-cell">&nbsp;</td>
                <td width="1%" py:if="editable" class="grid-cell">&nbsp;</td>
            </tr>
        </tbody>

        <tr py:def="make_editors(data=None)" class="grid-row editors" py:if="editable and editors">
            <td py:if="selector" class="grid-cell">&nbsp;</td>
            <td py:for="i, (field, field_attrs) in enumerate(headers)" class="grid-cell">
                ${editors[field].display()}
            </td>
            <td class="grid-cell" style="text-align: center; padding: 0px;">
                <!-- begin hidden fields -->
                <span py:for="field, field_attrs in hiddens" py:replace="editors[field].display()"/>
                <!-- end of hidden fields -->
                <img src="/static/images/save_inline.gif" class="listImage editors" border="0" title="${_('Update')}" onclick="new ListView('${name}').save(${(data and data['id']) or 'null'})"/>
            </td>
            <td class="grid-cell" style="text-align: center; padding: 0px;">
                <img src="/static/images/delete_inline.gif" class="listImage editors" border="0" title="${_('Cancel')}" onclick="new ListView('${name}').reload()"/>
            </td>
        </tr>

        <tr py:def="make_row(data)" class="grid-row" record="${data['id']}">
            <td py:if="selector" class="grid-cell">
                <input type="${selector}" class="${selector} grid-record-selector" id="${name}/${data['id']}" name="${name}" value="${data['id']}"/>
            </td>
            <td py:for="i, (field, field_attrs) in enumerate(headers)" class="grid-cell ${field_attrs.get('type', 'char')}" style="color: ${data[field].color};" >
                <span py:if="not (field_attrs.get('type')=='many2one' and link=='0')" py:strip="">
                    <a py:strip="(show_links &lt; 0 or (i &gt; 0 and show_links==0)) or not data[field].link" href="${data[field].link}" onclick="${data[field].onclick}">${data[field]}</a>
                 </span>
                <span py:if="field_attrs.get('type')=='many2one' and link=='0'" py:strip="">
                    ${data[field]}
                </span>
                <span py:if="data[field].text == ''">&nbsp;</span>
            </td>
            <td py:if="editable" width="22" class="grid-cell" style="text-align: center; padding: 0px;">
                <img src="/static/images/edit_inline.gif" class="listImage" border="0" title="${_('Edit')}" py:if="not editors" onclick="editRecord(${data['id']}, '${source}')"/>
                <img src="/static/images/edit_inline.gif" class="listImage" border="0" title="${_('Edit')}" py:if="editors" onclick="new ListView('${name}').edit(${data['id']})"/>
            </td>
            <td py:if="editable" width="22" class="grid-cell" style="text-align: center; padding: 0px;">
                <img src="/static/images/delete_inline.gif" class="listImage" border="0" title="${_('Delete')}" onclick="new ListView('${name}').remove(${data['id']})"/>
            </td>
        </tr>

        <tr py:replace="make_editors()" py:if="edit_inline == -1"/>

        <span py:for="i, d in enumerate(data)" py:strip="">
            <tr py:if="d['id'] == edit_inline" class="grid-row" py:replace="make_editors(d)"/>
            <tr py:if="d['id'] != edit_inline" class="grid-row" py:replace="make_row(d)"/>
        </span>

        <tr py:for="i in range(0, 4 - len(data))" class="grid-row">
            <td width="1%" py:if="selector" class="grid-cell">&nbsp;</td>
            <td py:for="i, (field, field_attrs) in enumerate(headers)" class="grid-cell">&nbsp;</td>
            <td py:if="editable" style="text-align: center" class="grid-cell">&nbsp;</td>
            <td py:if="editable" style="text-align: center" class="grid-cell">&nbsp;</td>
        </tr>

        <tr class="field_sum" py:if="field_total">
            <td width="1%" py:if="selector" class="grid-cell">&nbsp;</td>
            <td py:for="i, (field, field_attrs) in enumerate(headers)" class="grid-cell" style="text-align: right" nowrap="nowrap">
                 <span py:if="'sum' in field_attrs" py:strip="">
                     <span py:for="key, val in field_total.items()" py:strip="">
                         <span py:if="field == key" style="border: 1px inset ; padding: 0px 4px; display: block;">${val[1]}</span>
                     </span>
                 </span>
                 <span py:if="'sum' not in field_attrs" py:strip="">&nbsp;</span>
            </td>
            <td width="1%" py:if="editable" class="grid-cell">&nbsp;</td>
            <td width="1%" py:if="editable" class="grid-cell">&nbsp;</td>
        </tr>

        <tr class="pagerbar" py:if="pageable">
            <td colspan="${columns}" class="pagerbar-cell">
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                        <td class="pagerbar-links">         
                            <a href="javascript: void(0)" onclick="new ListView('$name').importData()">Import</a> | <a href="javascript: void(0)" onclick="new ListView('$name').exportData()">Export</a>
                        </td>
                        <td align="right" py:content="pager.display(pager_id='pager2')"></td>
                    </tr>
                </table>
            </td>
        </tr>
        <script type="text/javascript">
            do_sort('${name}');
        </script>
    </table>
</div>
