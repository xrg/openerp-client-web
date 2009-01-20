<div class='tabber' id="${name}" xmlns:py="http://purl.org/kid/ns#">
    <div class='tabbertab' py:for="page in children" py:if="not page.invisible" title="${page.string}" attrs="${str(page.attributes)}">
        <div py:content="page.display(value_for(page), **params_for(page))"/>
    </div>
</div>
