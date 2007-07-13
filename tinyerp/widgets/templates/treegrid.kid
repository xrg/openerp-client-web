<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
<span  id="${field_id}"/>
    <script type="text/javascript">
        var ${field_id} = new TreeGrid('${field_id}', '${headers}');

        ${field_id}.show_headers = ${(show_headers and 'true') or 'false'};
        ${field_id}.onopen = ${onopen or 'null'};
        ${field_id}.onselection = ${onselection or 'null'};

        ${field_id}.load('${url}', ${str(ids)}, {model: '${model}', domain: "${str(domain)}", field_parent: '${field_parent}'});
    </script>
</span>