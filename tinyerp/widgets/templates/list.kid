<table xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" width="100%" cellpadding="0" cellspacing="1" border="0" id="${name}" class="grid">

    <thead>
        <tr class="even">
            <th style="text-align: center; width: 25px" py:if="selectable"><input type="checkbox" onClick="new ListView('${name}').checkAll(this.checked)"/></th>
            <th py:for="field in headers" py:content="field[1]" class="col_${headers.index(field)}">Title</th>
            <th style="text-align: center; width: 20px" py:if="editable"></th>
            <th style="text-align: center; width: 20px" py:if="editable"></th>
        </tr>
    </thead>
    <tbody>
        <tr py:for="i, row in enumerate(data)" class="${i%2 and 'odd' or 'even'}">
            
            <td align="center" py:if="selectable">
                <input type="checkbox" id="${name}/${row['id']}" name="${name}" value="${row['id']}"/>
            </td>                
            <td py:for="field, title in headers" py:content="row[field]">Data</td>                
            <td py:if="editable" style="text-align: center">
                <img src="/static/images/edit_inline.gif" class="listImage" border="0" title="Edit" onclick="inline_edit(${row['id']}, ${(o2m and '\x27%s\x27'%o2m) or 'null'})"/>
            </td>
            <td py:if="editable" style="text-align: center">
                <img src="/static/images/delete_inline.gif" class="listImage" border="0" title="Delete" onclick="inline_delete(${row['id']}, ${(o2m and '\x27%s\x27'%o2m) or 'null'})"/>
            </td>
        </tr>

        <tr py:if="not data" py:for="i in range(6)" class="even">
            <td align="center" py:if="selectable"></td>
            <td py:for="field, title in headers">&nbsp;</td>
            <td py:if="editable" style="text-align: center">
            </td>
            <td py:if="editable" style="text-align: center">
            </td>
        </tr>

    </tbody>
</table>