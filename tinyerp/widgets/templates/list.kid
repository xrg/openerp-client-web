<span xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
    <script language = "javascript">
    function checkAll(selector){
		
			boxes = document.getElementsByName('check');
			
			forEach(boxes, function(b){
				b.checked = selector.checked;
			});
		}
	</script>
    <table width="100%" cellpadding="0" cellspacing="1" border="0" id="widget" class="grid">
        <thead>
            <tr class="even">
                <th style="text-align: center; width: 25px" py:if="selectable"><input type="checkbox" id="checkall" onClick="checkAll(this)"/></th>
                <th py:for="field in headers" py:content="field[1]" class="col_${headers.index(field)}">Title</th>
                <th style="text-align: center; width: 20px" py:if="editable"></th>
                <th style="text-align: center; width: 20px" py:if="editable"></th>
            </tr>
        </thead>
        <tbody>
            <?python row_class = ['even', 'odd']?>
            <tr py:for="row in data" class="${row_class[data.index(row) % 2]}">
                <td align="center" py:if="selectable"><input type="checkbox" name="check" value="${row['id']}"/></td>
                <td py:for="name, title in headers" py:content="row[name]">Data</td>
                <td py:if="editable" style="text-align: center">
                    <img src="/static/images/edit_inline.gif" class="listImage" border="0" title="Edit" onclick="inline_edit(${row['id']})"/>
                </td>
                <td py:if="editable" style="text-align: center">
                    <img src="/static/images/delete_inline.gif" class="listImage" border="0" title="Delete" onclick="inline_delete(${row['id']})"/>
                </td>
            </tr>

            <tr py:if="not data" py:for="i in range(6)" class="even">
                <td align="center" py:if="selectable"></td>
                <td py:for="name, title in headers">&nbsp;</td>
                <td py:if="editable" style="text-align: center">
                </td>
                <td py:if="editable" style="text-align: center">
                </td>
            </tr>

        </tbody>
    </table>
</span>
