<span xmlns:py="http://purl.org/kid/ns#">
<span  id="${field_id}"/>
    <script type="text/javascript">
        var ${field_id} = new TreeGrid('${field_id}', '${headers}');

        ${field_id}.onopen = ${onopen or 'null'};
        ${field_id}.onselection = ${onselection or 'null'};

        ${field_id}.action_url = '${action_url or 'null'}';
        ${field_id}.action_params = ${ustr(action_params or 'null')};

        ${field_id}.load('${url}', ${str(ids)}, {model: '${model}', fields:'${fields}', domain: "${str(domain)}", field_parent: '${field_parent}'});
    </script>
</span>