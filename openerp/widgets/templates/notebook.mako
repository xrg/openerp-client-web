<div class='tabber' id="${name}">
    % for page in children:
    <div class='tabbertab' title="${page.string}" attrs="${str(page.attributes)}">
        <div>${display_child(page)}</div>
    </div>
    % endfor
</div>
<script type="text/javascript">
    tabberOptions.div = getElement('${name}');
    tabberOptions.div.tabber = new tabberObj(tabberOptions);
</script>

