<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <div class='tabber' id="${name}">
        <div class='tabbertab' py:for="page in children" title="${page.string}" attrs="${str(page.attributes)}">
            <div py:content="page.display(value_for(page), **params_for(page))"/>
        </div>
    </div>
    <script type="text/javascript">
        tabberOptions.div = getElement('${name}');
        tabberOptions.div.tabber = new tabberObj(tabberOptions);
    </script>
</span>
