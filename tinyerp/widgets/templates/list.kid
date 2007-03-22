<span xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
    <table width="100%" cellpadding="0" cellspacing="1" border="0" id="widget" class="grid">
        <thead>
            <tr class="even">
                <th style="text-align: center; width: 25px" py:if="checkable"><input type="checkbox" id="checkall" onclick="checkall(this)"/></th>
                <th py:for="field in headers" py:content="field[1]" class="col_${headers.index(field)}">Title</th>
                <th style="text-align: center; width: 20px" py:if="editable"></th>
                <th style="text-align: center; width: 20px" py:if="editable"></th>
            </tr>
        </thead>
        <tbody>
            <?python row_class = ['even', 'odd']?>
            <tr py:for="row in data" class="${row_class[data.index(row) % 2]}">
                <td align="center" py:if="checkable"><input type="checkbox" name="check" value="${row['id']}"/></td>
                <td py:for="name, title in headers" py:content="row[name]">Data</td>
                <td py:if="editable" style="text-align: center">
                    <a class="imglink" href="/edit?view_id=False&amp;model=${model}&amp;id=${row['id']}" ><img src="/static/images/edit_inline.gif" border="0" title="Edit"/></a>
                </td>
                <td py:if="editable" style="text-align: center">
                    <a class="imglink" onclick="alert('Not implemented yet!')" ><img src="/static/images/delete_inline.gif" border="0" title="Delete"/></a>
                </td>
            </tr>
        </tbody>
    </table>
</span>
