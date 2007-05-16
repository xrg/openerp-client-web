<div xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" style="overflow: auto;">
	<table width="100%" cellpadding="0" cellspacing="1" id="${name}" class="grid">
	    <thead>
	        <tr>
	            <th align="center" width="20px" py:if="selectable">
	                <input type="checkbox" py:if="selector=='checkbox'" onclick="new ListView('${name}').checkAll(this.checked)"/>
	            </th>
	            <th py:for="field in headers" py:content="field[1]">Title</th>
	            <th align="center" width="20px" py:if="editable"></th>
	            <th align="center" width="20px" py:if="editable"></th>
	        </tr>
	    </thead>
	    <tbody>
	        <tr py:for="i, row in enumerate(data)" class="row">

	            <td align="center" py:if="selectable">
	                <input type="${selector}" id="${name}/${row['id']}" name="${name}" value="${row['id']}"/>
	            </td>
	            <td py:for="field, title in headers" py:content="row[field]">Data</td>
	            <td py:if="editable" style="text-align: center">
	                <img src="/static/images/edit_inline.gif" class="listImage" border="0" title="Edit" onclick="inlineEdit(${row['id']}, '${source}')"/>
	            </td>
	            <td py:if="editable" style="text-align: center">
	                <img src="/static/images/delete_inline.gif" class="listImage" border="0" title="Delete" onclick="inlineDelete(${row['id']}, '${source}')"/>
	            </td>
	        </tr>

	        <tr py:if="not data" py:for="i in range(6)" class="row">
	            <td align="center" py:if="selectable"></td>
	            <td py:for="field, title in headers">&nbsp;</td>
	            <td py:if="editable" style="text-align: center">
	            </td>
	            <td py:if="editable" style="text-align: center">
	            </td>
	        </tr>
	    </tbody>
	</table>
</div>