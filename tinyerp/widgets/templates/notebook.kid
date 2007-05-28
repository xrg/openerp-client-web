<div class='tabber' id="${name}" xmlns:py="http://purl.org/kid/ns#">
    <div class='tabbertab' py:for="page in children">
        <h3>${page.string}</h3>
        <div>
            ${page.display(value_for(page), **params_for(page))}
        </div>
    </div>
</div>