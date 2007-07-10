<table id="${name}" class="grid" width="100%" cellspacing="0" cellpadding="0" xmlns:py="http://purl.org/kid/ns#">
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
        </td>
        <td py:for="(field, field_attrs) in headers" id="grid-data-column/${(name != '_terp_list' or None) and (name + '/')}${field}" class="grid-cell ${field_attrs.get('type', 'char')}" py:content="field_attrs['string']">Title</td>
        <td width="1%" py:if="editable" class="grid-cell">&nbsp;</td>
        <td width="1%" py:if="editable" class="grid-cell">&nbsp;</td>
    </tr>
    
    <tr py:def="make_editors(data=None)" class="grid-row editors" py:if="editable and editors">
        <td py:if="selector" class="grid-cell">&nbsp;</td>
        <td py:for="i, (field, field_attrs) in enumerate(headers)" class="grid-cell">
            ${editors[field].display()}
        </td>
        <td class="grid-cell" style="text-align: center; padding: 0px;">
            <!-- begin hidden fields -->
            <span py:for="field, field_attrs in hiddens" py:replace="editors[field].display()"/>
            <!-- end of hidden fields -->
            <img src="/static/images/save_inline.gif" class="listImage editors" border="0" title="Update" onclick="new ListView('${name}').save(${(data and data['id']) or 'null'})"/>
        </td>
        <td class="grid-cell" style="text-align: center; padding: 0px;">
            <img src="/static/images/delete_inline.gif" class="listImage editors" border="0" title="Cancel" onclick="new ListView('${name}').reload()"/>
        </td>
    </tr>
    
    <tr py:def="make_row(data)" class="grid-row">
        <td py:if="selector" class="grid-cell">
            <input type="${selector}" class="${selector} grid-record-selector" id="${name}/${data['id']}" name="${name}" value="${data['id']}"/>
        </td>
        <td py:for="i, (field, field_attrs) in enumerate(headers)" class="grid-cell ${field_attrs.get('type', 'char')}" style="color: ${data[field].color};" >
            <a py:strip="(show_links &lt; 0 or (i &gt; 0 and show_links==0)) or not data[field].link" href="${data[field].link}" onclick="${data[field].onclick}">${data[field]}</a>
            <span py:if="data[field].text == ''">&nbsp;</span>
        </td>
        <td py:if="editable" class="grid-cell" style="text-align: center; padding: 0px;">
            <img src="/static/images/edit_inline.gif" class="listImage" border="0" title="Edit" py:if="not editors" onclick="inlineEdit(${data['id']}, '${source}')"/>
            <img src="/static/images/edit_inline.gif" class="listImage" border="0" title="Edit" py:if="editors" onclick="new ListView('${name}').edit(${data['id']})"/>
        </td>
        <td py:if="editable" class="grid-cell" style="text-align: center; padding: 0px;">
            <img src="/static/images/delete_inline.gif" class="listImage" border="0" title="Delete" onclick="new ListView('${name}').remove(${data['id']})"/>
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

	<tr class="pagerbar" py:if="pageable">
	    <td colspan="${columns}" class="pagerbar-cell">
	        <table border="0" cellpadding="0" cellspacing="0" width="100%">
	            <tr>
					<td class="pagerbar-links">		 
						<a href="#">Import</a> |
						<a href="#">Export</a>
					</td>
                    <td align="right" py:content="pager.display(pager_id='pager2')"></td>
                </tr>
            </table>
        </td>
	</tr>
</table>
