<table id="${name}" class="grid" width="100%" cellspacing="0" cellpadding="0" xmlns:py="http://purl.org/kid/ns#">
	<tr class="pager" py:if="pageable">
	    <td colspan="${columns}">
	        <table border="0" cellpadding="0" cellspacing="0" width="100%">
	            <tr>
	                <td align="right">
						<a href="#" onclick="${options.on_first}"><img border="0" align="absmiddle" src="/static/images/pager_start.gif"/> Start</a>
						<a href="#" onclick="${options.on_previous}"><img border="0" align="absmiddle" src="/static/images/pager_prev.gif"/> Previous</a>
						<a href="#">(${options.offset} to ${options.limit + options.offset})</a>
						<a href="#" onclick="${options.on_next}">Next <img border="0" align="absmiddle" src="/static/images/pager_next.gif"/></a>
						<a href="#" onclick="${options.on_end}">End <img border="0" align="absmiddle" src="/static/images/pager_end.gif"/></a>
					</td>			                
	            </tr>
	        </table>
	    </td>
	</tr>

    <tr class="header">
        <td width="1%" py:if="selectable">
            <input type="checkbox" class="checkbox" py:if="selector=='checkbox'" onclick="new ListView('${name}').checkAll(this.checked)"/>
        </td>
        <td py:for="field in headers" py:content="field[1]">Title</td>
        <td align="center" width="20px" py:if="editable"></td>
        <td align="center" width="20px" py:if="editable"></td>
    </tr>

    <tr py:for="i, row in enumerate(data)" class="row">		
        <td width="1%" py:if="selectable">
            <input type="${selector}" class="${selector}" id="${name}/${row['id']}" name="${name}" value="${row['id']}"/>
        </td>
        <td py:for="field, title in headers" py:content="row[field]">Data</td>
        <td py:if="editable" style="text-align: center">
            <img src="/static/images/edit_inline.gif" class="listImage" border="0" title="Edit" onclick="inlineEdit(${row['id']}, '${source}')"/>
        </td>
        <td py:if="editable" style="text-align: center">
            <img src="/static/images/delete_inline.gif" class="listImage" border="0" title="Delete" onclick="inlineDelete(${row['id']}, '${source}')"/>
        </td>
    </tr>

	<tr class="pager" py:if="pageable">
	    <td colspan="${columns}">
	        <table border="0" cellpadding="0" cellspacing="0" width="100%">
	            <tr>		            			        
					<td>		 
						<a href="#">Import</a> |
						<a href="#">Export</a>
					</td>
					<td align="right">
						<a href="#" onclick="${options.on_first}"><img border="0" align="absmiddle" src="/static/images/pager_start.gif"/> Start</a>
						<a href="#" onclick="${options.on_previous}"><img border="0" align="absmiddle" src="/static/images/pager_prev.gif"/> Previous</a>
						<a href="#">(${options.offset} to ${options.limit + options.offset})</a>
						<a href="#" onclick="${options.on_next}">Next <img border="0" align="absmiddle" src="/static/images/pager_next.gif"/></a>
						<a href="#" onclick="${options.on_end}">End <img border="0" align="absmiddle" src="/static/images/pager_end.gif"/></a>
					</td>
                </tr>
            </table>
        </td>
	</tr>
</table>