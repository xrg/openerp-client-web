<span xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">

    <script language="javascript">
        function ${name}_checkall(selector){
            boxes = document.getElementsByName('${name}_checkbox');
            forEach(boxes, function(b){
                b.checked = selector.checked;
            });
        }

        function edit_${name}_record(id){
            window.location.href = URL('/edit', {view_id: 'False', model: '${model}', id: id});
        }
    </script>

    <table class="grid" border="0" cellpadding="1" cellspacing="1">
        <thead>
            <tr>
                <th py:if="checkable" class="listButton">
                    <input type="checkbox" onclick="${name}_checkall(this)"/>
                </th>
                <th py:for="header in headers" py:content="header[1]">Header</th>
                <th py:if="editable" class="listButton"></th>
                <th py:if="editable" class="listButton"></th>
            </tr>
        </thead>                
        <tbody id="${name}_body"></tbody>
    </table>  

</span>
