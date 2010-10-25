<span id="${name}">
    <script type="text/javascript">
        treeGrids['${name}'] = new TreeGrid('${name}', {
            'showheaders': ${showheaders and 'true' or 'false'},
            'onselect': ${onselection or 'null'},
            'onbuttonclick': ${onbuttonclick or 'null'},
            'onheaderclick': ${onheaderclick or 'null'},
            'expandall': ${(expandall and 'true') or 'false'},
            'linktarget': ${linktarget}
        });
        treeGrids['${name}'].setHeaders(${headers|n});
        treeGrids['${name}'].setRecords('${url}', ${url_params|n});
        jQuery(document).ready(jQuery.proxy(treeGrids['${name}'], 'render'));
    </script>
</span>

