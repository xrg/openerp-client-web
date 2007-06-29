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
        <td width="1%" py:if="selector" class="grid-header-cell">
            <input type="checkbox" class="checkbox" py:if="selector=='checkbox'" onclick="new ListView('${name}').checkAll(this.checked)"/>
        </td>
        <td py:for="(field, field_attrs) in headers" py:content="field_attrs['string']" class="grid-header-cell ${field_attrs.get('type', 'char')}">Title</td>
        <td width="1%" py:if="editable" class="grid-header-cell">&nbsp;</td>
        <td width="1%" py:if="editable" class="grid-header-cell">&nbsp;</td>
    </tr>

    <tr py:for="i, row in enumerate(data)" class="grid-row">
        <td py:if="selector" class="grid-header-cell">
            <input type="${selector}" class="${selector}" id="${name}/${row['id']}" name="${name}" value="${row['id']}"/>
        </td>
        <td py:for="i, (field, field_attrs) in enumerate(headers)" class="grid-header-cell ${field_attrs.get('type', 'char')}" style="color: ${row[field].color};" >
            <a py:strip="(show_links &lt; 0 or (i &gt; 0 and show_links==0)) or not row[field].link" href="${row[field].link}" onclick="${row[field].onclick}">${row[field]}</a>
            <span py:if="row[field].text == ''">&nbsp;</span>
        </td>
        <td py:if="editable" class="grid-header-cell" style="text-align: center; padding: 0px;">
            <img src="/static/images/edit_inline.gif" class="listImage" border="0" title="Edit" onclick="inlineEdit(${row['id']}, '${source}')"/>
        </td>
        <td py:if="editable" class="grid-header-cell" style="text-align: center; padding: 0px;">
            <img src="/static/images/delete_inline.gif" class="listImage" border="0" title="Delete" onclick="inlineDelete(${row['id']}, '${source}')"/>
        </td>
    </tr>
    
    <tr py:for="i in range(0, 4 - len(data))" class="grid-row">
        <td width="1%" py:if="selector" class="grid-header-cell">&nbsp;</td>
        <td py:for="i, (field, field_attrs) in enumerate(headers)" class="grid-header-cell">&nbsp;</td>
        <td py:if="editable" style="text-align: center" class="grid-header-cell">&nbsp;</td>
        <td py:if="editable" style="text-align: center" class="grid-header-cell">&nbsp;</td>        
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
