<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
<span  id="${field_id}"/>
    <script type="text/javascript">
        var ${field_id} = new TreeGrid('${field_id}');
        
        ${field_id}.options.showheaders = ${(showheaders and 'true') or 'false'};
        ${field_id}.options.onselect = ${onselection or 'null'};
        ${field_id}.options.onbuttonclick = ${onbuttonclick or 'null'};
        ${field_id}.options.onheaderclick = ${onheaderclick or 'null'};
        
        ${field_id}.options.expandall = ${(expandall and 'true') or 'false'};

        ${field_id}.setHeaders(${ustr(headers)});
        ${field_id}.setRecords('${url}', ${ustr(url_params)});
        
        ${field_id}.render();
    </script>
</span>