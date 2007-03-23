<span xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">

    <span id="${model.replace('.', '_')}_table"></span>

    <script language="javascript">  
        new AjaxList("${model.replace('.', '_')}_table", ${checkable}, ${editable}).render('/list_info', {model: '${model}'});
    </script>

</span>
