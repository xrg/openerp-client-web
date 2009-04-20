<span id="${name}"/>
    <script type="text/javascript">
        var ${name} = new TreeGrid('${name}');
        
        ${name}.options.showheaders = ${(showheaders and 'true') or 'false'};
        ${name}.options.onselect = ${onselection or 'null'};
        ${name}.options.onbuttonclick = ${onbuttonclick or 'null'};
        ${name}.options.onheaderclick = ${onheaderclick or 'null'};
        
        ${name}.options.expandall = ${(expandall and 'true') or 'false'};

        ${name}.setHeaders(${ustr(headers)});
        ${name}.setRecords('${url}', ${ustr(url_params)});
        
        ${name}.render();
    </script>
</span>

