<span id="${name}"/>
    <script type="text/javascript">
    
        var ${name} = new TreeGrid('${name}');
        
        ${name}.options.showheaders = ${(showheaders and 'true') or 'false'};
        ${name}.options.onselect = ${onselection or 'null'};
        ${name}.options.onbuttonclick = ${onbuttonclick or 'null'};
        ${name}.options.onheaderclick = ${onheaderclick or 'null'};
        
        ${name}.options.expandall = ${(expandall and 'true') or 'false'};
        ${name}.options.linktarget = ${linktarget};
        
        MochiKit.DOM.addLoadEvent(function(e){
        
            ${name}.setHeaders(${headers|n});
            ${name}.setRecords('${url}', ${url_params|n});
        
            ${name}.render();
        });
    </script>
</span>

