<span xmlns:py="http://purl.org/kid/ns#">
<span  id="${id}"/>
    <script type="text/javascript">
        var ${id} = new TreeGrid('${id}', '${headers}');

        ${id}.onopen = ${onopen or 'null'};
        ${id}.onselection = ${onselection or 'null'};

        ${id}.action_url = '${action_url or 'null'}';
        ${id}.action_params = ${ustr(action_params or 'null')};

        ${id}.load('${url}', -1, {model: '${model}', fields:'${fields}', domain: "${str(domain)}", field_parent: '${field_parent}'});
    </script>
</span>