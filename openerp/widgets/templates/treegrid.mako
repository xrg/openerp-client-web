<span id="${name}"/>
    <script type="text/javascript">
        var ${name} = new TreeGrid('${name}');
        
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

